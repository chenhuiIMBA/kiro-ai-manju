# EP06 视频资产 — 七日恋人

## 段间衔接规划

| 衔接 | 场景变化 | 色温变化 | 方式 | 段尾指令 | 段头指令 |
|------|---------|---------|------|---------|---------|
| 段1→段2 | 同一婚礼场地 | 相同（暖白日光） | **硬切** | 无 | 无 |
| 段2→段3 | 同一场地（更衣室出口→花拱门下） | 相同（暖白日光） | **硬切** | 无 | 无 |
| 段3→段4 | 场地内→场地外 | 暖白→暖金夕阳 | **黑场fade 0.5s** | 无 | 无 |

**合成衔接模式：HHB**

---

## 内心独白汇总

| 段 | 时机 | 角色 | 内容 | 语气 |
|----|------|------|------|------|
| 段1-3 | 无 | — | — | — |
| 段4 | 陆深听到"你今天很帅"后愣住时 | 陆深 | "她说的是……我？" | 很低，像自言自语，困惑 |

---

## EP06 集级可迁移分析

### 场景 A：婚礼场地·白天（seg1、seg2、seg3）
- 可迁移：场地空间布局、花拱门、落地窗 → 定场帧 seg1/frame02.jpg 已覆盖
- 可迁移：角色日常服装外观 → 设定图已覆盖
- 可迁移：婚纱外观 → seg2/frame01.jpg 已覆盖
- 不可迁移：手整理花艺的动作、婚纱走出的动态、交换戒指的手指停顿、对白

### 场景 B：场地外·傍晚（seg4）
- 可迁移：傍晚街道空间、夕阳光影 → 定场帧 seg4/frame01.jpg 已覆盖
- 不可迁移：脱口而出的对白、愣住的表情变化、影子交叠的动态

### 补充参考图需求
- 无需额外补图。seg2 婚纱帧已覆盖婚纱外观。

---

## 段1 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep06/seg1/frame01.jpg | 钩子帧：手整理花艺特写的构图和光影 |
| 图片2 | ep06/seg1/frame02.jpg | 定场：婚礼场地两人花拱门前对视的空间和光影 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/bright-smile.jpg | 苏晚宁爽朗笑表情（职业性轻快） |
| 图片6 | lushen/expressions/cold-mask.jpg | 陆深冰冷面具表情（观察） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

婚礼前一天，策划师苏晚宁比婚庆公司更早到达场地检查细节，新郎陆深随后到场，两人在花拱门下第一次对视。

开场3秒：`图片1`中手整理花艺特写的构图——一双纤细的女性手在签到台上调整白玫瑰，手法专业精准。淡金色桌布，花瓣上有柔和光泽。镜头使用约85mm中长焦，浅景深。3秒无对白，只有花瓣被拨动的细微声响。

镜头缓缓拉远，露出苏晚宁穿着白衬衫和卡其色风衣站在签到台前。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng）。苏晚宁表情参考`图片5`中的爽朗笑——职业性的轻快。她走向花拱门，皱眉自言自语。

苏晚宁说道："花拱门的灯串间距不对……左边密右边疏。"

她伸手调整灯串。身后传来脚步声。

场景切到`图片2`中婚礼场地的中景构图。两侧落地窗暖白日光均匀洒入，柔光，整体明亮通透，淡金色调。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装，从入口走入，在过道中央停下。陆深表情参考`图片6`中的冰冷面具。淡暖金轮廓光勾勒两人发丝边缘。镜头使用约35mm标准焦段，深景深。

陆深说道："你比婚庆公司来得还早。"

苏晚宁转身，笑了一下，说道："职业病。看到不完美的婚礼会手痒。"

画面底部出现字幕，字幕内容与对话一致。视频节奏前慢后快，开场3秒沉默，对白后节奏轻快。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep06/seg1/frame01.jpg
  图片2: 03-storyboard/ep06/seg1/frame02.jpg
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

## 段2 精简版 Prompt

### ref-images 清单（6张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep06/seg2/frame01.jpg | 婚纱登场：苏晚宁穿婚纱走出更衣室的全身远景 |
| 图片2 | ep06/seg2/frame02.jpg | 情绪高点：陆深面部特写（表情裂开） |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（被击中的瞬间） |
| 图片6 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（不确定自己看到了什么） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

苏晚宁换上婚纱从更衣室走出来，陆深看到她的瞬间表情失控两秒后恢复冷脸。两人在全身镜前并排站立。

更衣室的门打开。`图片1`中苏晚宁穿白色简约缎面A字婚纱的全身构图——裙摆拖地，头发挽起露出脖颈线条，一只手提着裙摆。她从偏暗的更衣室方向走向明亮的场地中央。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng）。右侧落地窗暖白日光半逆光，婚纱缎面在光线中微微发光，裙摆边缘透出柔和光晕。淡暖金轮廓光勾勒头发和肩部边缘。镜头使用约50mm标准焦段，中等景深。

镜头切到`图片2`中陆深面部特写。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。陆深表情参考`图片5`中的克制温柔——看到苏晚宁的瞬间，眼神从空白变成柔软，嘴唇微微张开，右手从裤袋里抽出来手指微微蜷缩——像是想伸出去又克制住了。这个表情只持续两秒，然后他的下巴微微抬起，眼神恢复冷淡。镜头使用约100mm中长焦，浅景深，背景虚化为暖白色。眼神光在瞳孔上方可见。

苏晚宁走近，在他面前站定。苏晚宁表情参考`图片6`中的犹豫——她注意到了什么但不确定。

苏晚宁微微歪头，说道："怎么样？能过关吗？"

陆深停顿一秒，目光从她脸上移开，说道："……合适。"

两人走到全身镜前并排站立。镜子里映出一对新人——西装笔挺的男人和白纱曳地的女人。

画面底部出现字幕，字幕内容与对话一致。视频节奏减速型——婚纱登场时放慢，对白简短克制。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep06/seg2/frame01.jpg
  图片2: 03-storyboard/ep06/seg2/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/lushen/expressions/gentle.jpg
  图片6: 04-human-design/suwanning/expressions/hesitate.jpg
--audio
  音频1: 04-human-design/suwanning/voice-ref.mp3
  音频2: 04-human-design/lushen/voice-ref.mp3
--ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

---

## 段3 精简版 Prompt

### ref-images 清单（5张）

| 编号 | 文件 | 用途 |
|------|------|------|
| 图片1 | ep06/seg3/frame01.jpg | 定场：花拱门下两人面对面，灯串点亮 |
| 图片2 | ep06/seg3/frame02.jpg | 情绪高点：戒指滑上无名指极近特写 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/hesitate.jpg | 苏晚宁犹豫表情（说不清的复杂） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色（本段苏晚宁无对白，但保留音色锚定） |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色（本段陆深无对白，但保留音色锚定） |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

彩排走到交换戒指环节，陆深握住苏晚宁的手时两人都顿了一下，戒指滑上无名指后两人都没有松手。

`图片1`中花拱门下两人面对面的中景构图。白色花拱门灯串已点亮，暖白色小灯泡在白玫瑰间闪烁，形成梦幻光点散景。两侧落地窗暖白日光从左右同时打入，均匀柔光包围。光比约1.5:1——全剧灯光最完美的一刻。淡暖金轮廓光勾勒两人发丝和肩部边缘。镜头使用约50mm标准焦段，中等景深。

司仪站在一旁，看着流程单，说道："好，接下来是交换戒指环节。新郎先请。"

陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。他从司仪手中接过戒指盒，打开，拿起一枚简约铂金戒指，转向苏晚宁。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿白色婚纱。

他伸出左手握住苏晚宁的右手——手指碰到的瞬间，两个人都顿了一下。不是犹豫，是某种电流般的反应。

镜头推进到`图片2`中戒指滑上无名指的极近特写。陆深的拇指在她指节上停了一秒，然后把戒指缓缓推上她的无名指。男性手指关节微微泛白。镜头使用约100mm微距感，极浅景深，背景虚化为暖白色花朵和灯串光点。

苏晚宁低头看着戒指滑上自己的手指。苏晚宁表情参考`图片5`中的犹豫——嘴唇微微抿紧，睫毛低垂，表情不是喜悦，是某种说不清的复杂。

两人都没有松手。花拱门上的灯串在他们头顶闪烁。停顿两秒。

司仪打破沉默，语气轻松，说道："很好，很自然。明天就这样。"

苏晚宁先抽回了手。

画面底部出现字幕，字幕内容与对话一致。视频节奏极慢——交换戒指的动作被放慢，停顿是核心。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep06/seg3/frame01.jpg
  图片2: 03-storyboard/ep06/seg3/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/hesitate.jpg
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
| 图片1 | ep06/seg4/frame01.jpg | 定场：傍晚两人并肩走出场地，影子交叠 |
| 图片2 | ep06/seg4/frame02.jpg | 情绪高点：陆深愣住的侧脸中近景 |
| 图片3 | suwanning/front.jpg | 苏晚宁（Sū Wǎnníng）角色外观 |
| 图片4 | lushen/front.jpg | 陆深（Lù Shēn）角色外观 |
| 图片5 | suwanning/expressions/bright-smile.jpg | 苏晚宁爽朗笑表情（脱口而出的自然） |
| 图片6 | lushen/expressions/gentle.jpg | 陆深克制温柔表情（不知所措） |

### audio 清单（2条）

| 编号 | 文件 | 用途 |
|------|------|------|
| 音频1 | suwanning/voice-ref.mp3 | 苏晚宁音色 |
| 音频2 | lushen/voice-ref.mp3 | 陆深音色 |

### Prompt

```
现代韩漫风格，精致写实画风，纤细线条，柔和渐变上色，面部精致美型，柔和阴影。

彩排结束换回便装，苏晚宁脱口而出"你今天很帅"，陆深愣了三秒没接话。

`图片1`中傍晚两人并肩走出场地的中景构图。苏晚宁形象参考`图片3`中的苏晚宁（Sū Wǎnníng），穿回白衬衫和卡其色风衣。陆深形象参考`图片4`中的陆深（Lù Shēn），穿深灰西装。两人并肩走在人行道上，保持半臂距离。暖金色夕阳从左侧低角度打来，穿过行道树叶间隙洒在两人身上。光比约3:1，半逆光，面部暗但轮廓被金色光线勾勒。淡暖金轮廓光强烈勾勒两人发丝和肩部边缘。地面上两人的影子被拉得很长。镜头使用约35mm标准焦段，深景深。

苏晚宁走着，语气随意，像在说今天天气不错。苏晚宁表情参考`图片5`中的爽朗笑——自然，没有防备。

苏晚宁说道："你今天很帅。"

陆深的脚步顿了一下。镜头切到`图片2`中陆深侧脸的中近景。陆深表情参考`图片6`中的克制温柔——不是冷漠，是某种不知所措，嘴唇微微张开像要说什么但没说出口。夕阳暖金色光照在他左半边脸上，右半边在柔和阴影中。眼神光在瞳孔上方可见，暖金色。镜头使用约85mm中长焦，浅景深，背景行道树虚化为暖金色光斑。

三秒沉默。他的右手拇指在身侧无意识搓了一下食指。

💭 画面停在陆深侧脸中近景上，夕阳暖金色光照在他脸上，表情不知所措。内心独白作为画外音出现——声音很低，像自言自语，带着困惑：
"她说的是……我？"

苏晚宁先走了几步，回头看他还站在原地，笑了一下，说道："走啊，发什么呆。"

最后一个画面：陆深跟上去，两人并肩走在夕阳下的人行道上，影子在地面上被拉得很长，影子的手几乎碰在一起——但没有。

画面底部出现字幕，字幕内容与对话一致。视频节奏减速型——"你今天很帅"之后节奏骤降，三秒沉默是核心。人物口型与配音同步。
```

### 完整参数

```
--prompt "{上述精简版prompt}"
--ref-images
  图片1: 03-storyboard/ep06/seg4/frame01.jpg
  图片2: 03-storyboard/ep06/seg4/frame02.jpg
  图片3: 04-human-design/suwanning/front.jpg
  图片4: 04-human-design/lushen/front.jpg
  图片5: 04-human-design/suwanning/expressions/bright-smile.jpg
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
| seg1 | completed | cgt-20260503115724-mzrz6 | seg1.mp4 + lastframe_seg1.png |
| seg2 | completed | cgt-20260503115800-2nss9 | seg2.mp4 + lastframe_seg2.png |
| seg3 | completed | cgt-20260503115835-q47wk | seg3.mp4 + lastframe_seg3.png |
| seg4 | completed | cgt-20260503120729-mktjl | seg4.mp4 + lastframe_seg4.png |

## 并行条件检查

- [x] seg1→seg2 硬切，seg2→seg3 硬切——同场景连续叙事，无尾帧依赖
- [ ] 不执行最佳帧反馈
- [x] 四段的 ref-images 互相独立

✅ 满足并行条件。seg1/seg2/seg3 先并发提交（并发数3），任意一段完成后提交 seg4。
