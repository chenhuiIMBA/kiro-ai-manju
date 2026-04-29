#!/usr/bin/env python3
"""豆包语音合成 TTS（V3） — 火山引擎语音合成大模型 HTTP Chunked 单向流式 API。

用法:
    # 基础合成
    python3 doubao_tts.py synthesize --text "你好世界" -d ./output

    # 指定音色和情感
    python3 doubao_tts.py synthesize \
      --text "我不会再逃了。" \
      --speaker zh_male_qingcang_uranus_bigtts \
      --emotion sad --emotion-scale 4 \
      -d ./output

    # 角色音色参考（ai-manju 集成用）
    python3 doubao_tts.py synthesize \
      --text "我叫林小夜。你不用帮我。" \
      --speaker zh_male_ruyayichen_uranus_bigtts \
      --speed -10 --emotion coldness --encoding mp3 \
      -d ./human-design/林小夜/

    # 列出推荐音色
    python3 doubao_tts.py voices

环境变量:
    DOUBAO_TTS_API_KEY      新版 API Key（推荐，从 https://console.volcengine.com/speech/new 获取）
    DOUBAO_TTS_RESOURCE_ID  资源 ID（默认 seed-tts-2.0，可选 seed-tts-1.0）

    旧版凭证（兼容，从 https://console.volcengine.com/speech/app 获取）:
    DOUBAO_TTS_APP_ID      应用 ID
    DOUBAO_TTS_ACCESS_KEY  Access Token
"""

import argparse
import base64
import json
import os
import sys
import uuid
import urllib.request
import urllib.error


API_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
TIMEOUT = 60

# ── 音色列表（豆包语音合成模型 2.0 / seed-tts-2.0）────────
# 来源: https://www.volcengine.com/docs/6561/1257544（本地: doc/auto-generate/api-doc/tts-api/）
# ⚠️ 1.0 音色（mars_bigtts/moon_bigtts/wvae_bigtts）将于 2026.06.30 下线，推荐迁移到 2.0 对应音色
# 2.0 命名规则: {语言}_{性别}_{特征}_uranus_bigtts（共 ~90 个，此处精选常用）

SPEAKER_CATEGORIES = {
    "角色扮演·男": [
        {"id": "zh_male_qingcang_uranus_bigtts",       "style": "深沉威严",   "use": "霸道男主、帝王、反派"},
        {"id": "zh_male_ruyayichen_uranus_bigtts",     "style": "儒雅清冷",   "use": "清冷男主、古风公子"},
        {"id": "zh_male_silang_uranus_bigtts",          "style": "低沉磁性",   "use": "成熟男性、权谋角色"},
        {"id": "zh_male_shaonianzixin_uranus_bigtts",  "style": "清澈少年",   "use": "少年男主、热血青年"},
        {"id": "zh_male_aojiaobazong_uranus_bigtts",   "style": "傲娇霸总",   "use": "傲娇男主、霸总"},
        {"id": "zh_male_gaolengchenwen_uranus_bigtts", "style": "高冷沉稳",   "use": "冷酷寡言、谍战角色"},
        {"id": "zh_male_xionger_uranus_bigtts",         "style": "憨厚可爱",   "use": "搞笑角色、萌系"},
        {"id": "zh_male_sunwukong_uranus_bigtts",      "style": "猴哥",       "use": "孙悟空、灵动机智"},
        {"id": "zh_male_lubanqihao_uranus_bigtts",     "style": "鲁班七号",   "use": "游戏角色、机械萌"},
        {"id": "zh_male_tangseng_uranus_bigtts",        "style": "唐僧",       "use": "啰嗦慈悲、喜剧角色"},
        {"id": "zh_male_zhuangzhou_uranus_bigtts",      "style": "庄周",       "use": "逍遥淡然、仙侠"},
        {"id": "zh_male_zhubajie_uranus_bigtts",        "style": "猪八戒",     "use": "贪吃憨厚、搞笑"},
        {"id": "zh_male_ruyaqingnian_uranus_bigtts",   "style": "儒雅青年",   "use": "温润公子、文艺男主"},
        {"id": "zh_male_wennuanahu_uranus_bigtts",     "style": "温暖阿虎",   "use": "暖男、阳光角色"},
        {"id": "zh_male_kailangdidi_uranus_bigtts",    "style": "开朗弟弟",   "use": "活泼小弟、元气少年"},
        {"id": "zh_male_lanyinmianbao_uranus_bigtts",  "style": "懒音绵宝",   "use": "慵懒可爱、萌系"},
        {"id": "zh_male_fanjuanqingnian_uranus_bigtts","style": "反卷青年",   "use": "摆烂吐槽、接地气"},
        {"id": "zh_male_huolixiaoge_uranus_bigtts",    "style": "活力小哥",   "use": "阳光开朗、运动系"},
    ],
    "角色扮演·女": [
        {"id": "zh_female_gaolengyujie_uranus_bigtts", "style": "高冷御姐",   "use": "御姐、冷艳角色"},
        {"id": "zh_female_meilinvyou_uranus_bigtts",   "style": "魅力女友",   "use": "温柔女主、知心角色"},
        {"id": "zh_female_sajiaoxuemei_uranus_bigtts", "style": "撒娇学妹",   "use": "萌系女主、学妹"},
        {"id": "zh_female_shuangkuaisisi_uranus_bigtts","style": "爽快思思",   "use": "爽朗女性、闺蜜"},
        {"id": "zh_female_wenroumama_uranus_bigtts",   "style": "温柔妈妈",   "use": "母亲、温柔长辈"},
        {"id": "zh_female_popo_uranus_bigtts",          "style": "婆婆",       "use": "婆婆、奶奶"},
        {"id": "zh_female_cancan_uranus_bigtts",       "style": "知性灿灿",   "use": "知性优雅、职场女性"},
        {"id": "zh_female_zhishuaiyingzi_uranus_bigtts","style":"直率英子",   "use": "直率女性、大姐大"},
        {"id": "zh_female_linxiao_uranus_bigtts",       "style": "林潇",       "use": "干练女强人"},
        {"id": "zh_female_lingling_uranus_bigtts",      "style": "玲玲姐姐",   "use": "温柔姐姐、邻家"},
        {"id": "zh_female_chunribu_uranus_bigtts",      "style": "春日部姐姐", "use": "活泼搞怪、元气"},
        {"id": "zh_female_yingtaowanzi_uranus_bigtts",  "style": "樱桃丸子",   "use": "可爱少女、童趣"},
        {"id": "zh_female_wuzetian_uranus_bigtts",      "style": "武则天",     "use": "霸气女帝、威严"},
        {"id": "zh_female_gujie_uranus_bigtts",         "style": "顾姐",       "use": "成熟女性、风情"},
        {"id": "zh_female_gufengshaoyu_uranus_bigtts", "style": "古风少御",   "use": "古风、侠女叙事"},
        {"id": "zh_female_wenroushunv_uranus_bigtts",  "style": "温柔淑女",   "use": "言情女主、温婉"},
        {"id": "zh_female_linjianvhai_uranus_bigtts",  "style": "邻家女孩",   "use": "普通女主、日常角色"},
        {"id": "zh_female_chanmeinv_uranus_bigtts",     "style": "谄媚女声",   "use": "谄媚角色、反派女"},
        {"id": "zh_female_nvleishen_uranus_bigtts",     "style": "女雷神",     "use": "霸气女战士"},
        {"id": "zh_female_jiaochuannv_uranus_bigtts",   "style": "娇喘女声",   "use": "软萌娇弱、嗲系"},
        {"id": "zh_female_ganmaodianyin_uranus_bigtts", "style": "感冒电音",   "use": "病弱药感、特色"},
    ],
    "有声阅读·男": [
        {"id": "zh_male_baqiqingshu_uranus_bigtts",    "style": "霸气青叔",   "use": "旁白、年长角色叙事"},
        {"id": "zh_male_shenyeboke_uranus_bigtts",     "style": "深夜播客",   "use": "文艺旁白、内心独白"},
        {"id": "zh_male_xuanyijieshuo_uranus_bigtts",  "style": "悬疑解说",   "use": "悬疑叙事、恐怖故事"},
        {"id": "zh_male_cixingjieshuonan_uranus_bigtts","style":"磁性解说",  "use": "磁性男声、纪录片"},
        {"id": "zh_male_guanggaojieshuo_uranus_bigtts", "style": "广告解说",   "use": "广告旁白、激情男声"},
        {"id": "zh_male_dayi_uranus_bigtts",            "style": "大壹",       "use": "视频配音、沉稳"},
        {"id": "zh_male_yizhipiannan_uranus_bigtts",   "style": "译制片男",   "use": "译制片腔、戏剧化"},
        {"id": "zh_male_dongfanghaoran_uranus_bigtts", "style": "东方浩然",   "use": "正气男主、古风"},
    ],
    "有声阅读·女": [
        {"id": "zh_female_qingxinnvsheng_uranus_bigtts","style":"清新女声",  "use": "清新旁白、文艺"},
        {"id": "zh_female_xiaoxue_uranus_bigtts",       "style": "儿童绘本",   "use": "儿童故事、柔和"},
        {"id": "zh_female_shaoergushi_uranus_bigtts",   "style": "少儿故事",   "use": "童趣旁白、寓教"},
        {"id": "zh_female_mizai_uranus_bigtts",         "style": "咪仔",       "use": "悬疑女声、侦探"},
        {"id": "zh_female_jitangnv_uranus_bigtts",      "style": "鸡汤女",     "use": "情感旁白、励志"},
        {"id": "zh_female_liuchangnv_uranus_bigtts",    "style": "流畅女声",   "use": "流畅叙事、解说"},
        {"id": "zh_female_tianmeiyueyue_uranus_bigtts", "style": "甜美悦悦",   "use": "甜美女主播"},
        {"id": "zh_female_wenrouxiaoya_uranus_bigtts",  "style": "温柔小雅",   "use": "温柔叙述、女性角色"},
        {"id": "zh_female_xinlingjitang_uranus_bigtts", "style": "心灵鸡汤",   "use": "深夜情感、暖声"},
    ],
    "通用·男": [
        {"id": "zh_male_vv_uranus_bigtts",              "style": "Vivi男版",   "use": "通用男声（Vivi）"},
        {"id": "zh_male_m191_uranus_bigtts",            "style": "云舟 2.0",     "use": "通用男声、播报"},
        {"id": "zh_male_taocheng_uranus_bigtts",        "style": "小天 2.0",     "use": "通用男声、聊天"},
        {"id": "zh_male_liufei_uranus_bigtts",          "style": "刘飞 2.0",     "use": "通用男声、自然"},
        {"id": "zh_male_linjiananhai_uranus_bigtts",    "style": "邻家男孩",   "use": "日常男声、亲切"},
        {"id": "zh_male_yangguangqingnian_uranus_bigtts","style":"阳光青年",  "use": "开朗青年、日常"},
        {"id": "zh_male_wenrouxiaoge_uranus_bigtts",    "style": "温柔小哥",   "use": "温柔男声、暖系"},
        {"id": "zh_male_qingshuangnanda_uranus_bigtts", "style": "清爽男大",   "use": "大学生感、清新"},
        {"id": "zh_male_yuanboxiaoshu_uranus_bigtts",   "style": "渊博小叔",   "use": "成熟知性、大叔"},
        {"id": "zh_male_youyoujunzi_uranus_bigtts",     "style": "悠悠君子",   "use": "温和君子、文雅"},
        {"id": "zh_male_kailangxuezhang_uranus_bigtts", "style": "开朗学长",   "use": "学长、阳光"},
        {"id": "zh_male_kuailexiaodong_uranus_bigtts",  "style": "快乐小东",   "use": "快乐闲适、元气"},
    ],
    "通用·女": [
        {"id": "zh_female_vv_uranus_bigtts",             "style": "Vivi 2.0",    "use": "通用女声、方言"},
        {"id": "zh_female_xiaohe_uranus_bigtts",         "style": "小何 2.0",    "use": "通用女声、自然"},
        {"id": "zh_female_sophie_uranus_bigtts",         "style": "魅力苏菲",   "use": "通用女声、聊天"},
        {"id": "zh_female_tianmeixiaoyuan_uranus_bigtts","style": "甜美小源",   "use": "甜美女声、元气"},
        {"id": "zh_female_tianmeitaozi_uranus_bigtts",   "style": "甜美桃子",   "use": "甜美女声、可爱"},
        {"id": "zh_female_peiqi_uranus_bigtts",          "style": "佩奇猪",     "use": "小猪佩奇、童趣"},
        {"id": "zh_female_tvbnv_uranus_bigtts",          "style": "TVB女声",     "use": "港剧腔女声"},
        {"id": "zh_female_qiaopinv_uranus_bigtts",       "style": "俏皮女声",   "use": "俏皮活泼"},
        {"id": "zh_female_mengyatou_uranus_bigtts",      "style": "萌丫头",     "use": "萌系少女"},
        {"id": "zh_female_tiexinnvsheng_uranus_bigtts",  "style": "贴心女声",   "use": "贴心温柔"},
        {"id": "zh_female_jitangmei_uranus_bigtts",      "style": "鸡汤妹妹",   "use": "暖心治愈"},
        {"id": "zh_female_kailangjiejie_uranus_bigtts",  "style": "开朗姐姐",   "use": "开朗大方"},
        {"id": "zh_female_qinqienv_uranus_bigtts",       "style": "亲切女声",   "use": "亲切自然"},
        {"id": "zh_female_zhixingnv_uranus_bigtts",      "style": "知性女声",   "use": "知性成熟"},
        {"id": "zh_female_liangsangmengzai_uranus_bigtts","style":"亮嗓萌仔",  "use": "清脆萌系"},
        {"id": "zh_female_roumeinvyou_uranus_bigtts",    "style": "柔美女友",   "use": "软萌女友"},
        {"id": "zh_female_wenjingmaomao_uranus_bigtts",  "style": "文静毛毛",   "use": "文静内向"},
        {"id": "zh_female_qingchezizi_uranus_bigtts",    "style": "清澈梓梓",   "use": "清澈少女"},
    ],
    "童声": [
        {"id": "zh_male_naiqimengwa_uranus_bigtts",     "style": "奶气萌娃",   "use": "小男孩、萌娃角色"},
        {"id": "zh_male_tiancaitongsheng_uranus_bigtts","style": "天才童声",   "use": "聪明小男孩"},
        {"id": "zh_male_liangsangmengzai_uranus_bigtts","style": "亮嗓萌仔",   "use": "清脆童声男"},
    ],
    "多语种": [
        {"id": "en_male_tim_uranus_bigtts",             "style": "Tim 美式男",  "use": "英文旁白、男性角色"},
        {"id": "en_female_dacey_uranus_bigtts",         "style": "Dacey 美式女", "use": "英文女性角色"},
        {"id": "en_female_stokie_uranus_bigtts",        "style": "Stokie 美式女","use": "英文女性角色"},
        {"id": "zh_female_yingyujiaoxue_uranus_bigtts", "style": "Tina 老师",    "use": "英语教学、中英双语"},
    ],
    "客服/助手": [
        {"id": "zh_female_kefunvsheng_uranus_bigtts",   "style": "暖阳女声",   "use": "客服、温和女声"},
        {"id": "zh_male_jieshuoxiaoming_uranus_bigtts", "style": "解说小明",   "use": "解说、播报男声"},
    ],
}

# Flattened list for backward compat (all speakers)
RECOMMENDED_SPEAKERS = []
for _cat_name, _voices in SPEAKER_CATEGORIES.items():
    for _v in _voices:
        RECOMMENDED_SPEAKERS.append({
            "id": _v["id"],
            "category": _cat_name,
            "style": _v["style"],
            "use": _v["use"],
        })


# ── API 调用 ──────────────────────────────────────────────

def synthesize(args):
    """调用豆包语音合成 V3 API，合成语音并保存。"""
    api_key = args.api_key or os.environ.get("DOUBAO_TTS_API_KEY")
    resource_id = args.resource_id or os.environ.get("DOUBAO_TTS_RESOURCE_ID", "seed-tts-2.0")
    app_id = args.app_id or os.environ.get("DOUBAO_TTS_APP_ID")
    access_key = args.access_key or os.environ.get("DOUBAO_TTS_ACCESS_KEY")

    if not api_key and not (app_id and access_key):
        print("Error: DOUBAO_TTS_API_KEY must be set (new console).", file=sys.stderr)
        print("  Or set DOUBAO_TTS_APP_ID + DOUBAO_TTS_ACCESS_KEY (old console).", file=sys.stderr)
        print("  Get credentials at https://console.volcengine.com/speech/new", file=sys.stderr)
        sys.exit(1)

    # Build request body
    body = {
        "user": {"uid": "openclaw-tts"},
        "namespace": "BidirectionalTTS",
        "req_params": {
            "text": args.text,
            "speaker": args.speaker,
            "audio_params": {
                "format": args.encoding,
                "sample_rate": args.rate,
            },
            "additions": "{}",
        },
    }

    # Optional params
    if args.emotion:
        body["req_params"]["audio_params"]["emotion"] = args.emotion
    if args.emotion_scale is not None:
        body["req_params"]["audio_params"]["emotion_scale"] = args.emotion_scale
    if args.speed != 0:
        body["req_params"]["audio_params"]["speech_rate"] = args.speed
    if args.loudness != 0:
        body["req_params"]["audio_params"]["loudness_rate"] = args.loudness
    if args.pitch != 0:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["post_process"] = {"pitch": args.pitch}
        body["req_params"]["additions"] = json.dumps(additions_obj)
    if args.encoding == "mp3":
        body["req_params"]["audio_params"]["bit_rate"] = args.bit_rate
    if args.model:
        body["req_params"]["model"] = args.model
    if args.context_texts:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["context_texts"] = args.context_texts
        body["req_params"]["additions"] = json.dumps(additions_obj)
    if args.explicit_language:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["explicit_language"] = args.explicit_language
        body["req_params"]["additions"] = json.dumps(additions_obj)
    if args.explicit_dialect:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["explicit_dialect"] = args.explicit_dialect
        body["req_params"]["additions"] = json.dumps(additions_obj)
    if args.silence_duration is not None:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["silence_duration"] = args.silence_duration
        body["req_params"]["additions"] = json.dumps(additions_obj)
    if args.enable_subtitle:
        body["req_params"]["audio_params"]["enable_subtitle"] = True
    if args.disable_markdown_filter:
        additions_obj = json.loads(body["req_params"]["additions"])
        additions_obj["disable_markdown_filter"] = True
        body["req_params"]["additions"] = json.dumps(additions_obj)

    data = json.dumps(body).encode("utf-8")

    # Build headers
    if api_key:
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
            "X-Api-Resource-Id": resource_id,
        }
    else:
        headers = {
            "Content-Type": "application/json",
            "X-Api-App-Id": app_id,
            "X-Api-Access-Key": access_key,
            "X-Api-Resource-Id": resource_id,
        }

    req_id = str(uuid.uuid4())
    headers["X-Api-Request-Id"] = req_id

    print(f"⏳ Synthesizing ({len(args.text)} chars, speaker={args.speaker}, emotion={args.emotion or 'auto'})...")

    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
            logid = resp.headers.get("X-Tt-Logid", "?")

            if status != 200:
                body_text = resp.read().decode("utf-8", errors="replace")
                print(f"Error: HTTP {status} — {body_text[:500]}", file=sys.stderr)
                sys.exit(1)

            # Read streaming JSON chunks
            audio_chunks = []
            sentence_count = 0

            for line in resp:
                line = line.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    # Non-chunked response (e.g., error)
                    continue

                event = chunk.get("event")
                payload = chunk.get("payload_msg")
                chunk_data = chunk.get("data") or (payload or {}).get("data", "")

                if chunk_data:
                    audio_chunks.append(base64.b64decode(chunk_data))

                if event == "TTSSentenceEnd":
                    sentence_count += 1

            if not audio_chunks:
                print("Error: no audio data received.", file=sys.stderr)
                print(f"  Log ID: {logid}", file=sys.stderr)
                sys.exit(1)

            audio_bytes = b"".join(audio_chunks)
            print(f"✅ Synthesis complete — {len(audio_bytes)} bytes, {sentence_count} sentences (log: {logid})")

    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} — {body_text[:500]}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Save
    import time
    ts = int(time.time() * 1000)
    filename = f"tts_{ts}.{args.encoding}"

    out_dir = args.download or "."
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    with open(path, "wb") as f:
        f.write(audio_bytes)
    print(f"📁 Saved: {path}")

    return 0


# ── 音色列表 ──────────────────────────────────────────────

def list_speakers(args):
    """打印音色列表，按类别分组。"""
    filter_cat = getattr(args, 'category', None)

    categories = SPEAKER_CATEGORIES
    if filter_cat:
        # Fuzzy match category name
        matched = [c for c in categories if filter_cat in c]
        if not matched:
            print(f"No category matching '{filter_cat}'.")
            print(f"Available: {', '.join(categories.keys())}")
            return 1
        categories = {c: categories[c] for c in matched}

    total = sum(len(v) for v in categories.values())
    print(f"豆包 TTS 2.0 音色列表 ({total} voices shown):\n")

    for cat_name, voices in categories.items():
        print(f"\n── {cat_name} ──")
        print(f"{'  Speaker ID':<52} {'Style':<16} {'Use Case'}")
        print("  " + "-" * 88)
        for v in voices:
            print(f"  {v['id']:<50} {v['style']:<16} {v['use']}")

    if not filter_cat:
        print(f"\n───")
        print(f"💡 使用 --category 过滤: 角色扮演 有声阅读 通用 童声 多语种 客服")
        print(f"📋 完整音色列表: https://www.volcengine.com/docs/6561/1257544")
        print(f"⚠️  1.0 音色将于 2026.06.30 下线，请迁移到 2.0 对应音色")
    return 0


# ── CLI ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="豆包语音合成 TTS V3 — 文字转语音")
    sub = parser.add_subparsers(dest="command")

    # synthesize
    p = sub.add_parser("synthesize", help="合成语音")
    p.add_argument("--text", required=True, help="合成文本")
    p.add_argument("--speaker", default="zh_female_shuangkuaisisi_uranus_bigtts",
                   help="发音人 ID")
    p.add_argument("--emotion", default=None,
                   help="情感: neutral/happy/sad/angry/surprised/fear/hate/excited/coldness/depressed/lovey-dovey/shy/comfort/tension/tender/storytelling/radio/magnetic/advertising/vocal-fry/ASMR/news/entertainment/dialect")
    p.add_argument("--emotion-scale", type=int, default=None,
                   help="情感强度 1~5（默认 4）")
    p.add_argument("--speed", type=int, default=0,
                   help="语速 -50~100（0=正常，100=2倍速，-50=0.5倍速）")
    p.add_argument("--loudness", type=int, default=0,
                   help="音量 -50~100（0=正常，100=2倍音量）")
    p.add_argument("--pitch", type=int, default=0,
                   help="音调 -12~12（半音）")
    p.add_argument("--rate", type=int, default=24000,
                   choices=[8000, 16000, 22050, 24000, 32000, 44100, 48000],
                   help="采样率")
    p.add_argument("--encoding", default="mp3",
                   choices=["mp3", "pcm", "ogg_opus"],
                   help="输出格式")
    p.add_argument("--bit-rate", type=int, default=128000,
                   help="MP3 比特率（默认 128k）")
    p.add_argument("--context-texts", nargs="*",
                   help="自然语言指令控制语气，用 [#指令] 前缀（例如: '#用悲伤的语气说'）")
    p.add_argument("--model", default=None,
                   help="模型版本: seed-tts-1.1（更优音质）/ seed-tts-2.0-expressive / seed-tts-2.0-standard（复刻音色）")
    p.add_argument("--explicit-language", default=None,
                   help="指定语种: zh-cn/en/ja/es-mx/id/pt-br（多语种场景用）")
    p.add_argument("--explicit-dialect", default=None,
                   choices=["dongbei", "shaanxi", "sichuan"],
                   help="指定方言（仅 Vivi 音色: zh_female_vv_uranus_bigtts）")
    p.add_argument("--silence-duration", type=int, default=None,
                   help="句尾增加静音时长 0~30000ms")
    p.add_argument("--enable-subtitle", action="store_true",
                   help="返回词级时间戳字幕（仅 TTS 2.0）")
    p.add_argument("--disable-markdown-filter", action="store_true",
                   help="不解析 Markdown 语法（默认会过滤 ** 等标记）")
    p.add_argument("-d", "--download", help="输出目录")
    p.add_argument("--api-key", help="API Key（新版控制台）")
    p.add_argument("--resource-id", help="资源 ID")
    p.add_argument("--app-id", help="APP ID（旧版控制台）")
    p.add_argument("--access-key", help="Access Token（旧版控制台）")
    p.set_defaults(func=synthesize)

    # voices
    pv = sub.add_parser("voices", help="列出音色列表")
    pv.add_argument("--category", "-c", default=None,
                    help="按类别过滤（模糊匹配，如: 角色扮演、有声阅读、多语种、方言、童声、助手）")
    pv.set_defaults(func=list_speakers)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
