#!/bin/bash
# 重新生成单段视频脚本
#
# 从 assets.md 中读取指定段的完整参数，重新提交 Seedance，
# 等待完成后下载，备份旧文件，替换为新文件。
#
# 用法:
#   bash regen_seg.sh <项目目录> <集号> <段号> [选项]
#
# 选项:
#   -s <seed>          指定 seed 值（不传则随机）
#   -S                 自动使用上一次的 seed（从 task_id 查询）
#   --seedance <路径>  seedance.py 路径（默认 video-generation/scripts/seedance.py）
#
# 示例:
#   bash regen_seg.sh projects/test-drama 06 3              # 随机 seed
#   bash regen_seg.sh projects/test-drama 06 3 -S           # 复用上一次 seed
#   bash regen_seg.sh projects/test-drama 06 3 -s 12345     # 指定 seed
#
# 流程:
#   1. 从 assets.md 解析该段的 prompt、ref-images、audio 等参数
#   2. 备份旧的 seg{N}.mp4 和 lastframe_seg{N}.png 到 _backup/
#   3. 提交 Seedance 任务（可选传入 seed）
#   4. 等待完成并下载
#   5. 重命名为 seg{N}.mp4 和 lastframe_seg{N}.png
#   6. 更新 assets.md 中的 task_id 和 seed
#
# 前置条件:
#   - ARK_API_KEY 环境变量已设置
#   - assets.md 中有该段的完整参数块

set -e

# ── 参数解析 ──────────────────────────────────────────

PROJECT=""
EP=""
SEG=""
SEEDANCE="video-generation/scripts/seedance.py"
SEED_VALUE=""
USE_PREV_SEED=false

while [ $# -gt 0 ]; do
  case "$1" in
    -s) SEED_VALUE="$2"; shift 2 ;;
    -S) USE_PREV_SEED=true; shift ;;
    --seedance) SEEDANCE="$2"; shift 2 ;;
    *)
      if [ -z "$PROJECT" ]; then PROJECT="$1"
      elif [ -z "$EP" ]; then EP="$1"
      elif [ -z "$SEG" ]; then SEG="$1"
      fi
      shift ;;
  esac
done

if [ -z "$PROJECT" ] || [ -z "$EP" ] || [ -z "$SEG" ]; then
  echo "用法: bash $0 <项目目录> <集号> <段号> [选项]"
  echo "选项: -s <seed>  指定seed  |  -S  复用上一次seed  |  --seedance <路径>"
  echo "示例: bash $0 projects/test-drama 06 3 -S"
  exit 1
fi

VDIR="$PROJECT/05-videos/ep${EP}"
ASSETS="$VDIR/assets.md"
BACKUP="$VDIR/_backup"

if [ ! -f "$ASSETS" ]; then
  echo "❌ 未找到: $ASSETS"
  exit 1
fi

if [ ! -f "$SEEDANCE" ]; then
  echo "❌ 未找到 seedance.py: $SEEDANCE"
  exit 1
fi

echo "🔄 重新生成 EP${EP} seg${SEG}"
echo "   assets: $ASSETS"

# ── 查询上一次 seed（如果 -S 标志开启）────────────────

if $USE_PREV_SEED && [ -z "$SEED_VALUE" ]; then
  # 从 assets.md 中提取上一次的 task_id
  PREV_TASK_ID=$(python3 -c "
import re
with open('$ASSETS', 'r') as f:
    content = f.read()
m = re.search(r'\| seg${SEG}\s*\|[^|]*\|\s*(\S+)\s*\|', content)
if m:
    print(m.group(1))
" 2>/dev/null)

  if [ -n "$PREV_TASK_ID" ] && [ "$PREV_TASK_ID" != "—" ]; then
    echo "   查询上一次 seed (task: $PREV_TASK_ID)..."
    PREV_SEED=$(python3 "$SEEDANCE" status "$PREV_TASK_ID" 2>/dev/null | python3 -c "
import sys, json, re
text = sys.stdin.read()
# 尝试从 JSON 输出中提取 seed
m = re.search(r'\"seed\"\s*:\s*(\d+)', text)
if m:
    print(m.group(1))
" 2>/dev/null)

    if [ -n "$PREV_SEED" ]; then
      SEED_VALUE="$PREV_SEED"
      echo "   上一次 seed: $SEED_VALUE（将复用）"
    else
      echo "   ⚠️ 无法查询上一次 seed，将使用随机 seed"
    fi
  else
    echo "   ⚠️ 未找到上一次 task_id，将使用随机 seed"
  fi
fi

if [ -n "$SEED_VALUE" ]; then
  echo "   seed: $SEED_VALUE"
else
  echo "   seed: 随机"
fi

# ── 解析 assets.md ────────────────────────────────────

# 提取该段的 Prompt 块（在 ```...``` 之间）
# 查找模式：## 段{N} 精简版 Prompt → 找到 ### Prompt → 提取 ``` 块
PROMPT=$(python3 -c "
import re, sys

with open('$ASSETS', 'r') as f:
    content = f.read()

# 找到该段的区域
seg_pattern = r'## 段${SEG} 精简版 Prompt.*?(?=## 段\d|## 段级进度|\Z)'
seg_match = re.search(seg_pattern, content, re.DOTALL)
if not seg_match:
    print('ERROR: 未找到段${SEG}的prompt区域', file=sys.stderr)
    sys.exit(1)

seg_text = seg_match.group()

# 提取 ### Prompt 下的 \`\`\` 块
prompt_pattern = r'### Prompt\s*\n+\`\`\`\s*\n(.*?)\n\`\`\`'
prompt_match = re.search(prompt_pattern, seg_text, re.DOTALL)
if not prompt_match:
    print('ERROR: 未找到段${SEG}的prompt内容', file=sys.stderr)
    sys.exit(1)

print(prompt_match.group(1).strip())
")

if [ -z "$PROMPT" ]; then
  echo "❌ 无法从 assets.md 解析段${SEG}的 prompt"
  exit 1
fi

echo "   prompt: $(echo "$PROMPT" | head -1)..."

# 提取 ref-images 文件列表
REF_IMAGES=$(python3 -c "
import re, sys

with open('$ASSETS', 'r') as f:
    content = f.read()

seg_pattern = r'## 段${SEG} 精简版 Prompt.*?(?=## 段\d|## 段级进度|\Z)'
seg_match = re.search(seg_pattern, content, re.DOTALL)
if not seg_match:
    sys.exit(0)

seg_text = seg_match.group()

# 提取完整参数块中的 ref-images 路径
# 格式: 图片N: 路径
ref_pattern = r'图片\d+:\s*(.+)'
refs = re.findall(ref_pattern, seg_text)

# 将相对路径转为从项目目录开始的路径
for ref in refs:
    ref = ref.strip()
    # 路径可能是 03-storyboard/... 或 04-human-design/...
    print('$PROJECT/' + ref)
")

# 提取 audio 文件列表
AUDIO_FILES=$(python3 -c "
import re, sys

with open('$ASSETS', 'r') as f:
    content = f.read()

seg_pattern = r'## 段${SEG} 精简版 Prompt.*?(?=## 段\d|## 段级进度|\Z)'
seg_match = re.search(seg_pattern, content, re.DOTALL)
if not seg_match:
    sys.exit(0)

seg_text = seg_match.group()

# 提取 audio 路径
# 格式: 音频N: 路径
audio_pattern = r'音频\d+:\s*(.+)'
audios = re.findall(audio_pattern, seg_text)

for a in audios:
    a = a.strip()
    print('$PROJECT/' + a)
")

echo "   ref-images: $(echo "$REF_IMAGES" | wc -l) 张"
echo "   audio: $(echo "$AUDIO_FILES" | wc -l) 条"

# ── 备份旧文件 ────────────────────────────────────────

mkdir -p "$BACKUP"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -f "$VDIR/seg${SEG}.mp4" ]; then
  cp "$VDIR/seg${SEG}.mp4" "$BACKUP/seg${SEG}_${TIMESTAMP}.mp4"
  echo "   备份: seg${SEG}.mp4 → _backup/seg${SEG}_${TIMESTAMP}.mp4"
fi

if [ -f "$VDIR/lastframe_seg${SEG}.png" ]; then
  cp "$VDIR/lastframe_seg${SEG}.png" "$BACKUP/lastframe_seg${SEG}_${TIMESTAMP}.png"
  echo "   备份: lastframe_seg${SEG}.png → _backup/"
fi

# ── 构建 seedance 命令 ────────────────────────────────

CMD="python3 $SEEDANCE create"
CMD="$CMD --prompt \"$PROMPT\""

# 添加 ref-images
if [ -n "$REF_IMAGES" ]; then
  REF_ARGS=""
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    if [ ! -f "$ref" ]; then
      echo "⚠️  ref-image 不存在: $ref"
    else
      REF_ARGS="$REF_ARGS $ref"
    fi
  done <<< "$REF_IMAGES"
  if [ -n "$REF_ARGS" ]; then
    CMD="$CMD --ref-images$REF_ARGS"
  fi
fi

# 添加 audio
if [ -n "$AUDIO_FILES" ]; then
  AUDIO_ARGS=""
  while IFS= read -r aud; do
    [ -z "$aud" ] && continue
    if [ ! -f "$aud" ]; then
      echo "⚠️  audio 不存在: $aud"
    else
      AUDIO_ARGS="$AUDIO_ARGS $aud"
    fi
  done <<< "$AUDIO_FILES"
  if [ -n "$AUDIO_ARGS" ]; then
    CMD="$CMD --audio$AUDIO_ARGS"
  fi
fi

CMD="$CMD --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true"

# 添加 seed（如果指定了）
if [ -n "$SEED_VALUE" ]; then
  CMD="$CMD --seed $SEED_VALUE"
fi

echo ""
echo "📤 提交 Seedance 任务..."
echo "   命令: $CMD"
echo ""

# ── 提交并等待 ────────────────────────────────────────

# 提交任务，提取 task_id
TASK_OUTPUT=$(eval "$CMD" 2>&1)
echo "$TASK_OUTPUT"

TASK_ID=$(echo "$TASK_OUTPUT" | grep -oP 'ID:\s*\K\S+' | head -1)
if [ -z "$TASK_ID" ]; then
  TASK_ID=$(echo "$TASK_OUTPUT" | grep -oP '"id":\s*"\K[^"]+' | head -1)
fi

if [ -z "$TASK_ID" ]; then
  echo "❌ 无法提取 task_id"
  echo "$TASK_OUTPUT"
  exit 1
fi

echo ""
echo "⏳ 等待任务完成: $TASK_ID"
python3 "$SEEDANCE" wait "$TASK_ID" --download "$VDIR/"

# ── 重命名下载文件 ────────────────────────────────────

# seedance.py 下载的文件名格式: seedance_{task_id}_{timestamp}.mp4
NEW_VIDEO=$(ls -t "$VDIR"/seedance_${TASK_ID}_*.mp4 2>/dev/null | head -1)
NEW_LASTFRAME=$(ls -t "$VDIR"/lastframe_${TASK_ID}.png 2>/dev/null | head -1)

if [ -n "$NEW_VIDEO" ]; then
  mv "$NEW_VIDEO" "$VDIR/seg${SEG}.mp4"
  echo "✅ seg${SEG}.mp4 已更新"
else
  echo "⚠️  未找到下载的视频文件"
fi

if [ -n "$NEW_LASTFRAME" ]; then
  mv "$NEW_LASTFRAME" "$VDIR/lastframe_seg${SEG}.png"
  echo "✅ lastframe_seg${SEG}.png 已更新"
else
  echo "⚠️  未找到尾帧文件"
fi

# ── 更新 assets.md 中的 task_id 和 seed ─────────────

# 查询新任务的 seed
NEW_SEED=$(python3 "$SEEDANCE" status "$TASK_ID" 2>/dev/null | python3 -c "
import sys, re
text = sys.stdin.read()
m = re.search(r'\"seed\"\s*:\s*(\d+)', text)
if m:
    print(m.group(1))
" 2>/dev/null)

python3 -c "
import re

with open('$ASSETS', 'r') as f:
    content = f.read()

# 更新段级进度追踪表中的 task_id
pattern = r'(\| seg${SEG}\s*\|[^|]*\|)\s*\S+\s*(\|.*)'
replacement = r'\1 ${TASK_ID} \2'
new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open('$ASSETS', 'w') as f:
        f.write(new_content)
    print('   assets.md task_id 已更新')
else:
    print('   ⚠️ assets.md task_id 未更新（格式可能不匹配）')
"

echo ""
echo "🎬 重新生成完成: EP${EP} seg${SEG}"
echo "   新 task_id: $TASK_ID"
if [ -n "$NEW_SEED" ]; then
  echo "   新 seed: $NEW_SEED"
fi
echo "   旧文件备份在: $BACKUP/"
echo ""
echo "下一步: 重新合成成片"
echo "   bash ai-manju/scripts/composite.sh $PROJECT $EP <衔接模式>"
