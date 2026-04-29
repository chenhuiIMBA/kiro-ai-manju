# 七日恋人 配色方案

## 全剧色板

| 色板元素 | 颜色名称 | 语义标记 | 适用场景 |
|----------|---------|----------|---------|
| 主角肤色亮面 | 暖象牙白 | skin_highlight | 所有角色特写 |
| 主角肤色暗面 | 浅玫瑰棕 | skin_shadow | 所有角色特写 |
| 苏晚宁服装主色 | 米白/浅卡其 | charA_primary | 日常通勤装 |
| 陆深服装主色 | 深藏蓝 | charB_primary | 西装三件套 |
| 豪宅日景主调 | 暖白 | mansion_day | EP01-08 客厅/主卧 |
| 豪宅夜景主调 | 暖琥珀 | mansion_night | 台灯/吊灯场景 |
| 出租屋主调 | 灰冷蓝 | rental_ambient | EP13/15/17 出租屋 |
| 医院走廊 | 冷白 | hospital_cold | EP04 深夜医院 |
| 婚礼场地 | 淡金 | wedding_gold | EP06-07 婚礼 |
| 宴会厅 | 暖黄+冷蓝 | banquet_mixed | EP09 商业晚宴 |
| 雨景街道 | 冷蓝+暖金点缀 | rain_mixed | EP17 雨中 |
| 暖光源光色 | 暖金 | warm_key | 窗光/台灯/日落 |
| 冷光源光色 | 冷蓝 | cool_key | 月光/荧光灯/阴天 |
| 轮廓光 | 淡暖金 | rim_warm | 所有角色轮廓光 |
| 冲突场景环境 | 低饱和灰蓝 | conflict_ambient | EP10-13 冷战期 |
| 和解场景环境 | 柔暖米黄 | resolve_ambient | EP18-20 回暖期 |

## 使用规则

后续所有 prompt 使用语义标记引用色板，确保全剧色彩一致：

- 角色描述："苏晚宁穿着米白色衬衫（charA_primary）"
- 场景描述："豪宅客厅暖白色调（mansion_day），落地窗洒入暖金色光线（warm_key）"
- 光源描述："暖金色轮廓光（rim_warm）从角色后上方勾勒头发边缘"
- 对比场景："出租屋灰冷蓝色调（rental_ambient）与豪宅暖白（mansion_day）形成空间对比"

## 色彩弧线

| 阶段 | 集数 | 主导色调 | 情绪 |
|------|------|---------|------|
| 甜蜜期 | EP01-07 | 暖白+淡金（mansion_day + wedding_gold） | 温暖、希望、心动 |
| 僵持期 | EP08 | 暖白但偏淡（mansion_day 降饱和） | 不确定、等待 |
| 冲突期 | EP09-13 | 低饱和灰蓝（conflict_ambient） | 怀疑、冷战、分离 |
| 最低点 | EP13-14 | 灰冷蓝（rental_ambient） | 孤独、压抑 |
| 反击期 | EP15-16 | 冷蓝中出现暖金点缀 | 转折、希望重现 |
| 和解期 | EP17-20 | 柔暖米黄（resolve_ambient） | 柔和、真实、安定 |
