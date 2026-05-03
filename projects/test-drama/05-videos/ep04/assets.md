# EP04 视频资产 — 七日恋人

## 段间衔接规划

| 衔接 | 场景变化 | 色温变化 | 方式 | 段尾指令 | 段头指令 |
|------|---------|---------|------|---------|---------|
| 段1→段2 | 豪宅走廊→医院走廊 | 暖琥珀→冷白 | **黑场fade 0.5s** | `画面缓慢暗下` | `画面从黑场渐亮` |
| 段2→段3 | 同一医院走廊 | 相同（冷白） | **短crossfade 0.3s** | 无 | 无 |
| 段3→段4 | 医院走廊→车内 | 冷白→冷蓝+暖金交替 | **黑场fade 0.5s** | `画面缓慢暗下` | `画面从黑场渐亮` |

---

## 内心独白汇总

| 段 | 时机 | 角色 | 内容 | 语气 |
|----|------|------|------|------|
| 段2 | 陆深低头看苏晚宁+缴费单时 | 陆深 | "五十万……原来是这个。" | 很低，克制中带压抑的心疼 |
| 段4 | 苏晚宁闭眼靠车窗时 | 苏晚宁 | "他为什么……要来找我。" | 很轻，疲惫中带一丝动摇 |

---

## EP04 集级可迁移分析

### 场景 A：豪宅走廊·深夜（seg1）
- 可迁移：走廊空间、暖琥珀壁灯、虚掩的门 → 定场帧 seg1/frame01.jpg 已覆盖
- 可迁移：陆深深色家居服外观 → 设定图+seg1/frame02.jpg 已覆盖
- 不可迁移：推门确认空床的动作时序、拿手机犹豫放下的心理过程、拿车钥匙出门

### 场景 B：医院走廊·深夜（seg2、seg3）
- 可迁移：走廊空间、冷白荧光灯、蓝色塑料椅 → 定场帧 seg2/frame01.jpg 已覆盖
- 可迁移：陆深低头看的角度和表情 → seg2/frame02.jpg + gentle表情已覆盖
- 可迁移：苏晚宁惊醒表情 → seg3/frame01.jpg + restrain表情已覆盖
- 可迁移：披外套的构图 → seg3/frame02.jpg 已覆盖
- 不可迁移：蜷缩睡着→惊醒的动作转换、缴费单被塞进口袋的动作、对白、内心独白

### 场景 C：车内·深夜（seg4）
- 可迁移：车内空间、仪表盘冷蓝光、路灯暖金光 → 定场帧 seg4/frame01.jpg 已覆盖
- 不可迁移：转发绳的动作、对白、闭眼但睫毛颤动、内心独白、手机屏幕"已结清"

### 补充参考图需求
- 无需额外补图。所有场景已被故事板帧覆盖。

---

## 段1 精简版 Prompt

### ref-images 清单（5张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep04/seg1/frame01.jpg | 钩子帧：虚掩门缝看到空床的构图和光影 |
| 图片2 | ep04/seg1/frame02.jpg | 陆深站在深夜走廊的空间和光影 |
| 图片3 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片4 | lushen/expressions/cold-mask.jpg | 陆深冰冷面具表情（克制不安） |
| 图片5 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（发现她不在后的微妙变化） |

### audio 清单（1条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

深夜，陆深发现苏晚宁不在家，沉默地拿起车钥匙出门去找她。

开场3秒：`图片1`中虚掩门缝的构图——镜头缓缓推近门缝，透过门缝看到空荡荡的床，白色被子掀开一半，枕头有凹陷但人不在。只有空调低频嗡鸣和远处钟表滴答声。镜头使用约50mm标准焦段，中等景深，焦点在门缝内的空床上。

镜头切到`图片2`中陆深站在深夜走廊的中景构图。陆深形象参考`图片3`中的陆深（Lù Shēn），穿深色家居服。走廊尽头暖琥珀色壁灯是唯一光源，从右上方照来，柔光，光比约4:1，照亮他脸部右侧，左侧沉入暗区。淡暖金轮廓光勾勒头发和肩部边缘。陆深表情参考`图片4`中的冰冷面具——但下巴微微收紧，右手拇指按住银戒没有转动。

他推开门确认——房间是空的。他拿起手机，拇指悬在屏幕上方，停了两秒，然后锁屏放下。

他走到玄关，拿起车钥匙。动作果断，没有犹豫。

画面缓慢暗下。

画面底部出现字幕，字幕内容与对话一致。视频节奏缓慢压抑，全程无对白，纯视觉叙事。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep04/seg1/frame01.jpg
  图片2: 03-storyboard/ep04/seg1/frame02.jpg
  图片3: 04-human-design/lushen/front.jpg
  图片4: 04-human-design/lushen/expressions/cold-mask.jpg
  图片5: 04-human-design/lushen/expressions/gentle.jpg
--audio
  音频1: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```


---

## 段2 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep04/seg2/frame01.jpg | 定场：医院走廊远景，苏晚宁蜷缩在椅子上 |
| 图片2 | ep04/seg2/frame02.jpg | 情绪高点：陆深低头看苏晚宁的仰拍 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/restrain.jpg | 苏晚宁隐忍表情（睡着时眉头微皱） |
| 图片6 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（心疼） |

### audio 清单（1条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | lushen/voice-ref.mp3 | 陆深音色（内心独白） |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

画面从黑场渐亮。陆深在深夜医院走廊找到了苏晚宁——她蜷缩在塑料椅上睡着了，手里攥着缴费单。他站在她面前，没有叫醒她。

场景参考`图片1`中医院走廊远景的构图和冷白光影。冷白荧光灯从天花板均匀照射，无方向性漫射光，整体冷白色调。地面白色瓷砖反射冷光。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深色家居服，从走廊尽头走来，脚步放慢。镜头使用约24mm广角，深景深。

他看到了她——苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿薄外套，蜷缩在蓝色塑料椅上，头歪靠着墙，眼睛闭着，眉头微皱。苏晚宁表情参考`图片5`中的隐忍状态。手里攥着一张缴费单，纸角被捏皱。

镜头推近缴费单——能看到"手术费"和一串数字。

镜头切到`图片2`中陆深低头看苏晚宁的仰拍构图。陆深表情参考`图片6`中的克制温柔——眉头微松，嘴唇微抿，眼神柔和。右手抬起一半悬在半空，像是想碰她的肩膀，又放下了。冷白荧光灯从天花板照下，光比约3:1。镜头使用约85mm中长焦，浅景深。

💭 画面停在陆深低头看苏晚宁的中近景上，冷白荧光灯照在两人身上。内心独白作为画外音出现——声音很低，克制中带压抑的心疼：
"五十万……原来是这个。"

画面底部出现字幕，字幕内容与对话一致。视频节奏极缓，陆深走近的脚步声是唯一的动态声音。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep04/seg2/frame01.jpg
  图片2: 03-storyboard/ep04/seg2/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/restrain.jpg
  图片6: 04-human-design/lushen/expressions/gentle.jpg
--audio
  音频1: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段3 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep04/seg3/frame01.jpg | 苏晚宁惊醒面部特写 |
| 图片2 | ep04/seg3/frame02.jpg | 情绪高点：陆深给苏晚宁披外套 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/restrain.jpg | 苏晚宁隐忍表情（慌张防御） |
| 图片6 | lushen/expressions/cold-mask.jpg | 陆深冰冷面具表情（恢复平静） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

苏晚宁在医院走廊惊醒，发现陆深站在面前，慌张撒谎说"朋友生病了"。陆深没有拆穿，只说了一个字"嗯"，然后脱下外套搭在她肩上。

开场：`图片1`中苏晚宁面部特写构图。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng）。她猛地睁开眼——瞳孔微微收缩，表情从迷糊瞬间转为惊慌。苏晚宁表情参考`图片5`中的隐忍状态。冷白荧光灯从上方照下，面部被均匀冷光照亮。眼神光在瞳孔上方可见。镜头使用约100mm中长焦，浅景深。

她迅速把缴费单塞进口袋，站起来，后退半步。

苏晚宁慌张说道："你……你怎么在这？"

陆深形象参考`图片4`中的陆深（Lù Shēn），穿深色家居服。陆深表情参考`图片6`中的冰冷面具——已经恢复平静。

陆深平静说道："你不在家。"

苏晚宁说道："一个朋友生病了，我来看看。没什么大事。"

两秒沉默。陆深看着她，她知道他可能知道，但两人都没有捅破。

陆深只说了一个字："嗯。"

镜头切到`图片2`中陆深给苏晚宁披外套的中景构图。陆深脱下自己的外套，搭在苏晚宁肩上。动作自然但小心。走廊尽头出口标志灯在他身后形成微弱暖红色光晕——冷白环境中唯一的暖色。镜头使用约50mm标准焦段，中等景深。

画面底部出现字幕，字幕内容与对话一致。视频节奏前快后慢——惊醒时快，披外套时几乎静止。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep04/seg3/frame01.jpg
  图片2: 03-storyboard/ep04/seg3/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/restrain.jpg
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
| 图片1 | ep04/seg4/frame01.jpg | 定场：车内两人沉默，冷暖交替光线 |
| 图片2 | ep04/seg4/frame02.jpg | 悬念帧：手机屏幕"已结清" |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（动摇但抗拒） |
| 图片6 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（沉默的关心） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

画面从黑场渐亮。深夜回家路上，车内沉默。陆深说"以后有事可以说"，苏晚宁说"不用"。最后一个画面：第二天手机屏幕显示医药费"已结清"。

场景参考`图片1`中车内两人沉默的构图和冷暖交替光线。仪表盘冷蓝色光为基础照明，车窗外路灯暖金色光间歇性扫过车内，在两人脸上划出暖金色光条。光比约3:1。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），靠着车窗，肩上披着陆深的深色外套，头微微低下，右手手指无意识转着手腕上的旧发绳。苏晚宁表情参考`图片5`中的犹豫——动摇但抗拒。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深色家居服，双手握方向盘，目视前方。陆深表情参考`图片6`中的克制温柔。镜头使用约35mm标准焦段，中等景深。

陆深目视前方，语气平淡说道："以后有事，可以说。"

苏晚宁低头，声音很轻说道："不用。我自己能处理。"

三秒沉默。陆深没有再说话。苏晚宁靠着车窗，路灯光一道一道划过她的脸。她闭上了眼睛，但睫毛在微微颤动——没有睡着。

💭 画面停在苏晚宁闭眼靠着车窗的中近景上，路灯暖光和仪表盘冷光交替照在她脸上。内心独白作为画外音出现——声音很轻，疲惫中带一丝动摇：
"他为什么……要来找我。"

最后画面切到第二天白天。`图片2`中手机屏幕特写构图——医院缴费系统页面，大字"已结清"。苏晚宁的手指停在屏幕上，一动不动。暖白日光从左侧打入。镜头使用约85mm中长焦，浅景深。

画面底部出现字幕，字幕内容与对话一致。视频节奏减速型——从沉默到对白到更深的沉默。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep04/seg4/frame01.jpg
  图片2: 03-storyboard/ep04/seg4/frame02.jpg
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
| seg1 | completed | cgt-20260430184522-p5bhb | seg1.mp4 + lastframe_seg1.png |
| seg2 | completed | cgt-20260430184556-bhvlh | seg2.mp4 + lastframe_seg2.png |
| seg3 | completed | cgt-20260430184632-4q7vp | seg3.mp4 + lastframe_seg3.png |
| seg4 | completed | cgt-20260430185322-7rhvk | seg4.mp4 + lastframe_seg4.png |

## 提交顺序

seg1 → 等待完成 → seg2 → 等待完成 → seg3 → 等待完成 → seg4 → 进入合成

## 并行条件检查

- [x] seg1→seg2 黑场fade（无硬切依赖）
- [x] seg2→seg3 短crossfade（同场景但无尾帧依赖）
- [x] seg3→seg4 黑场fade（无硬切依赖）
- [x] 四段的 ref-images 互相独立
- [x] 满足并行条件：先提交 seg1/seg2/seg3（并发数3），任意一段完成后提交 seg4
