# 阶段 07：视频 Prompt 组装 + 依赖链并行生成

> 工具：Seedance 2.0（多模态参考生视频）
> ⚠️ 所有 seg 的 prompt 一次性组装并审核，然后按**依赖链并行**提交

## 前置条件

- 本集剧本已确认
- `narrative-state.md` 已更新（门禁 4）
- `03-scenes/` 场景库已就绪（本集用到的场景都存在）
- `04-character/{角色}/multiview.png` 和 `voice-ref.mp3` 存在

## 进入本阶段前的强制校验（🆕 门禁 4 自检）

**AI 执行进入阶段 07 前必须完成以下自检，任一未通过即回退到阶段 06：**

1. 读取 `01-scripts/narrative-state.md`，确认文件头部的 `最后更新集` = `EP{当前集}`
2. 如不等于当前集（例如仍是前一集），说明阶段 06 的步骤 6 未正确执行
3. 此时禁止进入视频组装，立即回退到阶段 06 步骤 6 完成 narrative-state 更新
4. 更新完成后重新进入阶段 07

> ⚠️ narrative-state 门禁不过不得绕过——未来集的视频 prompt 组装依赖本集的状态快照。跳过会导致角色态度/已揭露信息不连续，漂移风险显著上升。

## 流程

### 步骤 1：seg 切分

拿到确认的剧本后，按以下规则将一集拆分为多个 Seedance 任务。

#### 基础规则

- **规则 1：时长范围** — 每个 seg 4-15 秒，同一 seg 内保持同一场景
- **规则 2：尾帧衔接** — 同场景相邻 seg 中，后者的**起始画面**来自前者的尾帧（通过 `--ref-images` + prompt 声明实现）

#### 优化规则

- **规则 3：对白密度限制**
  - 4-8 秒段：最多 1 句对白
  - 8-12 秒段：最多 2 句对白
  - 12-15 秒段：最多 3 句对白
  - 超过密度的剧本内容应拆成多 seg

- **规则 4：单 seg 最多 2 个角色同框** — 3+ 角色场景面部一致性和动作协调易出错
  - 涉及 3+ 角色的时间轴，视角锁定在 1-2 个角色，其他作为背景或画外音
  - 展示群像（如选秀大殿全景）用远景，不靠面部识别

- **规则 5：场景跳转段起始画面必须文生视频** — 避免场景 B 起始画面继承场景 A 残影

- **规则 6：单 seg 只允许一种主运镜** — 复合运镜（推完再拉、推完再摇）执行经常失败

- **规则 7：回忆/闪回独立成段** — 回忆段起始画面用文生视频（哪怕前段是同场景），prompt 中明确"闪回，画面偏暖黄，老照片质感"

- **规则 8：对白段起始画面留 1-2 秒预热** — Seedance 对白启动有 0.3-0.8 秒延迟。对白段开头安排静默动作（看向对方、深呼吸），再进入对白

- **规则 9：段尾 0.5 秒留白** — 每段最后 0.5 秒尽量静态，便于下一段用尾帧作为起始画面时更自然

#### 片段划分表格式（assets.md 标准格式，强制）

写入 `05-videos/ep{NN}/assets.md`，严格遵守 `_convention.md` 的视频 seg 标准格式：

```markdown
## 片段划分表

| seg | 时长 | 状态 | task_id | seed | 首帧来源 | 依赖 | 备注 |
|-----|------|------|---------|------|---------|------|------|
| 1 | 10s | pending | — | — | 文生视频 | — | 幼年沈鹿溪揉面团 |
| 2 | 8s | pending | — | — | seg-1 尾帧 | seg-1 | 爷爷教做面 |
| 3 | 12s | pending | — | — | 文生视频 | — | 萧珩高坐审视（场景跳转） |
| 4 | 6s | pending | — | — | seg-3 尾帧 | seg-3 | 萧珩特写 |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

**首帧来源规则**：
- **文生视频**：场景跳转 / 回忆闪回（规则 5、7）
- **seg-N 尾帧**：同场景连续叙事时，上一 seg 尾帧作为起始画面（规则 2）

**依赖列规则**：
- 若 `首帧来源 = 文生视频`，`依赖 = —`
- 若 `首帧来源 = seg-N 尾帧`，`依赖 = seg-N`
- 该列决定并行提交的拓扑顺序（见步骤 5）

### 步骤 2：组装每个 seg 的 Prompt

为每个 seg 编写 Seedance prompt，采用**时间段节拍拆分结构**。

> ⚠️ **Prompt 审核门禁（门禁 1）**：所有 seg 的 prompt 组装完成后，对照 `references/prompt-guide.md` §六「提示词优化 Checklist」自查。**批次审核**——一整集所有 seg 的 prompt + ref-images 组合 + 参数一次性发给用户审核，确认后才可提交。

**Prompt 模板**：

```
{画风关键词}

视频中不要出现水印。保持无字幕，避免画面生成字幕。

[可选] 参考图片{N}作为起始画面。

{一句话场景总述：谁在哪里做什么}。
画面中{N}个人{：人物列表和位置，如有需要}。

{t1}-{t2}s：{景别}，{动作描述}。[可选：<环境音>]
{t2}-{t3}s：{景别}，{动作描述}。{角色A}说道："{台词A}"（emotion: {情感}, speed: {语速偏移}, loudness: {音量偏移}）
{t3}-{t4}s：{景别}，{动作描述}。{角色B}说道："{台词B}"（emotion: {情感}, speed: {语速偏移}, loudness: {音量偏移}）
...

💭 {如有内心独白}：
内心独白作为画外音出现——{语气描述}：
"{独白内容}"（emotion: {情感}）

[可选：无对话。]
```

**格式要点**：
- **画风关键词**：独立首行
- **反面约束**：紧跟画风关键词独占一段，固定写"视频中不要出现水印。保持无字幕，避免画面生成字幕。"
- **起始画面声明**（条件必选）：同场景相邻 seg 在反面约束后加"参考图片{N}作为起始画面"（N 是尾帧在 `--ref-images` 中的编号）。场景跳转段不加
- **时间段节拍**：`0-4s:`、`4-8s:` 等，每节拍 3-5 秒，每节拍一件事
- **景别术语**：特写/中近景/中景/中远景/远景（5 种）
- **镜头动词**：推进/拉远/跟拍/摇向/闪白/切入（简洁中文）
- **对白格式**：双引号包裹，紧跟动作后同节拍内；**对白后圆括号内注入 emotion/speed/loudness 三维情感标注**（从剧本对白汇总表复制过来）
- **情感标注作用**：作为 Seedance 配音的软提示，影响语气/语速/音量；值从剧本流转而来，不再是"文档性标注"
- **环境音**：用 `<>` 包裹，和对白视觉分离
- **反面约束**：紧跟画风关键词独占一段，不放 prompt 末尾
- **无对话段**：末尾加"无对话。"

### 步骤 3：ref-images 逻辑槽位 + 物理索引

每个 seg 的 ref-images 按**逻辑槽位**组织，但 Seedance 按**物理顺序**编号"图片N"。两者的映射必须在 assets.md 中显式记录。

#### 逻辑槽位定义

| 逻辑槽位 | 内容 | 默认路径 |
|---------|------|----------|
| 槽位-场景 | 场景主视角图 | `03-scenes/{场景名}/main.png` |
| 槽位-角色A | 角色A 多视图组合图 | `04-character/{角色A}/multiview.png` |
| 槽位-角色B | 角色B 多视图组合图 | `04-character/{角色B}/multiview.png` |
| 槽位-起始画面 | 本 seg 的起始画面（来源：上一 seg 的尾帧文件） | `05-videos/ep{NN}/lastframe_seg{N-1}.png` |
| 槽位-补充 | 手部/道具/换装参考图 | 按需生成（**可 1-3 张**） |

**传入顺序**（固定）：场景 → 角色A → 角色B → 起始画面 → 补充。缺失的槽位**跳过**，不占物理编号。

> ⚠️ **场景图只用 main.png，不要 multiview**。场景的核心价值是色调+材质+空间氛围，一张高质量主视角图足够。场景 multiview 在阶段 06 已取消生成（见 `06-scenes.md`），角色 multiview 保留（角色需要正/侧/背外观一致性）。

> ⚠️ **补充槽位可多张**：手部参考图 + 道具参考图 + 换装参考图可以同时存在，在补充槽位里按传入顺序各占一个物理编号。总 ref-images 张数受 4-5 张最佳、≤6 张的整体限制约束。

> ⚠️ **起始画面 vs 尾帧的区分**：从**当前 seg** 的角度，这张图承担"起始画面"的角色（即 prompt 里写"参考图片N作为起始画面"）。它的文件名是 `lastframe_seg{N-1}.png`（上一 seg 的尾帧文件），但在当前 seg 的 ref-images 语境下，它的**逻辑角色**是起始画面。槽位从消费者角度命名。

#### 物理编号（Seedance "图片N" 指代）

Seedance prompt 里的"图片N"按**实际传入的物理顺序**编号（1-based）。官方指南不支持稀疏槽位——只传 3 张图就不能写"图片4"。

**示例 1**（双人场景衔接段，5 张图全传）：

| 逻辑槽位 | 物理编号 | 文件 |
|---------|---------|------|
| 槽位-场景 | 图片1 | scene/main.png |
| 槽位-角色A | 图片2 | charA/multiview.png |
| 槽位-角色B | 图片3 | charB/multiview.png |
| 槽位-起始画面 | 图片4 | lastframe_seg3.png |
| 槽位-补充 | 图片5 | hand-ref.png |

Prompt 里写："参考图片4作为起始画面"。

**示例 2**(单人场景，无角色B/补充，含起始画面，传 3 张)：

| 逻辑槽位 | 物理编号 | 文件 |
|---------|---------|------|
| 槽位-场景 | 图片1 | scene/main.png |
| 槽位-角色A | 图片2 | charA/multiview.png |
| 槽位-角色B | （跳过） | — |
| 槽位-起始画面 | 图片3 | lastframe_seg3.png |

Prompt 里写："参考图片3作为起始画面"（不是图片4）。

#### 组装 prompt 时的编号计算规则

AI 组装 prompt 时，必须**根据本 seg 的实际 ref-images 列表**动态计算物理编号：

```
1. 按固定顺序（场景 → 角色A → 角色B → 起始画面 → 补充）枚举要传入的图片
2. 跳过缺失的槽位
3. 第 K 个传入的图片 = "图片K"
4. prompt 里所有"图片N"指代都用物理编号
```

**反模式**：不要为了跨 seg 对齐而硬留编号——如 prompt 写"图片4 作为起始画面"但实际只传 3 张图。这会指向不存在的图，模型会忽略或胡乱关联。

#### assets.md 中的双重记录

每个 seg 的详情块必须记录逻辑槽位 → 物理编号的映射：

```markdown
#### ref-images 映射

| 逻辑槽位 | 物理编号 | 文件路径 |
|---------|---------|----------|
| 槽位-场景 | 图片1 | `./03-scenes/shisi/main.png` |
| 槽位-角色A | 图片2 | `./04-character/alice/multiview.png` |
| 槽位-角色B | — | —（本段无） |
| 槽位-起始画面 | 图片3 | `./05-videos/ep01/lastframe_seg2.png` |
| 槽位-补充 | 图片4 | `./03-scenes/_props/hand-ring.png` |
| 槽位-补充 | 图片5 | `./03-scenes/_props/ring-closeup.png` |
```

> ⚠️ **补充槽位可多行**：同一逻辑槽位允许多张图（手部/道具/换装可共存），按传入顺序各占物理编号。

**ref-images 总数 4-5 张最佳**。超过 6 张风险上升。

### 步骤 4：用户批次审核

所有 seg 的 prompt + ref-images 组合 + 完整参数一次性发给用户审核（P0/P1 等级）。P2 等级可跳过。

### 步骤 5：依赖链并行提交

> ⚠️ **重大优化**：以前要求"逐个提交、等待完成再提下一个"。现改为**依赖链内串行、链间并行**，吞吐量提升 2-3 倍。

#### 依赖拓扑分析

从片段划分表的"依赖"列构造有向无环图（DAG）：
- 无依赖的 seg（文生视频段）= 根节点
- `依赖 = seg-N` 的 seg = seg-N 的子节点

同一场景的连续 seg 形成链：`seg-A (文生) → seg-B → seg-C`（后一个依赖前一个的尾帧）。
不同场景的 seg 形成独立链。

**示例 DAG**（一集 8 seg）：

```
链1（食肆场景）：seg-1 (文生) → seg-2 → seg-3
链2（大殿场景）：seg-4 (文生) → seg-5 → seg-6
链3（独立特写）：seg-7 (文生)
链4（食肆结尾）：seg-8 (文生)
```

4 条链可并发提交，每条链内部串行。

#### 并发执行策略

- **并发上限**：同时最多 3 个链（避免 API 限流）。超过 3 条链时，按场景优先级排队
- **链内串行**：依赖前置 seg 尾帧的 seg 必须等前置完成才能提交
- **起始画面传递**：前置 seg 完成下载后，将 `lastframe_seg{N}.png` 加入后续 seg 的**起始画面槽位**（物理编号按实际传入顺序计算）

#### 并发调度参考实现

> AI 执行时可用以下 bash 模式管理并发（不是强制脚本，按需调整）：

```bash
# 并发上限
MAX_PARALLEL=3

# 第一波：所有根节点 seg（无依赖，可并发启动）
declare -A TASK_IDS   # seg_num → task_id
declare -A CHAIN_HEAD # 场景名 → 当前最新已启动的 seg

# 枚举根节点 seg，控制并发
for seg in 根节点列表; do
  while [ $(jobs -r -p | wc -l) -ge $MAX_PARALLEL ]; do sleep 5; done
  (
    task_id=$(python3 <video-gen>/scripts/seedance.py create ... | extract_task_id)
    echo "${seg}:${task_id}" >> /tmp/tasks.log
    python3 <video-gen>/scripts/seedance.py wait "$task_id" --download ./05-videos/ep{NN}/
    # 重命名 + 更新 assets.md
  ) &
done
wait

# 第二波：子节点 seg（依赖已完成的前置 seg 尾帧）
# 重复上面的逻辑，ref-images 中加入对应前置 seg 的 lastframe
```

**简化建议**：对于典型一集 8-10 seg 的规模，可以先提交**所有根节点**等全部完成，再提交**所有子节点**等全部完成。虽然不是最优拓扑排序，但实现简单，一集通常只有 1-2 波。

#### 执行命令

> ⚠️ **`--audio` 传入条件**：只在本段**有对白 / 内心独白 / 画外音**（有人声需要 TTS 生成）时传入对应角色的 `voice-ref.mp3`。纯动作段（无人声）**省略 `--audio`**。`--generate-audio true` 不变（仍用于生成环境音效），prompt 中的 `<环境音>` 标注走独立生成通道，与 voice-ref 无关。

**文生视频段**（场景跳转/独立段，有对白示例）：

```bash
python3 <video-gen>/scripts/seedance.py create \
  --prompt "{seg 视频 prompt}" \
  --ref-images \
    ./03-scenes/{场景名}/main.png \
    ./04-character/{角色A}/multiview.png \
    ./04-character/{角色B}/multiview.png \
  --audio \
    ./04-character/{角色A}/voice-ref.mp3 \
    ./04-character/{角色B}/voice-ref.mp3 \
  --ratio 9:16 \
  --duration {seg 时长} \
  --generate-audio true \
  --return-last-frame true
```

**同场景衔接段**（尾帧作为起始画面，双人有对白示例）：

```bash
python3 <video-gen>/scripts/seedance.py create \
  --prompt "{seg 视频 prompt，开头含『参考图片4作为起始画面』——因为实际传入顺序场景/角色A/角色B/尾帧 = 图片1/2/3/4}" \
  --ref-images \
    ./03-scenes/{场景名}/main.png \
    ./04-character/{角色A}/multiview.png \
    ./04-character/{角色B}/multiview.png \
    ./05-videos/ep{NN}/lastframe_seg{N-1}.png \
  --audio \
    ./04-character/{角色A}/voice-ref.mp3 \
    ./04-character/{角色B}/voice-ref.mp3 \
  --ratio 9:16 \
  --duration {seg 时长} \
  --generate-audio true \
  --return-last-frame true
```

**纯动作段**（无对白/独白/画外音，省略 `--audio`）：

```bash
python3 <video-gen>/scripts/seedance.py create \
  --prompt "{seg 视频 prompt，末尾含『无对话。』}" \
  --ref-images \
    ./03-scenes/{场景名}/main.png \
    ./04-character/{角色A}/multiview.png \
    ./05-videos/ep{NN}/lastframe_seg{N-1}.png \
  --ratio 9:16 \
  --duration {seg 时长} \
  --generate-audio true \
  --return-last-frame true
```

> ⚠️ **图片编号随实际传入顺序动态变化**：同一 "尾帧" 槽位，双人场景时是图片4、单人场景时是图片3。必须根据本 seg 实际 ref-images 列表计算物理编号，并在 assets.md 的"ref-images 映射"表中记录。

> ⚠️ **为什么尾帧作为 ref-images 而不是 `--first-frame`**：Seedance 的 `--first-frame` 参数与多模态参考（`--ref-images`）互斥。我们用多模态参考传入场景图和角色图，所以尾帧必须作为 `--ref-images` 的一张传入，并在 prompt 中用"参考图片N作为起始画面"声明。

#### 批量管理

并发任务用 task_id 追踪，统一轮询：

```bash
# 提交所有根节点 seg（无依赖）
for seg in 根节点列表; do
  task_id=$(python3 <video-gen>/scripts/seedance.py create ... | grep -oP 'ID:\s*\K\S+')
  记录到 assets.md
done

# 等待完成并下载
python3 <video-gen>/scripts/seedance.py wait <task_id> --download ./05-videos/ep{NN}/

# 重命名
# 视频：seedance_{task_id}_{timestamp}.mp4 → seg{N}.mp4
# 尾帧：lastframe_{task_id}.png → lastframe_seg{N}.png

# 子节点 seg 此时可启动（前置尾帧已到位）
```

> 💡 优化：`seedance.py` 支持单次 `wait` 多个 task_id 可进一步并行化。如不支持，用 shell 后台进程轮询。

### 步骤 6：seed 策略

| 场景 | seed 值 | 理由 |
|------|---------|------|
| 首次生成 | 不传（默认 -1，随机） | 让模型自由发挥 |
| 重新生成（修 prompt） | 传上一次的 seed | 锚定"好方向" |
| 重新生成（碰运气） | 不传（默认 -1） | 换个随机方向 |

### 步骤 7：失败重试策略

| 失败类型 | 判断方式 | 处理 |
|----------|---------|------|
| API 超时/网络错误 | `seedance.py wait` 返回错误 | 原参数重试，最多 2 次 |
| 安全过滤拒绝 | 返回 content_filter 错误 | 调整 prompt 中可能触发过滤的描述，重试 |
| 质量不合格 | 目测：角色变形/面部崩塌/光影严重偏离 | 用 `regen_seg.sh` 重新生成，最多 2 次 |
| 连续 3 次失败 | 同 seg 连续 3 次未通过 | 停止，报告问题，和用户讨论方向调整 |
| API 整体不可用 | 所有任务都失败 | **暂停项目，等服务恢复**。禁止切换到备用模型（会导致风格漂移） |

**重试参数调整建议**：
- 角色变形 → 强化"保持角色与多视图一致"
- 光影偏离 → 强化光线描述
- 面部崩塌 → 检查角色多视图是否清晰
- 安全过滤 → 替换敏感表述

### 步骤 8：每段生成后的即时登记

每个 seg 下载完成后，立即更新 assets.md（即时登记门禁 2）：
- 片段划分表状态：pending → completed
- task_id、seed 填入
- seg 详情块写入完整 prompt（v1）、ref-images 槽位、audio

> assets.md 的 seg 块格式严格遵循 `_convention.md`「视频 seg 的标准格式」。

## 产出

| 文件 | 说明 |
|------|------|
| `05-videos/ep{NN}/seg{1-N}.mp4` | 本集所有 seg 视频 |
| `05-videos/ep{NN}/lastframe_seg{1-N}.png` | 各 seg 尾帧 |
| `05-videos/ep{NN}/assets.md` | 完整资产清单（按 `_convention.md` 标准格式） |

## 验收

- [ ] 所有 seg 已生成并下载
- [ ] 每段视频目测通过（角色一致性、场景色调）
- [ ] assets.md 按标准格式记录（片段划分表 + 每段详情块 + 版本历史）
- [ ] 每段的 ref-images 按固定逻辑槽位顺序传入，assets.md 记录物理编号映射
- [ ] 用户已确认进入合成

## 完成后

→ `stages/08-composite.md`
将 `STATE.md` 中 `当前阶段` 更新为 `08-composite`，勾选 07。
