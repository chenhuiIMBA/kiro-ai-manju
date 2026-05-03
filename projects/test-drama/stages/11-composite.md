# 阶段 11：合成成片

> 工具：FFmpeg
> ⚠️ **零裁切原则**：不截取原片任何内容。转场库详见 `references/workflow-detail.md` §8.1。

## 前置条件

- `05-videos/ep{NN}/seg1.mp4` + `seg2.mp4` + `seg3.mp4` + `seg4.mp4` 均已确认
- `05-videos/ep{NN}/assets.md` 中的段间衔接规划表已填写（含转场方式和情绪意图）

## 流程

### 步骤 1：段间色温一致性检查（必做）

> ⚠️ 四段视频是独立 Seedance 任务，色温/亮度/对比度可能有差异。转场能掩盖构图跳跃，但掩盖不了色温跳变。合成前必须先检查。

截取每段首帧，横向拼接对比：

```bash
# 截取每段首帧（跳过前 0.5s 不稳定区域）
ffmpeg -i ./05-videos/ep{NN}/seg1.mp4 -ss 0.5 -vframes 1 ./05-videos/ep{NN}/seg1_first.jpg
ffmpeg -i ./05-videos/ep{NN}/seg2.mp4 -ss 0.5 -vframes 1 ./05-videos/ep{NN}/seg2_first.jpg
ffmpeg -i ./05-videos/ep{NN}/seg3.mp4 -ss 0.5 -vframes 1 ./05-videos/ep{NN}/seg3_first.jpg
ffmpeg -i ./05-videos/ep{NN}/seg4.mp4 -ss 0.5 -vframes 1 ./05-videos/ep{NN}/seg4_first.jpg

# 横向拼接对比
ffmpeg -i ./05-videos/ep{NN}/seg1_first.jpg -i ./05-videos/ep{NN}/seg2_first.jpg \
       -i ./05-videos/ep{NN}/seg3_first.jpg -i ./05-videos/ep{NN}/seg4_first.jpg \
  -filter_complex "[0][1][2][3]hstack=inputs=4" \
  ./05-videos/ep{NN}/color_comparison.jpg
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
ffmpeg -i ./05-videos/ep{NN}/seg2.mp4 \
  -vf "colorbalance=rs=0.05:gs=0.02:bs=-0.05" \
  ./05-videos/ep{NN}/seg2_corrected.mp4

# 示例：段3 偏暗，需要提亮
ffmpeg -i ./05-videos/ep{NN}/seg3.mp4 \
  -vf "eq=brightness=0.03:contrast=1.02" \
  ./05-videos/ep{NN}/seg3_corrected.mp4
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

### 步骤 2：按衔接规划表合成

从 `05-videos/ep{NN}/assets.md` 读取段间衔接规划表，根据转场方式选择合成方案。

#### 方案 A：纯硬切 + 黑场插入（concat demuxer）

适用于衔接方式只有硬切和黑场的情况。原片不裁切。

```bash
# 生成黑场（按需，匹配源视频参数）
ffmpeg -f lavfi -i "color=c=black:s=720x1280:r=24:d=0.5" \
       -f lavfi -i "anullsrc=r=44100:cl=stereo" \
       -t 0.5 -c:v libx264 -c:a aac -shortest black_0.5s.mp4

# 创建 concat 列表（原片不裁切）
echo "file 'seg1.mp4'" > concat.txt
echo "file 'seg2.mp4'" >> concat.txt
echo "file 'black_0.5s.mp4'" >> concat.txt
echo "file 'seg3.mp4'" >> concat.txt
echo "file 'seg4.mp4'" >> concat.txt

ffmpeg -f concat -safe 0 -i concat.txt \
  -c:v libx264 -preset medium -crf 18 \
  -c:a aac -b:a 128k \
  ./06-output/ep{NN}-final.mp4
```

#### 方案 B：xfade 转场（filter_complex）

适用于衔接方式包含 fade/fadewhite/fadeblack/circleclose 等 xfade 转场的情况。原片不裁切。

```bash
# 示例：seg1→seg2 硬切，seg2→seg3 fadewhite 0.3s，seg3→seg4 fadeblack 0.5s
ffmpeg -i seg1.mp4 -i seg2.mp4 -i seg3.mp4 -i seg4.mp4 \
  -filter_complex "
    [0:v][1:v]concat=n=2:v=1:a=0[v01];
    [0:a][1:a]concat=n=2:v=0:a=1[a01];
    [v01][2:v]xfade=transition=fadewhite:duration=0.3:offset=29.7[v012];
    [a01][2:a]acrossfade=d=0.3[a012];
    [v012][3:v]xfade=transition=fadeblack:duration=0.5:offset=44.2[vout];
    [a012][3:a]acrossfade=d=0.5[aout]
  " -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 \
  -c:a aac -b:a 128k \
  ./06-output/ep{NN}-final.mp4
```

> ⚠️ **offset 计算**：`offset = 前面所有段的累计时长 - 前面所有 xfade 转场的累计时长 - 当前转场时长`。硬切和黑场插入不消耗 offset。
>
> 💡 如果一集中既有硬切/黑场又有 xfade 转场，统一用 filter_complex 方案（方案 B）。

#### 闪烁帧处理（仅在发现问题时执行）

大部分情况下 Seedance 首尾帧是正常的，不需要处理。如果合成后发现某个衔接点有明显闪烁：

```bash
# 对段尾 0.1s 做 fade-out（不截内容，仅柔化最后几帧）
ffmpeg -i seg1.mp4 -vf "fade=t=out:st=14.9:d=0.1" -c:a copy seg1_faded.mp4
# 对段头 0.1s 做 fade-in
ffmpeg -i seg2.mp4 -vf "fade=t=in:st=0:d=0.1" -c:a copy seg2_faded.mp4
```

### 转场库速查

| 转场 | FFmpeg 参数 | 适用场景 |
|------|------------|---------|
| 硬切 | `concat` | 同场景连续叙事 |
| 淡入淡出 | `xfade=transition=fade` | 时间流逝、情绪缓冲 |
| 渐黑 | `xfade=transition=fadeblack` | 场景大跳跃、色温变化大 |
| 渐白 | `xfade=transition=fadewhite` | 婚礼/梦境、仪式感升级 |
| 柔滑左移 | `xfade=transition=smoothleft` | 进入回忆/闪回 |
| 柔滑右移 | `xfade=transition=smoothright` | 从回忆回到现实 |
| 向下擦除 | `xfade=transition=wipedown` | 竖屏空间跳转 |
| 向上擦除 | `xfade=transition=wipeup` | 情绪上升、空间提升 |
| 左滑 | `xfade=transition=slideleft` | 平行叙事 |
| 圆形收缩 | `xfade=transition=circleclose` | 聚焦关键物体、回忆结束 |
| 圆形展开 | `xfade=transition=circleopen` | 新场景揭示、回忆开始 |
| 径向擦除 | `xfade=transition=radial` | 时间流逝视觉隐喻 |

## 产出

| 文件 | 说明 |
|------|------|
| `06-output/ep{NN}-final.mp4` | 第 N 集成品（~60s） |

## 验收

- [ ] 段间色温一致性检查已执行（color_comparison.jpg 已生成并目测通过）
- [ ] 如有色彩校正，校正后重新对比确认通过
- [ ] 原片内容完整保留（零裁切）
- [ ] 段间转场方式与 assets.md 衔接规划表一致
- [ ] 3 处段间拼接无明显视觉跳跃或闪烁
- [ ] 音频无断裂或音量突变
- [ ] 总时长约 60s

## 完成后

→ `stages/12-.*.md`
将 `STATE.md` 中 `当前阶段` 更新为 `12-.*`，勾选 11。
