# EP07 视频资产 — 七日恋人

## 段间衔接规划

| 衔接 | 场景变化 | 色温变化 | 方式 | 转场时长 |
|------|---------|---------|------|---------|
| 段1→段2 | 化妆间→花拱门下 | 暖白化妆灯→暖白日光+灯串 | **fadewhite 0.3s** | 0.3s |
| 段2→段3 | 同一花拱门下（连续） | 相同 | **硬切** | 0s |
| 段3→段4 | 花拱门下→陆深家客厅（夜晚） | 暖白日光→暖琥珀夜灯 | **fadeblack 0.5s** | 0.5s |

**合成衔接模式：WHB**（fadewhite + 硬切 + fadeblack）
**转场总时长**：0.8s

---

## 内心独白汇总

| 段 | 时机 | 角色 | 内容 | 语气 |
|----|------|------|------|------|
| 段1 | 苏晚宁看着镜中的自己，手刚稳住 | 苏晚宁 | "我策划过一百多场婚礼……从来没有手抖过。" | 很轻，困惑，像在问自己 |
| 段3 | 苏晚宁给陆深戴戒指时碰到他的手 | 苏晚宁 | "他的手……不抖了。" | 很轻，带着某种发现 |

---

## EP07 集级可迁移分析

### 场景 A：化妆间（seg1）
- 可迁移：化妆间空间、化妆灯、镜子 → 定场帧 seg1/frame01.jpg 已覆盖
- 可迁移：苏晚宁婚纱外观 → EP06 seg2/frame01.jpg 可复用，但 seg1 是化妆间特写不需要全身
- 不可迁移：手抖的动态、内心独白、林可欣推门的动作、表情切换

### 场景 B：花拱门下·正式婚礼（seg2、seg3）
- 可迁移：花拱门+灯串+宾客空间 → 定场帧 seg2/frame01.jpg 已覆盖
- 可迁移：戒指特写 → seg3/frame01.jpg 已覆盖
- 不可迁移：誓词对白（台本+脱稿）、表情变化时序、戒指动作、耳语动态

### 场景 C：陆深家客厅·夜晚（seg4）
- 可迁移：客厅空间、冷暖对比光线 → 定场帧 seg4/frame01.jpg 已覆盖
- 不可迁移：沉默的对峙、"饿了吗"对白、戒指反光细节

### 补充参考图需求
- 无需额外补图。所有场景已有故事板帧覆盖。

---

## 段1 精简版 Prompt

### ref-images 清单（5张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep07/seg1/frame01.jpg | 钩子帧：镜中倒影·手抖+口红的构图和光影 |
| 图片2 | ep07/seg1/frame02.jpg | 林可欣推门·苏晚宁转身的空间和光影 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | linkexin/front.jpg | 林可欣（Lín Kěxīn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（恍惚→职业微笑的过渡） |

### audio 清单（1条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |

### Prompt

```
婚礼当天清晨，苏晚宁在化妆间对着镜子化妆，手拿口红时手指微微发抖。林可欣推门催她出场。
画面中先1个人，后2个人。

开场3秒：`图片1`中化妆镜的构图——镜中映出苏晚宁的脸，妆容精致，白色婚纱缎面领口在画面下方。她的右手拿着口红伸向嘴唇，手指在微微发抖，口红尖端悬在嘴唇前停住了。
苏晚宁（Sū Wǎnníng）形象参考`图片3`，表情参考`图片5`中的犹豫。
3秒无对白，只有空调低鸣。

苏晚宁闭眼深吸一口气。手稳住了。她画完口红，放下手，看着镜中的自己。

💭 内心独白作为画外音出现——声音很轻，困惑，像在问自己：
"我策划过一百多场婚礼……从来没有手抖过。"

门被推开。`图片2`中的空间构图。林可欣（Lín Kěxīn）形象参考`图片4`，从门口探进半个身子，短发，大耳环，表情夸张兴奋。

林可欣说道："新娘子！外面都准备好了，就等你了！"

苏晚宁转身，表情从恍惚瞬间切换为职业微笑。

苏晚宁说道："来了。妆没花吧？"

画面底部出现字幕，字幕内容与对话一致。
```

### 完整参数

```bash
python3 video-generation/scripts/seedance.py create \
  --prompt "{上述prompt}" \
  --ref-images \
    projects/test-drama/03-storyboard/ep07/seg1/frame01.jpg \
    projects/test-drama/03-storyboard/ep07/seg1/frame02.jpg \
    projects/test-drama/04-human-design/suwanning/front.jpg \
    projects/test-drama/04-human-design/linkexin/front.jpg \
    projects/test-drama/04-human-design/suwanning/expressions/hesitate.jpg \
  --audio \
    projects/test-drama/04-human-design/suwanning/voice-ref.mp3 \
  --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段2 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep07/seg2/frame01.jpg | 定场：花拱门下正式婚礼誓词中景 |
| 图片2 | ep07/seg2/frame02.jpg | 情绪高点：陆深脱稿瞬间面部特写 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（脱稿时的坦然） |
| 图片6 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（听到脱稿后的空白） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
正式婚礼誓词环节，苏晚宁念完台本誓词后，陆深脱稿说了一句不在台本里的真心话，苏晚宁的表演微笑消失了。
画面中2个人，宾客在背景虚化。

`图片1`中花拱门下两人面对面的中景构图。灯串全部点亮，暖白色小灯泡在白玫瑰间密集闪烁。宾客就座，背景虚化为暖白色光斑和人影。
苏晚宁（Sū Wǎnníng）形象参考`图片3`，穿白色婚纱。
陆深（Lù Shēn）形象参考`图片4`，穿深灰三件套西装。

司仪说道："请新娘说出你的誓词。"

苏晚宁微笑看着陆深，语气温柔稳定，说道："我愿意在每一个平凡的日子里，和你一起面对生活的所有。"

司仪说道："请新郎说出你的誓词。"

陆深看着苏晚宁，声音低沉稳定，说道："我愿意尊重你、保护你——"

他停了。嘴唇合上，又张开。目光从苏晚宁的眼睛移到她的手——她的手指在婚纱裙摆上微微攥紧——然后移回她的眼睛。
停顿一秒半。

镜头缓缓推向陆深面部，构图参考`图片2`。陆深表情参考`图片5`中的克制温柔——不是冲动，是想清楚了的坦然。
他声音放低，语速比台本慢，说道："……在你之前，没有人让我觉得，这些话不只是念一遍就算了。"

苏晚宁的表演微笑消失了。表情参考`图片6`中的犹豫——变成毫无防备的空白，嘴唇微微张开，眼睛里有什么在闪。

宾客席传来掌声。苏晚宁眨了一下眼睛，微笑恢复了——但嘴角在微微发颤。

画面底部出现字幕，字幕内容与对话一致。
```

### 完整参数

```bash
python3 video-generation/scripts/seedance.py create \
  --prompt "{上述prompt}" \
  --ref-images \
    projects/test-drama/03-storyboard/ep07/seg2/frame01.jpg \
    projects/test-drama/03-storyboard/ep07/seg2/frame02.jpg \
    projects/test-drama/04-human-design/suwanning/front.jpg \
    projects/test-drama/04-human-design/lushen/front.jpg \
    projects/test-drama/04-human-design/lushen/expressions/gentle.jpg \
    projects/test-drama/04-human-design/suwanning/expressions/hesitate.jpg \
  --audio \
    projects/test-drama/04-human-design/suwanning/voice-ref.mp3 \
    projects/test-drama/04-human-design/lushen/voice-ref.mp3 \
  --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段3 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep07/seg3/frame01.jpg | 戒指滑上无名指极近特写 |
| 图片2 | ep07/seg3/frame02.jpg | 情绪高点：陆深耳语·苏晚宁眼眶泛红 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（郑重+眼眶泛红） |
| 图片6 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（确定） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色（内心独白） |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色（耳语） |

### Prompt

```
正式交换戒指，陆深的动作很稳很慢，苏晚宁给他戴戒指时发现他的手不抖了。司仪说亲吻新娘，两人没有亲，陆深在她耳边说了一句话。
画面中2个人。

陆深（Lù Shēn）形象参考`图片4`，表情参考`图片6`中的克制温柔。他拿起铂金戒指，握住苏晚宁的左手，拇指轻轻按在她指节上，把戒指缓缓推上她的无名指（第四根手指，不是中指）。动作很稳，很慢——不像彩排时有那个顿。
构图参考`图片1`中戒指滑上无名指的极近特写。

苏晚宁（Sū Wǎnníng）形象参考`图片3`，表情参考`图片5`。她低头看着戒指，手停了一秒——不是犹豫，是某种没预料到的郑重。睫毛低垂，嘴唇微微抿紧。

轮到苏晚宁。她拿起另一枚戒指，握住陆深的左手。她的手指碰到他的手时——

💭 内心独白作为画外音出现——声音很轻，带着某种发现：
"他的手……不抖了。"

苏晚宁把戒指推上陆深的无名指，动作比预想的慢。

司仪微笑说道："现在，你可以亲吻你的新娘。"

两人对视。陆深没有吻她。他微微侧头，靠近她的耳边——构图参考`图片2`中的耳语中近景。他的嘴唇几乎贴着苏晚宁的耳廓，低声说了一句话。

苏晚宁的眼眶慢慢泛红，嘴角却微微上扬——不是笑，是某种忍住了什么的表情。

宾客鼓掌。两人分开，面向宾客。苏晚宁的手垂在身侧，手指微微蜷缩。

画面底部出现字幕，字幕内容与对话一致。
```

### 完整参数

```bash
python3 video-generation/scripts/seedance.py create \
  --prompt "{上述prompt}" \
  --ref-images \
    projects/test-drama/03-storyboard/ep07/seg3/frame01.jpg \
    projects/test-drama/03-storyboard/ep07/seg3/frame02.jpg \
    projects/test-drama/04-human-design/suwanning/front.jpg \
    projects/test-drama/04-human-design/lushen/front.jpg \
    projects/test-drama/04-human-design/suwanning/expressions/hesitate.jpg \
    projects/test-drama/04-human-design/lushen/expressions/gentle.jpg \
  --audio \
    projects/test-drama/04-human-design/suwanning/voice-ref.mp3 \
    projects/test-drama/04-human-design/lushen/voice-ref.mp3 \
  --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段4 精简版 Prompt

### ref-images 清单（5张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep07/seg4/frame01.jpg | 定场：客厅两人站立·夜晚冷暖对比 |
| 图片2 | ep07/seg4/frame02.jpg | 情绪高点：两只戴戒指的手垂在身侧 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（释然） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
婚礼结束回到家，夜晚客厅。两人换回便装但都没摘戒指。沉默中谁都没提契约到期，苏晚宁说"饿了吗"，陆深说"热一下吧"。
画面中始终只有2个人。

`图片1`中客厅的中景构图。暖琥珀色吊灯从上方打下柔光，落地窗外城市夜景冷蓝色，冷暖对比。
苏晚宁（Sū Wǎnníng）形象参考`图片3`，穿白衬衫，站在客厅中央。
陆深（Lù Shēn）形象参考`图片4`，穿深色休闲衫，站在她几步之外。
两人都没有摘手上的戒指——苏晚宁左手无名指上的铂金戒指在灯光下微微反光。

沉默。两人各自站着，保持一米多距离。

苏晚宁低头看了一眼自己手上的戒指。她的拇指碰了一下戒指边缘。
她抬起头，看向陆深。陆深也在看她。

停顿三秒。

苏晚宁先开口，语气平淡，像在说一件最普通的事，说道："饿了吗？冰箱里应该还有昨天的菜。"

陆深看着她。陆深表情参考`图片5`中的克制温柔——嘴角有一个极微小的弧度，不是笑，是某种释然。
陆深停顿一秒，语气平静，说道："热一下吧。"

镜头缓缓下移，构图参考`图片2`——停在两人各自垂在身侧的手上。两只手距离很近，不到十厘米，但没有碰到。两只手上都戴着婚戒，铂金表面在暖琥珀灯光下反射出微小光点。

画面底部出现字幕，字幕内容与对话一致。
```

### 完整参数

```bash
python3 video-generation/scripts/seedance.py create \
  --prompt "{上述prompt}" \
  --ref-images \
    projects/test-drama/03-storyboard/ep07/seg4/frame01.jpg \
    projects/test-drama/03-storyboard/ep07/seg4/frame02.jpg \
    projects/test-drama/04-human-design/suwanning/front.jpg \
    projects/test-drama/04-human-design/lushen/front.jpg \
    projects/test-drama/04-human-design/lushen/expressions/gentle.jpg \
  --audio \
    projects/test-drama/04-human-design/suwanning/voice-ref.mp3 \
    projects/test-drama/04-human-design/lushen/voice-ref.mp3 \
  --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段级进度追踪

| 段 | 状态 | task_id | seed | 备注 |
|----|------|---------|------|------|
| seg1 | completed | cgt-20260503211535-2fh8q | 13510 | seg1.mp4 + lastframe_seg1.png |
| seg2 | completed | cgt-20260503211610-hlqzq | 38891 | seg2.mp4 + lastframe_seg2.png |
| seg3 | completed | cgt-20260503224517-9ltgv | 68457 | seg3.mp4 + lastframe_seg3.png（v4：新故事板帧——戒指v5+耳语v3） |
| seg4 | completed | cgt-20260503212231-rxxbl | 25931 | seg4.mp4 + lastframe_seg4.png |

## 并行条件检查

- [x] seg1→seg2 fadewhite 转场，无尾帧依赖（场景跳转）
- [x] seg2→seg3 硬切，同场景连续——可考虑传尾帧，但 seg2 和 seg3 的 ref-images 独立
- [x] seg3→seg4 fadeblack 转场，无尾帧依赖（场景大跳跃）
- [x] 四段的 ref-images 互相独立

✅ 满足并行条件。seg1/seg2/seg3 先并发提交（并发数3），任意一段完成后提交 seg4。
