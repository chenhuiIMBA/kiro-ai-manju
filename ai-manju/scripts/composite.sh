#!/bin/bash
# 混合转场合成脚本（零裁切版）
#
# 用法:
#   bash composite.sh <项目目录> <集号> <衔接模式>
#
# 衔接模式: 三个字符表示三个衔接点（seg1→seg2, seg2→seg3, seg3→seg4）
#   H = 硬切（concat，无过渡）
#   F = fade（淡入淡出叠化）
#   B = fadeblack（渐黑过渡）
#   W = fadewhite（渐白过渡）
#   L = smoothleft（柔滑左移，进入回忆）
#   R = smoothright（柔滑右移，回到现实）
#   D = wipedown（向下擦除，竖屏空间跳转）
#   U = wipeup（向上擦除）
#   C = circleclose（圆形收缩，聚焦关键物体）
#   O = circleopen（圆形展开，新场景揭示）
#   A = radial（径向擦除，时间流逝）
#   S = slideleft（左滑，平行叙事）
#
# 可选参数:
#   -d <时长>  转场时长，默认 0.3（秒），对所有 xfade 衔接点生效
#   -b <时长>  黑场/白场时长，默认 0.5（秒），对 B/W 类型生效
#
# 示例:
#   bash composite.sh projects/test-drama 06 HHB
#   bash composite.sh projects/test-drama 07 HWB -d 0.4 -b 0.6
#
# 零裁切原则：不截取原片任何内容。

set -e

# ── 参数解析 ──────────────────────────────────────────

PROJECT=""
EP=""
MODE=""
XFADE_DUR="0.3"
BLACK_DUR="0.5"

while [ $# -gt 0 ]; do
  case "$1" in
    -d) XFADE_DUR="$2"; shift 2 ;;
    -b) BLACK_DUR="$2"; shift 2 ;;
    *)
      if [ -z "$PROJECT" ]; then PROJECT="$1"
      elif [ -z "$EP" ]; then EP="$1"
      elif [ -z "$MODE" ]; then MODE="$1"
      fi
      shift ;;
  esac
done

if [ -z "$PROJECT" ] || [ -z "$EP" ] || [ -z "$MODE" ]; then
  echo "用法: bash $0 <项目目录> <集号> <衔接模式> [-d 转场时长] [-b 黑场时长]"
  echo "衔接模式: H=硬切 F=fade B=fadeblack W=fadewhite L=smoothleft R=smoothright"
  echo "          D=wipedown U=wipeup C=circleclose O=circleopen A=radial S=slideleft"
  echo "示例: bash $0 projects/test-drama 06 HHB"
  exit 1
fi

if [ ${#MODE} -ne 3 ]; then
  echo "❌ 衔接模式必须是3个字符，当前: '$MODE' (${#MODE}个字符)"
  exit 1
fi

VDIR="$PROJECT/05-videos/ep${EP}"
ODIR="$PROJECT/06-output"
TMP="$ODIR/_tmp_ep${EP}"

# 检查输入文件
for i in 1 2 3 4; do
  if [ ! -f "$VDIR/seg${i}.mp4" ]; then
    echo "❌ 未找到: $VDIR/seg${i}.mp4"
    exit 1
  fi
done

mkdir -p "$TMP" "$ODIR"

# ── 工具函数 ──────────────────────────────────────────

# 字符→xfade transition 名称
char_to_transition() {
  case "$1" in
    H) echo "concat" ;;
    F) echo "fade" ;;
    B) echo "fadeblack" ;;
    W) echo "fadewhite" ;;
    L) echo "smoothleft" ;;
    R) echo "smoothright" ;;
    D) echo "wipedown" ;;
    U) echo "wipeup" ;;
    C) echo "circleclose" ;;
    O) echo "circleopen" ;;
    A) echo "radial" ;;
    S) echo "slideleft" ;;
    *) echo "unknown"; return 1 ;;
  esac
}

# 获取视频时长（秒，浮点数）
get_duration() {
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"
}

# ── 判断合成方案 ──────────────────────────────────────

T1="${MODE:0:1}"
T2="${MODE:1:1}"
T3="${MODE:2:1}"

# 检查是否所有衔接点都是硬切或黑场（可用 concat demuxer 的简单方案）
ALL_SIMPLE=true
for T in "$T1" "$T2" "$T3"; do
  if [ "$T" != "H" ] && [ "$T" != "B" ]; then
    ALL_SIMPLE=false
    break
  fi
done

# ── 方案 A：concat demuxer（纯硬切+黑场） ─────────────

if $ALL_SIMPLE; then
  echo "📋 方案A: concat demuxer (硬切+黑场)"
  echo "   衔接: $(char_to_transition $T1) / $(char_to_transition $T2) / $(char_to_transition $T3)"

  # 确保黑场文件存在
  BLACK="$TMP/black.mp4"
  if [ "$T1" = "B" ] || [ "$T2" = "B" ] || [ "$T3" = "B" ]; then
    echo "   生成 ${BLACK_DUR}s 黑场..."
    ffmpeg -f lavfi -i "color=c=black:s=720x1280:r=24:d=${BLACK_DUR}" \
           -f lavfi -i "anullsrc=r=44100:cl=stereo" \
           -t "$BLACK_DUR" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 128k \
           -y "$BLACK" 2>/dev/null
  fi

  # 重编码四段（确保参数一致，concat demuxer 要求）
  echo "   重编码四段..."
  for i in 1 2 3 4; do
    ffmpeg -i "$VDIR/seg${i}.mp4" \
      -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 128k \
      -y "$TMP/s${i}.mp4" 2>/dev/null
  done

  # 生成 concat 列表
  CONCAT="$TMP/concat.txt"
  ABS_TMP="$(cd "$TMP" && pwd)"

  echo "file '${ABS_TMP}/s1.mp4'" > "$CONCAT"

  if [ "$T1" = "B" ]; then echo "file '${ABS_TMP}/black.mp4'" >> "$CONCAT"; fi
  echo "file '${ABS_TMP}/s2.mp4'" >> "$CONCAT"

  if [ "$T2" = "B" ]; then echo "file '${ABS_TMP}/black.mp4'" >> "$CONCAT"; fi
  echo "file '${ABS_TMP}/s3.mp4'" >> "$CONCAT"

  if [ "$T3" = "B" ]; then echo "file '${ABS_TMP}/black.mp4'" >> "$CONCAT"; fi
  echo "file '${ABS_TMP}/s4.mp4'" >> "$CONCAT"

  echo "   合成..."
  ffmpeg -f concat -safe 0 -i "$CONCAT" \
    -c:v libx264 -preset medium -crf 18 \
    -c:a aac -b:a 128k \
    -y "$ODIR/ep${EP}-final.mp4" 2>/dev/null

# ── 方案 B：filter_complex（xfade 转场） ─────────────

else
  echo "📋 方案B: filter_complex (xfade 转场)"
  echo "   衔接: $(char_to_transition $T1) / $(char_to_transition $T2) / $(char_to_transition $T3)"
  echo "   转场时长: ${XFADE_DUR}s, 黑场时长: ${BLACK_DUR}s"

  # 获取每段时长
  D1=$(get_duration "$VDIR/seg1.mp4")
  D2=$(get_duration "$VDIR/seg2.mp4")
  D3=$(get_duration "$VDIR/seg3.mp4")
  D4=$(get_duration "$VDIR/seg4.mp4")
  echo "   段时长: ${D1}s / ${D2}s / ${D3}s / ${D4}s"

  # 构建 filter_complex
  # 策略：
  # - 视频：所有衔接点统一用 xfade，硬切用 fade:duration=0.04（约1帧，视觉等效硬切）
  # - 音频：直接 concat 拼接（不做 acrossfade，段间对白独立，不需要音频过渡）
  # 这样避免 concat 和 xfade 混用时 timebase 不匹配，以及 acrossfade 链式处理丢帧的问题

  VFILTER=""
  CUMULATIVE="0"

  # 辅助函数：获取某个衔接点的实际 xfade duration
  get_xfade_dur() {
    local trans="$1"
    if [ "$trans" = "concat" ]; then
      echo "0.04"  # 硬切用约1帧的极短 fade 模拟
    else
      echo "$XFADE_DUR"
    fi
  }

  # ── 衔接1: seg1 + seg2 ──
  TRANS1=$(char_to_transition "$T1")
  XDUR1=$(get_xfade_dur "$TRANS1")
  XNAME1=$( [ "$TRANS1" = "concat" ] && echo "fade" || echo "$TRANS1" )
  OFFSET1=$(echo "$D1 - $XDUR1" | bc -l)
  VFILTER="[0:v][1:v]xfade=transition=${XNAME1}:duration=${XDUR1}:offset=${OFFSET1}[v01];"
  CUMULATIVE=$(echo "$D1 + $D2 - $XDUR1" | bc -l)

  # ── 衔接2: (seg1+seg2) + seg3 ──
  TRANS2=$(char_to_transition "$T2")
  XDUR2=$(get_xfade_dur "$TRANS2")
  XNAME2=$( [ "$TRANS2" = "concat" ] && echo "fade" || echo "$TRANS2" )
  OFFSET2=$(echo "$CUMULATIVE - $XDUR2" | bc -l)
  VFILTER="${VFILTER} [v01][2:v]xfade=transition=${XNAME2}:duration=${XDUR2}:offset=${OFFSET2}[v012];"
  CUMULATIVE=$(echo "$CUMULATIVE + $D3 - $XDUR2" | bc -l)

  # ── 衔接3: (seg1+seg2+seg3) + seg4 ──
  TRANS3=$(char_to_transition "$T3")
  XDUR3=$(get_xfade_dur "$TRANS3")
  XNAME3=$( [ "$TRANS3" = "concat" ] && echo "fade" || echo "$TRANS3" )
  OFFSET3=$(echo "$CUMULATIVE - $XDUR3" | bc -l)
  VFILTER="${VFILTER} [v012][3:v]xfade=transition=${XNAME3}:duration=${XDUR3}:offset=${OFFSET3}[vout];"

  # 音频直接 concat（不做 crossfade）
  FILTER="${VFILTER} [0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[aout]"

  echo "   合成..."
  ffmpeg -i "$VDIR/seg1.mp4" -i "$VDIR/seg2.mp4" \
         -i "$VDIR/seg3.mp4" -i "$VDIR/seg4.mp4" \
    -filter_complex "$FILTER" \
    -map "[vout]" -map "[aout]" \
    -c:v libx264 -preset medium -crf 18 \
    -c:a aac -b:a 128k \
    -y "$ODIR/ep${EP}-final.mp4" 2>/dev/null
fi

# ── 清理 + 输出 ──────────────────────────────────────

rm -rf "$TMP"

DUR=$(get_duration "$ODIR/ep${EP}-final.mp4")
echo "✅ EP${EP} 合成完成: $ODIR/ep${EP}-final.mp4 (${DUR}s)"
echo "   衔接模式: $MODE ($(char_to_transition $T1) / $(char_to_transition $T2) / $(char_to_transition $T3))"
