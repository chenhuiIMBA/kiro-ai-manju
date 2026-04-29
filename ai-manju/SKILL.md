---
name: ai-manju
description: AI 漫剧创作全流程工作流。Seedream 5.0 出图 + Seedance 2.0 出视频 + FFmpeg 合成。全程火山方舟。触发词：AI漫剧、漫剧创作、ai漫画剧、漫剧制作。
---

# AI 漫剧工作流

## 一句话

13 个自包含阶段的串行流水线：整季大纲（含 80 段骨架 + 叙事状态追踪）→ 风格板 → 灯光配色 → 角色设计 → 剧本（逐集展开 + 更新叙事状态）→ 故事板 → 四段 prompt 组装审核 → 串行提交 → 合成（含色温检查）→ 检查 → 批量。

## 快速开始

```bash
# 1. 设置环境变量
export ARK_API_KEY="your-ark-api-key"         # 火山方舟
export DOUBAO_TTS_API_KEY="your-tts-api-key"  # 豆包TTS（可选，用于角色音色）

# 2. 初始化项目（创建目录 + 复制阶段文件 + 写入 STATE.md）
#    OpenClaw 环境自动使用 /root/.openclaw/projects/
#    其他环境（Kiro/Claude）使用当前目录下的 projects/
python3 <ai-manju>/scripts/init_project.py <项目名>

# 3. 进入项目，读 STATE.md
cd projects/<项目名>/    # 或 /root/.openclaw/projects/<项目名>/
cat STATE.md

# 4. 执行当前阶段
cat stages/01-outline.md
# → 按文件内指令执行 → 完成后更新 STATE.md → 进入下一阶段
```

## 阶段总览

| # | 阶段 | 工具 | 产出 |
|---|------|------|------|
| 01 | 整季叙事大纲 | DeepSeek | `series-bible.md` + `character-bible.md` + `episode-skeleton.md`（80 段骨架）+ `narrative-state.md`（叙事状态追踪） |
| 02 | 风格板 Moodboard | Seedream | `02-moodboard/` 3-5 张概念图 |
| 03 | 灯光哲学 + 配色 | 人工+DeepSeek | `lighting-philosophy.md` + `color-palette.md` |
| 04 | 角色设计 | Seedream + TTS | `04-human-design/{角色}/` 四视图 + 表情变体 + voice-ref |
| 05 | 剧本（单集） | DeepSeek | `ep{NN}-script.md` + 更新 `narrative-state.md` |
| 06 | 故事板 | Seedream | `03-storyboard/ep{NN}/seg*/` 每段 2 帧 |
| 07 | 四段 prompt 组装+审核+串行提交 | Seedance | `05-videos/ep{NN}/seg1~4.mp4`（含可选最佳帧反馈） |
| 08-10 | 段 2-4 视频提交 | Seedance | 段级视频（从阶段 07 assets.md 读取 prompt） |
| 11 | 合成 | FFmpeg | `06-output/ep{NN}-final.mp4`（含色温一致性检查） |
| 12 | 成片检查 | 人工 | 检查清单通过 |
| 13 | 批量生产 | 循环 05-12 | 后续集（每 5 集跨集审计） |

## 项目目录

```
projects/<项目名>/
├── STATE.md
├── stages/
├── references/
├── 01-scripts/
│   ├── series-bible.md          # 整季大纲
│   ├── character-bible.md       # 角色圣经
│   ├── episode-skeleton.md      # 80 段骨架（🆕）
│   ├── narrative-state.md       # 叙事状态追踪（🆕，每集更新）
│   └── ep{NN}-script.md         # 各集剧本
├── 02-moodboard/
├── 03-storyboard/
├── 04-human-design/{角色}/
├── 05-videos/ep{NN}/
├── 06-output/
└── 07-consistency-check/
```

## 核心约束

- **串行提交**：Seedance 任务必须等待上一个完成
- **四段一次性审核**：阶段 07 四段 prompt 统一审核，后续 08-10 只提交不重新审
- **段间衔接规划**：阶段 07 必须包含衔接方式选择（黑场fade/crossfade/硬切）
- **参考内联指代**：视频 prompt 中用 `图片N` 内联指代参考图用途（对齐 Seedance 官方指南）
- **用户确认**：大纲、骨架、角色、剧本、故事板、四段视频必须提交确认
- **故事板锁**：不通过不进视频阶段
- **叙事状态门禁**：剧本确认后必须更新 narrative-state.md，否则不进故事板（🆕）
- **逐集独立**：每集首帧重新生成，不沿用上集
- **对白双引号**：prompt 中对白双引号包裹 + 底部字幕指令
- **色温检查**：合成前截取四段首帧横向拼接对比，色温差异明显时校正（🆕）
- ⚠️ **即时登记**：生成→重命名→登记 assets.md→下一张

## 依赖

- `video-generation` skill（Seedance + Seedream 脚本）
- `tts` skill（角色音色参考，可选）
- FFmpeg

## 参考

- `stages/_convention.md` — 阶段文件格式规范
- `references/prompt-guide.md` — prompt 模板 + 审查清单 + 精简流程 + 内心独白指南
- `references/workflow-detail.md` — 分步详解
