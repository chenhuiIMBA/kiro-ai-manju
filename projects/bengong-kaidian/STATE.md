# STATE — bengong-kaidian（《本宫想开店》）

**当前阶段**: 10-batch
**状态**: in-progress（EP04 已完成，EP05 剧本已确认）
**最后更新**: 2026-05-11
**当前集**: ep05
**当前子阶段**: 06-scenes
**总集数**: 80
**每集目标时长**: 120s（初始化时确定，后续剧本/切分以此为基准）
**信心度等级**: P0-全确认（EP04 重试率降至 12%，考虑 EP05 升级 P1）


---

## 时长参考（基于 120s/集）

| 类型 | 典型值 |
|------|--------|
| 每集 beat 数 | 3-5 |
| 每集 seg 数 | 12-20 |
| **单 seg 时长** | **4-15s（硬约束，每个 seg 必须在此区间）** |
| 对白密度 | 见 stages/07-video.md 规则 3 |

---

## 阶段进度

- [x] 01-outline  ← 已完成（series-bible / character-bible / episode-skeleton / narrative-state / visual-style-spec 已就绪，用户待审）
- [x] 02-moodboard  ← 已完成（7 张 16:9 风格概念图，纯中文 prompt，无人物）
- [x] 03-lighting  ← 已完成（lighting-philosophy.md + color-palette.md）
- [x] 04-character  ← 已完成（8 角色 front + multiview + voice-ref）
- [ ] 05-script
- [ ] 06-scenes  ← 按需模式（每集剧本确认后处理该集场景图：复用/修改/新建）
- [ ] 07-video
- [ ] 08-composite
- [ ] 09-review
- [ ] 10-batch
- [ ] 11-publish  ← 可选

> **场景库种子**：`03-scenes/` 已有 13 个场景的 main.png（阶段重排前生成），作为初始场景库。后续阶段 06 按需复用/修改/新建。

## 本集进度（ep03）

- [x] 05-script  ← 已完成（EP03 剧本确认 + narrative-state 已更新）
- [x] 06-scenes  ← 已完成（复用 xuanxiu-dadian + jinhuagong，无需新建）
- [x] 07-video  ← 已完成（12 seg 全部生成）
- [x] 08-composite  ← 已完成（raw + final 成片已产出，码率偏差 -4.31% ✅）
- [x] 09-review  ← 已完成（AI 预筛通过，技术参数达标，用户整体复盘通过）

## 本集进度（ep04）

- [x] 05-script  ← 已完成（EP04 v2 剧本确认 + narrative-state 已更新至 EP04）
- [x] 06-scenes  ← 已完成（御花园新增种菜角落变体图 zhongcai-jiao.png；冷月宫/御花园 main.png 复用）
- [x] 07-video  ← 已完成（12 seg 全部生成，P0 逐 seg，重试率 12%）
- [x] 08-composite  ← 已完成（raw + final 成片已产出，码率偏差 -3.03% ✅，时长 121.69s）
- [x] 09-review  ← 已完成（技术参数全部达标，字幕 Whisper 对齐 14/15，用户确认通过）

## 本集进度（ep05）

- [x] 05-script  ← 已完成（EP05 v1 剧本确认 + narrative-state 已更新至 EP05）
- [x] 06-scenes  ← 已完成（御膳房 yushangfang/main.png 完全匹配；宫道 gongdao/main.png 复用+prompt 覆盖深夜光线）
- [ ] 07-video
- [ ] 08-composite
- [ ] 09-review
