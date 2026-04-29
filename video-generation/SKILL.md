---
name: video-generation
description: Seedance 2.0 视频生成与 Seedream 5.0 图片生成工具。通过火山方舟 Ark API 调用 Seedance 和 Seedream 模型。触发词：视频生成、图片生成、Seedance、Seedream、文生视频、图生视频、图生图、组图。
---

# Seedance & Seedream 生成工具

通过火山方舟 Ark API 调用 **Seedance 2.0**（视频生成）和 **Seedream 5.0**（图片生成）模型。

## 环境要求

```bash
# 设置 API Key（两个工具共用）
export ARK_API_KEY="your-ark-api-key"
# 获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey
```

**零依赖**：仅使用 Python 标准库，Linux/Windows 均可直接运行。

## 工具概览

| 工具 | 模型 | 用途 |
|------|------|------|
| `scripts/seedance.py` | doubao-seedance-2-0-260128 | 视频生成（文生视频/图生视频/多模态参考生视频） |
| `scripts/seedream.py` | doubao-seedream-5-0-260128 | 图片生成（文生图/图生图/组图） |

---

## Seedance 2.0 视频生成

### 支持的生成模式

| 模式 | 输入 | 说明 |
|------|------|------|
| 文生视频 | 文本提示词 | 纯文字描述生成视频 |
| 图生视频-首帧 | 首帧图片 + 提示词(可选) | 从一张图生成视频 |
| 图生视频-首尾帧 | 首帧 + 尾帧图片 + 提示词(可选) | 控制视频起止画面 |
| 多模态参考生视频 | 图片(0~9) + 视频(0~3) + 音频(0~3) + 提示词(可选) | 全模态融合生成 |
| 样片生成 | draft_task_id | 基于样片生成正式视频 |

### 命令用法

```bash
# 文生视频
python3 scripts/seedance.py create --prompt "一只猫在草地上奔跑"

# 图生视频（首帧）
python3 scripts/seedance.py create --prompt "镜头缓缓推进" --image photo.jpg

# 图生视频（首尾帧）
python3 scripts/seedance.py create --image first.jpg --last-frame last.jpg --ratio 16:9

# 多模态参考生视频（图片+视频+音频）
python3 scripts/seedance.py create --prompt "画面跟随音乐节奏变化" \
  --ref-images char.jpg bg.jpg --video motion.mp4 --audio bgm.mp3

# 联网搜索增强
python3 scripts/seedance.py create --prompt "巴黎铁塔的日落延时摄影" --web-search

# 查询任务状态
python3 scripts/seedance.py status <task_id>

# 等待完成并下载
python3 scripts/seedance.py wait <task_id> --download ./output

# 列表查询
python3 scripts/seedance.py list --status succeeded --page 1 --page-size 10

# 取消/删除任务
python3 scripts/seedance.py delete <task_id>
```

### 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 文本提示词（中英日等，建议≤500字） | - |
| `--image` | 首帧图片（本地路径或URL） | - |
| `--last-frame` | 尾帧图片 | - |
| `--ref-images` | 参考图片（1~9张） | - |
| `--video` | 参考视频（0~3个） | - |
| `--audio` | 参考音频（0~3段） | - |
| `--draft-task-id` | 样片任务ID | - |
| `--model` | 模型ID | doubao-seedance-2-0-260128 |
| `--ratio` | 宽高比：16:9/4:3/1:1/3:4/9:16/21:9/adaptive | adaptive |
| `--duration` | 时长秒数（4~15 或 -1 自动） | 5 |
| `--frames` | 帧数（25+4n，29~289） | - |
| `--resolution` | 分辨率：480p/720p/1080p | 720p |
| `--seed` | 随机种子 | -1 |
| `--camera-fixed` | 固定机位（true/false） | false |
| `--watermark` | 添加水印（true/false） | false |
| `--generate-audio` | 生成音效（true/false） | true |
| `--draft` | 样片模式（仅1.5 Pro） | false |
| `--return-last-frame` | 返回尾帧图片 | false |
| `--service-tier` | 服务等级：default/flex（离线便宜50%） | default |
| `--timeout` | 任务超时秒数（3600~259200） | 172800 |
| `--callback-url` | 回调URL | - |
| `--web-search` | 启用联网搜索 | false |
| `--safety-id` | 终端用户安全标识 | - |

### 文件格式限制

- **图片**：jpeg/png/webp/bmp/tiff/gif/heic/heif，≤30MB
- **视频**：mp4/mov，≤50MB，时长2~15s，≤3个
- **音频**：wav/mp3，≤15MB，时长2~15s，≤3段

---

## Seedream 5.0 图片生成

### 支持的生成模式

| 模式 | 输入 | 说明 |
|------|------|------|
| 文生图 | 文本提示词 | 纯文字生成图片 |
| 单图生图 | 参考图片 + 提示词 | 基于参考图生成 |
| 多图生图 | 多张参考图(2~14) + 提示词 | 多图融合生成 |
| 文生组图 | 提示词 + seq=auto | 生成一组关联图片(≤15张) |
| 单图/多图生组图 | 参考图 + 提示词 + seq=auto | 参考图+组图 |

### 命令用法

```bash
# 文生图
python3 scripts/seedream.py create -p "夕阳下的海边城市" --size 16:9

# 图生图
python3 scripts/seedream.py create -p "转换为水彩画风格" -i photo.jpg

# 多图融合
python3 scripts/seedream.py create -p "两个角色一起喝咖啡" -i char1.png char2.png

# 生成组图
python3 scripts/seedream.py create -p "四季变化的故事" --seq auto --max-images 4

# 指定分辨率和格式
python3 scripts/seedream.py create -p "未来城市" --size 3K --format png

# 联网搜索增强
python3 scripts/seedream.py create -p "最新款特斯拉" --web-search

# 查看可用模型
python3 scripts/seedream.py models
```

### 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p`/`--prompt` | 文本提示词（中英，建议≤300字） | **必填** |
| `-i`/`--image` | 参考图（1~14张，本地路径或URL） | - |
| `-m`/`--model` | 模型：5.0/4.5/4.0/3.0 | 5.0 |
| `--size` | 尺寸：2K/3K、比例(16:9)、或 WxH | 2048x2048 |
| `--seed` | 随机种子（仅3.0） | -1 |
| `--seq` | 组图模式：auto/disabled | disabled |
| `--max-images` | 组图最大数量（1~15） | 15 |
| `--web-search` | 启用联网搜索（5.0） | false |
| `--stream` | 流式输出 | false |
| `--format` | 输出格式：png/jpeg（5.0） | jpeg |
| `--response-format` | 返回格式：url/b64_json | url |
| `--watermark` | 添加水印 | false |
| `--optimize-prompt` | 提示词优化：standard/fast | standard |
| `-d`/`--download` | 下载目录 | - |

### Size 推荐值

**2K**: 1:1→2048x2048, 16:9→2848x1600, 9:16→1600x2848, 4:3→2304x1728, 21:9→3136x1344

**3K**: 1:1→3072x3072, 16:9→4096x2304, 9:16→2304x4096, 4:3→3456x2592, 21:9→4704x2016

---

## 典型工作流

### 1. 先生成图片，再用图片生成视频

```bash
# 用 Seedream 生成首帧图片
python3 scripts/seedream.py create -p "一个宇航员站在火星表面" --size 16:9 --download ./frames

# 用 Seedance 基于首帧生成视频
python3 scripts/seedance.py create --prompt "宇航员缓缓抬头望向星空" \
  --image ./frames/seedream_1_xxx.jpg --ratio 16:9 --duration 5 --download ./videos
```

### 2. 连续视频生成（首尾帧衔接）

```bash
# 生成视频并返回尾帧
python3 scripts/seedance.py create --prompt "猫咪在花园里奔跑" \
  --image cat.jpg --return-last-frame true --download ./output

# 用上一段的尾帧作为下一段的首帧
python3 scripts/seedance.py create --prompt "猫咪跳上围墙" \
  --image ./output/lastframe_xxx.png --download ./output
```

### 3. 多模态参考生视频

```bash
python3 scripts/seedance.py create --prompt "角色跟随音乐节奏跳舞" \
  --ref-images character.png --video dance_ref.mp4 --audio music.mp3 \
  --ratio 9:16 --duration 10 --download ./output
```

---

## 提示词指南

编写 prompt 时参考官方指南可以显著提升生成质量：

- **Seedance 提示词指南**：[references/seedance-prompt.md](references/seedance-prompt.md)
  - 文本指令基础公式：主体 + 动作 → 环境/场景 → 光影/运镜/音效
  - 多模态参考指代：用"参考图片1的构图"、"参考视频2的动作"明确引用素材
  - 文字生成技巧：优先常用字，避免生僻字和特殊符号
  - 镜头调度：推拉摇移跟升降等专业术语

- **Seedream 提示词指南**：[references/seedream-prompt.md](references/seedream-prompt.md)
  - 通用规则：用自然语言描述主体+行为+环境，补充风格/色彩/光影
  - 图生图：支持增加/删除/替换/修改，可用涂鸦/线框/箭头指明编辑区域
  - 多图输入：明确指明"图一的XX"+"图二的YY"，支持替换/组合/风格迁移
  - 组图输出：用"一套"、"一系列"、具体数字触发组图生成

**关键提示**：
- Seedream 5.0 的文本理解能力比 3.0 强很多，**简洁精确优于堆砌华丽词汇**
- 文字内容用**双引号**包裹效果更好
- 图像编辑时明确指出**需保持不变的部分**

