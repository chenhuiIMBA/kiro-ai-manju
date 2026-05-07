# 资产速查表 — bengong-kaidian

> 本文件是项目所有生成资产的快速索引。每次新建/修改资产后同步更新。
> AI 进入任何阶段前先读此文件定位资产，不需要逐目录扫描。
> 最后更新：2026-05-06 16:20

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
| 选秀大殿 | `xuanxiu-dadian` | ✅ | EP01 选秀场景 |
| 御花园 | `yuhuayuan` | ✅ | 户外花园 |
| 御膳房 | `yushangfang` | ✅ | 沈鹿溪主要活动场所 |
| 赵太师府邸 | `zhaotaishi-fu` | ✅ | 权臣府邸内厅 |

**统计**：14 场景，main.png 14/14
**ref-images 用法**：阶段 07 直接传入 `main.png`（不需要 multiview）

---

## 角色库（04-character/）

| 中文名 | 目录名 | front.png | multiview.png | voice-ref.mp3 | 音色 ID |
|--------|--------|-----------|---------------|---------------|---------|
| 沈鹿溪 | `shenluxi` | ✅ | ✅ | ✅ | zh_female_meilinvyou (neutral) |
| 萧珩 | `xiaoheng` | ✅ | ✅ | ✅ | zh_male_qingcang (coldness) |
| 柳如烟 | `liuruyan` | ✅ | ✅ | ✅ | zh_female_gaolengyujie (coldness) |
| 温婉 | `wenwan` | ✅ | ✅ | ✅ | zh_female_meilinvyou (tender) |
| 太后 | `taihou` | ✅ | ✅ | ✅ | zh_female_wuzetian (coldness) |
| 赵太师 | `zhaotaishi` | ✅ | ✅ | ✅ | zh_male_qingcang (neutral) |
| 孙大厨 | `sundachu` | ✅ | ✅ | ✅ | zh_male_qingcang (happy) |
| 小桃 | `xiaotao` | ✅ | ✅ | ✅ | zh_female_sajiaoxuemei (excited) |

**统计**：8 角色，全部 3 件套齐全

---

## 视频产出（05-videos/）

| 集 | 目录 | seg 数 | 状态 |
|----|------|--------|------|
| EP01 | `05-videos/ep01/` | 14 | ✅ 全部生成 |

---

## 成片产出（06-output/）

| 集 | 文件 | 状态 |
|----|------|------|
| EP01 | `ep01-raw.mp4`（41M，无字幕） | ✅ |
| EP01 | `ep01-final.mp4`（24M，带字幕） | ✅ |

---

## 使用说明

- **场景引用**：阶段 07 的 ref-images 槽位-场景使用 `./03-scenes/{目录名}/main.png`
- **角色引用**：阶段 07 的 ref-images 槽位-角色使用 `./04-character/{目录名}/multiview.png`
- **音频引用**：阶段 07 的 --audio 使用 `./04-character/{目录名}/voice-ref.mp3`
