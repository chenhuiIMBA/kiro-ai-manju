# 阶段 11：合成成片

> 工具：FFmpeg（crossfade 拼接）
> ⚠️ 4 段 → 3 次 crossfade

## 前置条件

- `05-videos/ep01/seg1.mp4` + `seg2.mp4` + `seg3.mp4` + `seg4.mp4` 均已确认

## 流程

### 步骤 1：段间色温一致性检查（🆕 必做）

> ⚠️ 四段视频是独立 Seedance 任务，色温/亮度/对比度可能有差异。crossfade 能掩盖构图跳跃，但掩盖不了色温跳变——两段不同色温的画面叠化 = 灰泥色 0.5 秒。合成前必须先检查。

截取每段首帧，横向拼接对比：

```bash
# 截取每段首帧（跳过前 0.3s 不稳定区域）
ffmpeg -i ./05-videos/ep01/seg1.mp4 -ss 0.5 -vframes 1 ./05-videos/ep01/seg1_first.jpg
ffmpeg -i ./05-videos/ep01/seg2.mp4 -ss 0.5 -vframes 1 ./05-videos/ep01/seg2_first.jpg
ffmpeg -i ./05-videos/ep01/seg3.mp4 -ss 0.5 -vframes 1 ./05-videos/ep01/seg3_first.jpg
ffmpeg -i ./05-videos/ep01/seg4.mp4 -ss 0.5 -vframes 1 ./05-videos/ep01/seg4_first.jpg

# 横向拼接对比
ffmpeg -i ./05-videos/ep01/seg1_first.jpg -i ./05-videos/ep01/seg2_first.jpg \
       -i ./05-videos/ep01/seg3_first.jpg -i ./05-videos/ep01/seg4_first.jpg \
  -filter_complex "[0][1][2][3]hstack=inputs=4" \
  ./05-videos/ep01/color_comparison.jpg
```

目测检查 `color_comparison.jpg`：

- [ ] 四段首帧色温方向一致（同为暖调或同为冷调，不出现暖冷交替）
- [ ] 亮度无明显跳变（不出现一段明显偏亮或偏暗）
- [ ] 肤色一致（角色面部不出现一段偏黄一段偏红）

**如果差异可接受** → 直接进入步骤 2 合成。

**如果色温/亮度差异明显** → 进入步骤 1.5 色彩校正。

### 步骤 1.5：色彩校正（可选，仅色温差异明显时执行）

以段 1 为基准（用户最先看到，视觉印象最强），对偏差段做轻微校正：

```bash
# 示例：段2 偏冷，需要加暖
ffmpeg -i ./05-videos/ep01/seg2.mp4 \
  -vf "colorbalance=rs=0.05:gs=0.02:bs=-0.05" \
  ./05-videos/ep01/seg2_corrected.mp4

# 示例：段3 偏暗，需要提亮
ffmpeg -i ./05-videos/ep01/seg3.mp4 \
  -vf "eq=brightness=0.03:contrast=1.02" \
  ./05-videos/ep01/seg3_corrected.mp4
```

常用校正参数：

| 问题 | 滤镜 | 参数方向 |
|------|------|---------|
| 偏冷（蓝） | `colorbalance` | `rs=+0.03~0.08, bs=-0.03~0.08`（加红减蓝） |
| 偏暖（黄） | `colorbalance` | `rs=-0.03~0.08, bs=+0.03~0.08`（减红加蓝） |
| 偏暗 | `eq` | `brightness=+0.02~0.05` |
| 偏亮 | `eq` | `brightness=-0.02~0.05` |
| 对比度不足 | `eq` | `contrast=1.02~1.10` |

> ⚠️ 参数值保持微调（0.02~0.08 范围），过度校正比不校正更糟。校正后重新截首帧对比确认。

校正后的文件用于后续合成，原始文件保留不删除。

### 步骤 2：分步合成（推荐）

> ⚠️ **必须分步合成**。四段一次性用 concat + xfade 混合 filter_complex 会触发 FFmpeg timebase 不匹配错误（concat 输出的 timebase 与 xfade 输入不兼容）。分步两两拼接虽然多一次编码，但稳定可靠。

按 `05-videos/ep{NN}/assets.md` 中的衔接规划表，逐步拼接。以下以"段1→段2 黑场fade，段2→段3 crossfade 0.3s，段3→段4 crossfade 0.5s"为例：

```bash
# 步骤 2a：段1 + 段2（黑场 fade）
ffmpeg -y \
  -i ./05-videos/ep01/seg1.mp4 \
  -i ./05-videos/ep01/seg2.mp4 \
  -filter_complex "[0:v]fade=t=out:st=14.5:d=0.5[v0];[1:v]fade=t=in:st=0:d=0.5[v1];[v0][v1]concat=n=2:v=1:a=0[vout];[0:a][1:a]concat=n=2:v=0:a=1[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  ./05-videos/ep01/_tmp_seg12.mp4

# 步骤 2b：(段1+段2) + 段3（crossfade 0.3s）
# offset = 步骤2a输出时长 - crossfade时长（查 ffprobe 确认实际时长）
ffmpeg -y \
  -i ./05-videos/ep01/_tmp_seg12.mp4 \
  -i ./05-videos/ep01/seg3.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.3:offset={seg12时长-0.3}[vout];[0:a][1:a]acrossfade=d=0.3[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  ./05-videos/ep01/_tmp_seg123.mp4

# 步骤 2c：(段1+段2+段3) + 段4（crossfade 0.5s）
ffmpeg -y \
  -i ./05-videos/ep01/_tmp_seg123.mp4 \
  -i ./05-videos/ep01/seg4.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset={seg123时长-0.5}[vout];[0:a][1:a]acrossfade=d=0.5[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  ./06-output/ep01-final.mp4

# 清理临时文件
rm ./05-videos/ep01/_tmp_seg12.mp4 ./05-videos/ep01/_tmp_seg123.mp4
```

> 每步用 `ffprobe -v error -show_entries format=duration -of csv=p=0` 查中间文件时长，计算下一步的 offset。
> 衔接方式（黑场fade/crossfade/硬切）和时长从 assets.md 衔接规划表读取，不同集可能不同。

### 步骤 2（备选）：硬切拼接

如果所有段间衔接都是硬切（极少见）：

```bash
ffmpeg -i ./05-videos/ep01/seg1.mp4 -i ./05-videos/ep01/seg2.mp4 \
       -i ./05-videos/ep01/seg3.mp4 -i ./05-videos/ep01/seg4.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset medium -crf 18 \
  ./06-output/ep01-final.mp4
```

### 步骤 3：字幕错别字局部修复（🆕 按需执行）

> ⚠️ Seedance 内置字幕偶尔会出现形近字替换（如"各→何"）。字幕指令保留在 prompt 中以保证语音同步，成片检查时发现错别字用 FFmpeg drawtext 局部覆盖修复。

**修复流程**：

1. 成片检查时记录错别字位置：哪一段、哪句台词、出现在成片的第几秒
2. 用 FFmpeg drawtext 在错别字出现的时间段叠加正确文字覆盖

```bash
# 示例：成片 33-36 秒处"各走何路"→"各走各路"
ffmpeg -y \
  -i ./06-output/ep01-final.mp4 \
  -vf "drawtext=text='各走各路':fontfile=/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc:fontsize=36:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=h-80:enable='between(t,33,36)'" \
  -c:v libx264 -preset medium -crf 18 -c:a copy \
  ./06-output/ep01-final-fixed.mp4

# 确认修复后替换（遵循资产安全规则：先备份再替换）
cp ./06-output/ep01-final.mp4 ./06-output/_backup/ep01-final.mp4.bak
mv ./06-output/ep01-final-fixed.mp4 ./06-output/ep01-final.mp4
```

> 如果多处错别字，可以链式叠加多个 drawtext 滤镜，用逗号分隔。
> 字体、字号、位置需要与 Seedance 原始字幕样式尽量匹配。

**无错别字时跳过此步骤。**

## 产出

| 文件 | 说明 |
|------|------|
| `06-output/ep01-final.mp4` | 第 1 集成品（~60s） |

## 验收

- [ ] 段间色温一致性检查已执行（color_comparison.jpg 已生成并目测通过）（🆕）
- [ ] 如有色彩校正，校正后重新对比确认通过（🆕）
- [ ] 3 处段间拼接无明显视觉跳跃
- [ ] 音频无断裂或音量突变
- [ ] 总时长约 60s

## 完成后

→ `stages/12-.*.md`
将 `STATE.md` 中 `当前阶段` 更新为 `12-.*`，勾选 11。
