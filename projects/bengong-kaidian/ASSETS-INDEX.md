# 资产速查表 — bengong-kaidian

> 本文件是项目所有生成资产的快速索引。每次新建/修改资产后同步更新。
> AI 进入任何阶段前先读此文件定位资产，不需要逐目录扫描。
> 最后更新：2026-05-10（由 regen_assets_index.py 生成）

---

## 场景库（03-scenes/）

| 中文名 | 目录名 | main.png | 备注 |
|--------|--------|----------|------|
| 宫道 | `gongdao` | ✅ | 高墙夹峙的宫廷长道 |
| 宫门外 | `gongmen-wai` | ✅ | EP01 新建，皇宫正门+黄昏 |
| 宫墙边 | `gongqiang-bian` | ✅ | EP80 大结局食肆选址 |
| 宫宴大殿 | `gongyan-dadian` | ✅ | 金碧辉煌宴席大殿 |
| 锦华宫 | `jinhuagong` | ✅ | 柳如烟住所 |
| 冷月宫 | `lengyuegong` | ✅ | 沈鹿溪住所，清冷+暖灯 |
| 鹿溪记食肆 | `luxiji-shisi` | ✅ | 江南食肆，闪回+大结局 |
| 清芷宫 | `qingzhigong` | ✅ | 温婉住所 |
| 太后佛堂 | `taihou-fotang` | ✅ | 太后日常场景，佛像+沉香 |
| 萧珩书房 | `xiaoheng-shufang` | ✅ | 皇帝私人空间 |
| 选秀大殿 | `xuanxiu-dadian` | ✅ | EP01 选秀场景；新增 `jibai-buju.png` 集体跪拜群演布局变体 |
| 选秀大殿外廊下 | `xuanxiu-dadian-langxia` | ✅ | EP03 新建，殿外连廊，暖金阳光斜入 |
| 御花园 | `yuhuayuan` | ✅ | 户外花园 |
| 御膳房 | `yushangfang` | ✅ | 沈鹿溪主要活动场所 |
| 赵太师府邸 | `zhaotaishi-fu` | ✅ | 权臣府邸内厅 |

**统计**：15 场景，main.png 15/15
**ref-images 用法**：阶段 07 直接传入 `main.png`（不需要 multiview）

---

## 角色库（04-character/）

| 中文名 | 目录名 | front.png | multiview.png | voice-ref.mp3 | 音色 ID |
|--------|--------|-----------|---------------|---------------|---------|
| 柳如烟 | `liuruyan` | ✅ | ✅ | ✅ | zh_female_gaolengyujie (coldness) |
| 沈鹿溪 | `shenluxi` | ✅ | ✅ | ✅ | zh_female_meilinvyou (neutral) |
| 孙大厨 | `sundachu` | ✅ | ✅ | ✅ | zh_male_qingcang (happy) |
| 太后 | `taihou` | ✅ | ✅ | ✅ | zh_female_wuzetian (coldness) |
| 温婉 | `wenwan` | ✅ | ✅ | ✅ | zh_female_meilinvyou (tender) |
| 萧珩 | `xiaoheng` | ✅ | ✅ | ✅ | zh_male_qingcang (coldness) |
| 小桃 | `xiaotao` | ✅ | ✅ | ✅ | zh_female_sajiaoxuemei (excited) |
| 赵太师 | `zhaotaishi` | ✅ | ✅ | ✅ | zh_male_qingcang (neutral) |

**统计**：8 角色，全套齐全 8/8

### 群演角色（04-character/_extras/）

| 中文名 | 目录名 | multiview.png | 用途 |
|--------|--------|---------------|------|
| 众嫔妃群像 角色参考 | `_extras/bingfei-group` | ✅ |  |

---

## 视频产出（05-videos/）

| 集 | 目录 | seg 数 | 状态 |
|----|------|--------|------|
| EP01 | `05-videos/ep01/` | 14 | ✅ 全部生成 |
| EP02 | `05-videos/ep02/` | 13 | ✅ 全部生成 |
| EP03 | `05-videos/ep03/` | 12 | ✅ 全部生成 |

---

## 成片产出（06-output/）

| 集 | 文件 | 大小 | 状态 |
|----|------|------|------|
| EP01 | `ep01-final.mp4`（带字幕） | 39M | ✅ |
| EP01 | `ep01-raw.mp4`（无字幕） | 40M | ✅ |
| EP02 | `ep02-final.mp4`（带字幕） | 37M | ✅ |
| EP02 | `ep02-raw.mp4`（无字幕） | 38M | ✅ |
| EP03 | `ep03-final.mp4`（带字幕） | 46M | ✅ |
| EP03 | `ep03-raw.mp4`（无字幕） | 48M | ✅ |

---

## 使用说明

- **场景引用**：阶段 07 的 ref-images 槽位-场景使用 `./03-scenes/{目录名}/main.png`
- **角色引用**：阶段 07 的 ref-images 槽位-角色使用 `./04-character/{目录名}/multiview.png`
- **音频引用**：阶段 07 的 --audio 使用 `./04-character/{目录名}/voice-ref.mp3`
