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

### 步骤 2：交叉淡入淡出拼接（推荐）

4 段是独立 Seedance 任务，段间可能有微小视觉跳跃。每段首尾各截 0.3s，段间 0.5s crossfade：

```bash
ffmpeg -i ./05-videos/ep01/seg1.mp4 -i ./05-videos/ep01/seg2.mp4 \
       -i ./05-videos/ep01/seg3.mp4 -i ./05-videos/ep01/seg4.mp4 \
  -filter_complex \
    "[0:v]trim=0:14.7,setpts=PTS-STARTPTS[v0]; \
     [0:a]atrim=0:14.7,asetpts=PTS-STARTPTS[a0]; \
     [1:v]trim=0.3:14.7,setpts=PTS-STARTPTS[v1]; \
     [1:a]atrim=0.3:14.7,asetpts=PTS-STARTPTS[a1]; \
     [2:v]trim=0.3:14.7,setpts=PTS-STARTPTS[v2]; \
     [2:a]atrim=0.3:14.7,asetpts=PTS-STARTPTS[a2]; \
     [3:v]trim=0.3:15,setpts=PTS-STARTPTS[v3]; \
     [3:a]atrim=0.3:15,asetpts=PTS-STARTPTS[a3]; \
     [v0][v1]xfade=transition=fade:duration=0.5:offset=14.5[v01]; \
     [v01][v2]xfade=transition=fade:duration=0.5:offset=29.0[v012]; \
     [v012][v3]xfade=transition=fade:duration=0.5:offset=43.5[vout]; \
     [a0][a1]acrossfade=d=0.5:c1=nofade:c2=nofade[a01]; \
     [a01][a2]acrossfade=d=0.5:c1=nofade:c2=nofade[a012]; \
     [a012][a3]acrossfade=d=0.5:c1=nofade:c2=nofade[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 \
  ./06-output/ep01-final.mp4
```

> 每段首尾各截 0.3s，3 次 crossfade 过渡。总计损失 ~1.8s，成品约 58.2s。

### 步骤 2：硬切拼接（备选）

如果段间衔接本身很流畅：

```bash
ffmpeg -i ./05-videos/ep01/seg1.mp4 -i ./05-videos/ep01/seg2.mp4 \
       -i ./05-videos/ep01/seg3.mp4 -i ./05-videos/ep01/seg4.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset medium -crf 18 \
  ./06-output/ep01-final.mp4
```

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
