# EP02 视频资产 — 七日恋人

## 段间衔接规划

| 衔接 | 场景变化 | 色温变化 | 方式 | 段尾指令 | 段头指令 |
|------|---------|---------|------|---------|---------|
| 段1→段2 | 同一客厅 | 相同（暖白日光） | **短crossfade 0.3s** | 无 | 无 |
| 段2→段3 | 客厅→商场 | 暖白→暖黄 | **黑场fade 0.5s** | `画面缓慢暗下` | `画面从黑场渐亮` |
| 段3→段4 | 商场→傍晚街道 | 暖黄→暖金夕阳 | **crossfade 0.5s** | 无 | 无 |

---

## 内心独白汇总

| 段 | 时机 | 角色 | 内容 | 语气 |
|----|------|------|------|------|
| 段1-3 | 无 | — | — | — |
| 段4 | 苏晚宁发现陆深手在抖时 | 苏晚宁 | "他的手……在抖。" | 很轻，困惑中带意外 |

---

## EP02 集级可迁移分析

### 场景 A：陆深家客厅·白天（seg1、seg2）
- 可迁移：客厅空间布局、落地窗、沙发 → 定场帧 seg1/frame02.jpg 已覆盖
- 可迁移：角色服装外观 → 设定图已覆盖
- 不可迁移：牵手的动作时序、电话内容、情绪从僵硬到凝重的变化、运镜

### 场景 B：商场内部（seg3）
- 可迁移：商场空间、暖黄灯光氛围 → 定场帧 seg3/frame01.jpg 已覆盖
- 不可迁移：并肩走的动作、看橘子的视线方向、对白

### 场景 C：傍晚街道（seg4）
- 可迁移：街道空间、夕阳光影 → 定场帧 seg4/frame01.jpg 已覆盖
- 不可迁移：牵手动作、手指颤抖、表情变化

### 补充参考图需求
- 无需额外补图。

---

## 段1 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep02/seg1/frame01.jpg | 钩子帧：两手悬停特写的构图和光影 |
| 图片2 | ep02/seg1/frame02.jpg | 定场：客厅白天两人对峙的空间和光影 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（不情愿配合） |
| 图片6 | lushen/expressions/cold-mask.jpg | 陆深冰冷面具表情（强装镇定） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

清晨客厅，假夫妻苏晚宁和陆深第一次练习牵手，两人都僵硬得像木头。

开场3秒：`图片1`中两只手悬停特写的构图——左侧一只纤细的女性手指微微蜷缩，右侧一只修长的男性手掌摊开但僵硬，指尖相距不到五厘米，谁都没有先碰上去。3秒沉默，只有挂钟滴答声。镜头使用约100mm微距感，极浅景深，背景虚化为暖白光斑。

镜头拉远到`图片2`中客厅白天的中景构图。阳光从左侧落地窗均匀洒入，柔光，暖白色调。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿白衬衫高腰裤，双手抱在胸前，微微后仰。苏晚宁表情参考`图片5`中的犹豫状态。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装，手背在身后，右手拇指在身后无意识搓着食指。陆深表情参考`图片6`中的冰冷面具——强装镇定。淡暖金轮廓光从窗光方向勾勒两人发丝边缘。镜头使用约35mm标准焦段，深景深。

陆深说道："今天开始，我们需要在人前表现得……自然。"

苏晚宁说道："所以你的意思是……练习？"

陆深说道："从牵手开始。"

两人伸出手，指尖在半空中悬停。苏晚宁先碰上去——快速地、像完成任务一样握住他的手。两人都僵住了一秒。

画面底部出现字幕，字幕内容与对话一致。视频节奏前慢后快，开场3秒沉默，对白后节奏加速到牵手。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep02/seg1/frame01.jpg
  图片2: 03-storyboard/ep02/seg1/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/hesitate.jpg
  图片6: 04-human-design/lushen/expressions/cold-mask.jpg
--audio
  音频1: 04-human-design/suwanning/voice-ref.mp3
  音频2: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段2 精简版 Prompt

### ref-images 清单（5张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep02/seg2/frame01.jpg | 定场：苏晚宁背对窗光接电话的逆光构图 |
| 图片2 | ep02/seg2/frame02.jpg | 情绪高点：陆深门框遮挡中近景 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/restrain.jpg | 苏晚宁隐忍表情（压抑情绪打电话） |

### audio 清单（1条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

苏晚宁接到母亲电话，背过身压低声音说"钱快凑齐了"，不知道陆深站在原地听到了一切。

场景参考`图片1`中苏晚宁背对窗光的逆光构图。同一客厅，苏晚宁的手机响了，她迅速松开陆深的手，转身走向阳台方向。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿白衬衫。她背对落地窗站着，右手举着手机贴在耳边，左手垂在身侧握拳，头微微低下，肩膀微缩。落地窗明亮日光从她身后打来，强逆光，面部处于暗区，只有轮廓被光线勾勒。光比约4:1。苏晚宁表情参考`图片5`中的隐忍状态。镜头使用约50mm标准焦段，中等景深。

苏晚宁压低声音说道："妈，我知道……钱快凑齐了，你别担心。手术的事我在处理。"

苏晚宁声音更低，说道："嗯……不用等我，你先休息。"

苏晚宁挂了电话，深吸一口气，用手背快速擦了一下眼角，然后转身恢复职业表情。

镜头切到`图片2`中陆深的门框遮挡构图。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。他站在客厅中央，前景左侧门框遮住画面三分之一。他的表情从空白变成凝重——眉头微蹙，下巴微收。右手拇指停在银戒上没有转动——他听到了。镜头使用约85mm中长焦，浅景深，门框边缘微虚化。眼神光在瞳孔上方可见。

画面底部出现字幕，字幕内容与对话一致。视频节奏缓慢压抑，苏晚宁的台词之间有停顿和呼吸声。人物口型与配音同步。

画面缓慢暗下。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep02/seg2/frame01.jpg
  图片2: 03-storyboard/ep02/seg2/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/restrain.jpg
--audio
  音频1: 04-human-design/suwanning/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段3 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep02/seg3/frame01.jpg | 定场：商场远景两人并肩走 |
| 图片2 | ep02/seg3/frame02.jpg | 情绪高点：苏晚宁看橘子过肩特写 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/bright-smile.jpg | 苏晚宁爽朗笑表情（假装没事的轻快） |
| 图片6 | lushen/expressions/cold-mask.jpg | 陆深冰冷面具表情 |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

画面从黑场渐亮。陆深没有追问电话的事，而是带苏晚宁去商场买"夫妻装"——用交易借口包装关心。苏晚宁在水果摊前多看了一眼橘子。

开场：苏晚宁转身回来，表情恢复正常，语气轻快——太轻快了。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿卡其色风衣。苏晚宁表情参考`图片5`中的爽朗笑——假装没事。

苏晚宁说道："抱歉，私人电话。我们继续？"

陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。陆深表情参考`图片6`中的冰冷面具。他看了她一秒，没有追问，停顿后说。

陆深说道："出门。"

苏晚宁说道："去哪？"

陆深说道："买衣服。明天有人来家里，你需要看起来像住在这里的人。"

场景切换到`图片1`中的商场远景构图。商场内部，暖黄色多点光源从天花板洒下，柔光，整体暖黄色调。两人并肩走在服装区，保持半臂距离。镜头使用约35mm标准焦段，深景深。

镜头切到`图片2`中的过肩极特写。经过水果摊，苏晚宁的脚步慢了下来，目光落在一堆橘子上——暖黄灯光照在橘子表面泛出温暖的橙色光泽。她没有停下，只是多看了一眼，嘴角微微放松——一个不设防的瞬间。前景陆深肩膀虚化。镜头使用约85mm中长焦，浅景深。陆深的视线跟着她的目光移到了橘子上，然后移回来。他什么都没说。

画面底部出现字幕，字幕内容与对话一致。视频节奏前半快（对白），后半慢（商场无对白，用视觉叙事）。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep02/seg3/frame01.jpg
  图片2: 03-storyboard/ep02/seg3/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/bright-smile.jpg
  图片6: 04-human-design/lushen/expressions/cold-mask.jpg
--audio
  音频1: 04-human-design/suwanning/voice-ref.mp3
  音频2: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段4 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep02/seg4/frame01.jpg | 定场：傍晚街道远景，夕阳长影交叠 |
| 图片2 | ep02/seg4/frame02.jpg | 情绪高点：两手紧握极近特写 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（困惑+意外） |
| 图片6 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（避开目光但耳尖微红） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

傍晚回家路上，人群拥挤时陆深主动握住苏晚宁的手——不是练习，是直接握住的。苏晚宁发现他的手在发抖。

场景参考`图片1`中的傍晚街道远景构图。暖金色夕阳从左后方低角度打来，两人并肩走在人行道上，各自拎着购物袋。地面上两人的影子被夕阳拉得很长，影子在前方交叠在一起。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿卡其色风衣。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。光比约3:1，半逆光，面部暗但轮廓被金色光线勾勒。淡暖金轮廓光勾勒两人发丝和肩部边缘。镜头使用约35mm标准焦段，深景深。

一群人迎面走来，人行道变窄。陆深没有犹豫地伸手握住了苏晚宁的手——不是练习时那种摊开手掌等她来碰的姿势，是直接握住的。

镜头推进到`图片2`中两手紧握的极近特写。男性手从上方握住女性手，手指交叉扣紧，男性指节微微泛白。女性手腕上系着旧发绳。夕阳暖金色光从左侧打在手上，光比约3:1，硬光。镜头使用约100mm微距感，极浅景深，背景虚化为暖金色光斑。

苏晚宁低头看两人握在一起的手，语气轻，说道："……这次不用练了？"

陆深没有回答。苏晚宁感觉到他的手指在微微发抖。她抬头看他——陆深表情参考`图片6`中的克制温柔，侧脸被夕阳照亮，耳尖微红，目光看向前方，刻意不看她。苏晚宁表情参考`图片5`中的犹豫——困惑和意外。镜头使用约85mm中长焦，浅景深。

💭 画面停在苏晚宁抬头看陆深侧脸的中近景上，夕阳暖光打在两人脸上。内心独白作为画外音出现——声音很轻，困惑中带意外：
"他的手……在抖。"

最后一个画面：两人的手握在一起的特写，陆深的手指微微收紧。

画面底部出现字幕，字幕内容与对话一致。视频节奏减速型——从并肩走的日常节奏逐渐慢下来，到牵手后几乎静止。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep02/seg4/frame01.jpg
  图片2: 03-storyboard/ep02/seg4/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/hesitate.jpg
  图片6: 04-human-design/lushen/expressions/gentle.jpg
--audio
  音频1: 04-human-design/suwanning/voice-ref.mp3
  音频2: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段级进度追踪

| 段 | 状态 | task_id | 备注 |
|----|------|---------|------|
| seg1 | completed | cgt-20260430155418-4nxf8 | seg1.mp4 + lastframe_seg1.png |
| seg2 | completed | cgt-20260430162205-7rq9p | seg2.mp4 + lastframe_seg2.png |
| seg3 | completed | cgt-20260430162951-k9frd | seg3.mp4 + lastframe_seg3.png |
| seg4 | completed | cgt-20260430164022-7mkjc | seg4.mp4 + lastframe_seg4.png |

## 提交顺序

seg1 → 等待完成 → seg2 → 等待完成 → seg3 → 等待完成 → seg4 → 进入合成

## 并行条件检查

- [x] 段间没有硬切衔接（全部是 crossfade 或黑场fade）
- [ ] 不执行最佳帧反馈
- [x] 四段的 ref-images 互相独立

理论上可并行，但为稳妥仍串行提交。
