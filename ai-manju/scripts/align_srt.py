#!/usr/bin/env python3
"""
字幕自动对齐工具 — 用 faster-whisper 识别 raw 视频音频的真实时间戳，
配合剧本对白文本输出精确对齐的 SRT。

用法:
  python3 align_srt.py --video <raw.mp4> --srt <input.srt> --out <output.srt> [--model medium] [--lang zh]

工作流:
  1. Whisper 识别视频音频 → 得到带真实时间戳的 segments
  2. 读取输入 SRT 的对白文本作为"黄金文本"
  3. 按顺序对齐：Whisper 段 → 剧本对白
  4. 输出新 SRT：剧本文本 + Whisper 真实时间戳

边界:
  - Whisper 段数 N < 剧本对白数 M：警告，输出仅前 N 句对齐的 SRT
  - Whisper 段数 N > 剧本对白数 M：按相似度匹配，过滤噪声段
  - 对齐后检查字幕重叠，重叠处自动插 50ms 间隙
"""
import argparse
import difflib
import re
import sys
from pathlib import Path


def parse_srt(path):
    """解析 SRT 文件为 [{'index', 'start', 'end', 'text'}] 列表。时间单位 float 秒。"""
    text = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", text.strip())
    entries = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        idx = int(lines[0].strip())
        ts_line = lines[1].strip()
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", ts_line)
        if not m:
            continue
        g = m.groups()
        start = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
        end = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000
        text_content = "\n".join(lines[2:]).strip()
        entries.append({"index": idx, "start": start, "end": end, "text": text_content})
    return entries


def format_ts(seconds):
    """秒 → HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(entries, path):
    """将 entries 写为 SRT 文件。"""
    lines = []
    for i, e in enumerate(entries, 1):
        lines.append(str(i))
        lines.append(f"{format_ts(e['start'])} --> {format_ts(e['end'])}")
        lines.append(e["text"])
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def normalize_text(s):
    """去标点、空格、常见替换，繁→简，用于相似度对比。"""
    try:
        from zhconv import convert
        s = convert(s, "zh-cn")
    except ImportError:
        pass  # 没装 zhconv 也能跑，只是匹配分数会偏低
    s = re.sub(r"[，。！？、……\"\"''《》,.!?\"'\s]", "", s)
    return s.lower()


def similarity(a, b):
    """两串文本的相似度 0-1。"""
    return difflib.SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def align_by_order(whisper_segs, script_entries, min_sim=0.3):
    """
    按顺序对齐：遍历剧本对白，在 Whisper 段中找最佳匹配。
    返回 [{'text'(剧本), 'start'(Whisper), 'end'(Whisper), 'match_sim'}]。
    """
    aligned = []
    w_idx = 0
    n_whisper = len(whisper_segs)
    for s_entry in script_entries:
        s_text = s_entry["text"]
        best_idx = -1
        best_sim = -1.0
        # 在剩余 Whisper 段中向后搜索（允许跳过噪声段，但顺序单调）
        for j in range(w_idx, n_whisper):
            sim = similarity(s_text, whisper_segs[j]["text"])
            if sim > best_sim:
                best_sim = sim
                best_idx = j
            # 已找到高相似度，就停
            if sim >= 0.7:
                break
        if best_idx >= 0 and best_sim >= min_sim:
            w = whisper_segs[best_idx]
            aligned.append({
                "text": s_text,
                "start": w["start"],
                "end": w["end"],
                "match_sim": best_sim,
                "whisper_text": w["text"],
            })
            w_idx = best_idx + 1
        else:
            # 未找到匹配 → 回退到原始剧本时间戳（保留但标记）
            aligned.append({
                "text": s_text,
                "start": s_entry["start"],
                "end": s_entry["end"],
                "match_sim": 0.0,
                "whisper_text": "[未匹配]",
            })
    return aligned


def fix_overlaps(entries, gap=0.05):
    """相邻字幕如重叠，在前段末尾减去 gap 留出间隙。"""
    for i in range(len(entries) - 1):
        if entries[i]["end"] > entries[i + 1]["start"]:
            entries[i]["end"] = entries[i + 1]["start"] - gap
            if entries[i]["end"] < entries[i]["start"] + 0.3:
                entries[i]["end"] = entries[i]["start"] + 0.3
    return entries


def ensure_min_duration(entries, min_dur=0.8):
    """字幕显示时长过短时延长到至少 min_dur 秒（前提不与下一句重叠）。"""
    for i, e in enumerate(entries):
        duration = e["end"] - e["start"]
        if duration < min_dur:
            new_end = e["start"] + min_dur
            if i + 1 < len(entries):
                limit = entries[i + 1]["start"] - 0.05
                new_end = min(new_end, limit)
            e["end"] = max(new_end, e["start"] + 0.3)
    return entries


def cap_duration(entries, chars_per_sec=4.0, min_cap=2.0, max_cap=8.0):
    """
    字幕显示时长上限：按文本字数估算合理阅读时长，避免字幕挂太久。
    公式：cap = max(min_cap, min(字数/chars_per_sec + 1.0, max_cap))
    """
    for e in entries:
        text_len = len(re.sub(r"[，。！？、……\"\"''《》,.!?\"'\s]", "", e["text"]))
        cap = max(min_cap, min(text_len / chars_per_sec + 1.0, max_cap))
        if e["end"] - e["start"] > cap:
            e["end"] = e["start"] + cap
    return entries


def main():
    parser = argparse.ArgumentParser(description="Whisper 字幕自动对齐")
    parser.add_argument("--video", required=True, help="输入视频或音频文件")
    parser.add_argument("--srt", required=True, help="输入 SRT（提供剧本文本）")
    parser.add_argument("--out", required=True, help="输出对齐后的 SRT")
    parser.add_argument("--model", default="medium", help="Whisper 模型大小（tiny/base/small/medium/large-v3）")
    parser.add_argument("--lang", default="zh", help="语言代码")
    parser.add_argument("--device", default="cpu", help="cpu / cuda")
    parser.add_argument("--compute-type", default="int8", help="int8 / float16 / float32")
    parser.add_argument("--min-sim", type=float, default=0.3, help="最低相似度阈值，低于此值视为未匹配")
    args = parser.parse_args()

    video = Path(args.video)
    srt_in = Path(args.srt)
    if not video.exists():
        print(f"❌ 视频不存在: {video}", file=sys.stderr)
        sys.exit(1)
    if not srt_in.exists():
        print(f"❌ SRT 不存在: {srt_in}", file=sys.stderr)
        sys.exit(1)

    # 1. 读取剧本 SRT
    script_entries = parse_srt(srt_in)
    print(f"📜 剧本对白: {len(script_entries)} 句")

    # 2. Whisper 识别
    print(f"🔊 加载模型 {args.model} ({args.device}/{args.compute_type}) ...")
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    print(f"🎧 识别视频音频 {video} ...")
    segments, info = model.transcribe(
        str(video),
        language=args.lang,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 100},
        word_timestamps=False,
        initial_prompt="以下是普通话的简体中文对白。",
    )
    whisper_segs = []
    for s in segments:
        whisper_segs.append({"start": s.start, "end": s.end, "text": s.text.strip()})

    # 按标点拆分合并段：Whisper VAD 有时把多句对白合并成一个 segment，
    # 按 ? ! 。 拆分，按文本长度比例线性分配时间戳
    def split_by_punct(segs):
        out = []
        # 以句末标点切分（保留标点）
        pat = re.compile(r"[^?!。？！]+[?!。？！]?")
        for s in segs:
            text = s["text"].strip()
            parts = [p.strip() for p in pat.findall(text) if p.strip()]
            if len(parts) <= 1:
                out.append(s)
                continue
            total_len = sum(len(p) for p in parts)
            cursor = s["start"]
            duration = s["end"] - s["start"]
            for p in parts:
                span = duration * len(p) / total_len
                out.append({"start": cursor, "end": cursor + span, "text": p})
                cursor += span
        return out

    whisper_segs = split_by_punct(whisper_segs)

    print(f"🗣️  Whisper 识别: {len(whisper_segs)} 段（已按标点拆分）")
    for i, w in enumerate(whisper_segs):
        print(f"   [{i+1}] {w['start']:.2f}-{w['end']:.2f}s  {w['text']}")

    # 3. 对齐
    aligned = align_by_order(whisper_segs, script_entries, min_sim=args.min_sim)

    # 4. 修复重叠 + 最短时长 + 最长时长
    aligned = fix_overlaps(aligned)
    aligned = ensure_min_duration(aligned)
    aligned = cap_duration(aligned)

    # 5. 输出 SRT
    write_srt(aligned, args.out)

    # 6. 报告
    print("\n📊 对齐报告:")
    print(f"{'#':>3}  {'剧本 →':>8}  {'Whisper':>8}  {'相似度':>6}  剧本文本")
    for i, a in enumerate(aligned, 1):
        s_orig = script_entries[i - 1]
        delta = a["start"] - s_orig["start"]
        marker = "✅" if a["match_sim"] >= args.min_sim else "⚠️ "
        print(f"{marker} {i:>2}  {s_orig['start']:>6.2f}s  {a['start']:>6.2f}s  ({delta:+.2f})  {a['match_sim']:.2f}  {a['text'][:30]}")

    matched = sum(1 for a in aligned if a["match_sim"] >= args.min_sim)
    print(f"\n✅ 成功对齐 {matched}/{len(aligned)} 句")
    print(f"📝 输出: {args.out}")


if __name__ == "__main__":
    main()
