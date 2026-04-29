---
name: tts
description: 豆包语音合成 TTS（V3）。通过火山引擎「语音合成大模型」HTTP Chunked 单向流式 API 将文本合成为语音。支持 325+ 音色、20+ 情感、语速/音量/音调控制、情感强度调节。用于 ai-manju 角色音色参考、单句对白替换。触发词：TTS、语音合成、文字转语音、配音、音色参考。
---

# 豆包语音合成 TTS（V3）

通过火山引擎 **语音合成大模型 V3** 的 HTTP Chunked 单向流式 API，将文本合成为可下载的音频文件。

> ⚠️ **音色下线提醒**：1.0 音色（`mars_bigtts` / `moon_bigtts` / `wvae_bigtts` 后缀）将于 **2026.06.30** 下线停止服务（含 42 个音色如 Vivi、魅力苏菲、鲁班七号等），请迁移到 2.0 对应音色（`_uranus_bigtts` 后缀）。详见 `doc/auto-generate/api-doc/tts-api/docs-6561-2371397.md`

## 环境要求

```bash
# 推荐：新版控制台凭证（https://console.volcengine.com/speech/new）
export DOUBAO_TTS_API_KEY="your-api-key"

# 可选：覆盖默认资源 ID
export DOUBAO_TTS_RESOURCE_ID="seed-tts-2.0"

# 兼容：旧版控制台凭证（https://console.volcengine.com/speech/app）
export DOUBAO_TTS_APP_ID="your-app-id"
export DOUBAO_TTS_ACCESS_KEY="your-access-token"
```

**零依赖**：仅使用 Python 标准库。

---

## 命令用法

```bash
# 基础合成
python3 scripts/doubao_tts.py synthesize \
  --text "月色真美，不是吗？" \
  -d ./output

# 指定音色 + 情感
python3 scripts/doubao_tts.py synthesize \
  --text "我不会再逃了。" \
  --speaker zh_male_qingcang_uranus_bigtts \
  --emotion sadness --emotion-scale 4 \
  -d ./output

# 调整语速和音量
python3 scripts/doubao_tts.py synthesize \
  --text "你为什么还要回来？！" \
  --speaker zh_female_gaolengyujie_uranus_bigtts \
  --emotion angry --emotion-scale 5 \
  --speed 20 --loudness 10 \
  --encoding mp3 -d ./output

# 用上下文控制语气（仅 TTS 2.0）
python3 scripts/doubao_tts.py synthesize \
  --text "我永远不会原谅你。" \
  --speaker zh_female_shuangkuaisisi_uranus_bigtts \
  --context-texts "你可以用特别特别痛心的语气说话吗？"

# 列出推荐音色
python3 scripts/doubao_tts.py voices
```

---

## 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` | 合成文本 | **必填** |
| `--speaker` | 发音人 ID（见下方） | `zh_female_shuangkuaisisi_uranus_bigtts` |
| `--emotion` | 情感标记 | 自动（由模型根据文本推断） |
| `--emotion-scale` | 情感强度 1~5 | 4 |
| `--speed` | 语速 -50~100（0=正常，100=2倍速） | 0 |
| `--loudness` | 音量 -50~100（0=正常） | 0 |
| `--pitch` | 音调 -12~12（半音） | 0 |
| `--rate` | 采样率：8000/16000/22050/24000/32000/44100/48000 | 24000 |
| `--encoding` | 音频格式：mp3/pcm/ogg_opus | mp3 |
| `--bit-rate` | MP3 比特率（默认 128k） | 128000 |
| `--context-texts` | 语音指令，用 `[#指令]` 前缀控制语气（见「语音指令语法」） | - |
| `--model` | 模型版本：`seed-tts-1.1` / `seed-tts-2.0-expressive` / `seed-tts-2.0-standard` | - |
| `--explicit-language` | 指定语种：`zh-cn`/`en`/`ja`/`es-mx`/`id`/`pt-br` | - |
| `--explicit-dialect` | 指定方言（仅 Vivi 音色）：`dongbei`/`shaanxi`/`sichuan` | - |
| `--silence-duration` | 句尾增加静音 0~30000ms | - |
| `--enable-subtitle` | 返回词级时间戳字幕（仅 TTS 2.0） | false |
| `--disable-markdown-filter` | 不解析 Markdown 语法（默认会过滤 `**` 等标记） | false |
| `-d` / `--download` | 输出目录 | - |

**支持的情感**（取决于音色）：neutral, happy, sad, angry, surprised, fear, hate, excited, coldness, depressed, lovey-dovey, shy, comfort, tension, tender, storytelling, radio, magnetic, advertising, vocal-fry, ASMR, news, entertainment, dialect

### 鉴权参数

| 参数 | 变量 | 说明 |
|------|------|------|
| `--api-key` | `DOUBAO_TTS_API_KEY` | 新版 API Key（推荐） |
| `--resource-id` | `DOUBAO_TTS_RESOURCE_ID` | `seed-tts-2.0`（2.0音色）/ `seed-tts-1.0`（1.0音色） |
| `--app-id` | `DOUBAO_TTS_APP_ID` | 旧版 APP ID（兼容） |
| `--access-key` | `DOUBAO_TTS_ACCESS_KEY` | 旧版 Access Token（兼容） |

---

## 推荐音色

### 角色扮演 · 男

| 音色 ID | 风格 | 适用 |
|---------|------|------|
| `zh_male_qingcang_uranus_bigtts` | 深沉威严 | 霸道男主、帝王、反派 |
| `zh_male_ruyayichen_uranus_bigtts` | 儒雅清冷 | 清冷男主、古风公子 |
| `zh_male_silang_uranus_bigtts` | 低沉磁性 | 成熟男性、权谋角色 |
| `zh_male_shaonianzixin_uranus_bigtts` | 清澈少年 | 少年男主、热血青年 |
| `zh_male_aojiaobazong_uranus_bigtts` | 傲娇霸总 | 傲娇男主、霸总 |
| `zh_male_gaolengchenwen_uranus_bigtts` | 高冷沉稳 | 冷酷寡言、谍战角色 |
| `zh_male_sunwukong_uranus_bigtts` | 猴哥 | 孙悟空、灵动 |
| `zh_male_ruyaqingnian_uranus_bigtts` | 儒雅青年 | 温润公子 |
| `zh_male_wennuanahu_uranus_bigtts` | 温暖阿虎 | 暖男、阳光 |

### 角色扮演 · 女

| 音色 ID | 风格 | 适用 |
|---------|------|------|
| `zh_female_gaolengyujie_uranus_bigtts` | 高冷御姐 | 御姐、冷艳角色 |
| `zh_female_meilinvyou_uranus_bigtts` | 魅力女友 | 温柔女主、知心角色 |
| `zh_female_sajiaoxuemei_uranus_bigtts` | 撒娇学妹 | 萌系女主、学妹 |
| `zh_female_shuangkuaisisi_uranus_bigtts` | 爽快思思 | 爽朗女性、闺蜜 |
| `zh_female_wenroumama_uranus_bigtts` | 温柔妈妈 | 母亲、温柔长辈 |
| `zh_female_wuzetian_uranus_bigtts` | 武则天 | 霸气女帝 |
| `zh_female_gufengshaoyu_uranus_bigtts` | 古风少御 | 古风、侠女 |
| `zh_female_cancan_uranus_bigtts` | 知性灿灿 | 知性优雅 |
| `zh_female_chanmeinv_uranus_bigtts` | 谄媚女声 | 谄媚、反派女 |

### 有声阅读 / 旁白

| 音色 ID | 风格 | 适用 |
|---------|------|------|
| `zh_male_baqiqingshu_uranus_bigtts` | 霸气青叔 | 旁白、年长角色叙事 |
| `zh_male_shenyeboke_uranus_bigtts` | 深夜播客 | 文艺旁白、内心独白 |
| `zh_male_xuanyijieshuo_uranus_bigtts` | 悬疑解说 | 悬疑叙事 |
| `zh_male_cixingjieshuonan_uranus_bigtts` | 磁性解说 | 纪录片旁白 |
| `zh_female_qingxinnvsheng_uranus_bigtts` | 清新女声 | 清新旁白 |
| `zh_female_jitangnv_uranus_bigtts` | 鸡汤女 | 情感旁白 |

### 通用日常

| 音色 ID | 风格 | 适用 |
|---------|------|------|
| `zh_female_vv_uranus_bigtts` | Vivi 2.0 | 通用女声、支持方言 |
| `zh_female_tianmeixiaoyuan_uranus_bigtts` | 甜美小源 | 甜美女声 |
| `zh_male_yangguangqingnian_uranus_bigtts` | 阳光青年 | 开朗青年 |
| `zh_female_qinqienv_uranus_bigtts` | 亲切女声 | 日常自然 |

### 多语种

| 音色 ID | 风格 | 适用 |
|---------|------|------|
| `en_male_tim_uranus_bigtts` | Tim 美式男 | 英文旁白、角色 |
| `en_female_dacey_uranus_bigtts` | Dacey 美式女 | 英文女性角色 |

> 音色列表：`python3 scripts/doubao_tts.py voices`（按类别分组，可用 `-c 角色扮演` 过滤）  
> 完整音色文档：[音色列表](https://www.volcengine.com/docs/6561/1257544)，本地副本：`doc/auto-generate/api-doc/tts-api/docs-6561-1257544.md`

---

## 语音指令语法

TTS 2.0 音色支持用自然语言 `[#指令]` 前缀来控制语气、情感、演绎方式：

```bash
# 吵架语气
python3 scripts/doubao_tts.py synthesize \
  --text "那你另请高明啊，你找我干嘛！" \
  --speaker zh_female_shuangkuaisisi_uranus_bigtts \
  --context-texts "#你得跟我互怼！就是跟我用吵架的语气对话" \
  -d ./output

# ASMR 悄悄话
python3 scripts/doubao_tts.py synthesize \
  --text "每次听到你的声音，我都觉得心里暖暖的。" \
  --speaker zh_female_meilinvyou_uranus_bigtts \
  --context-texts "#用asmr的语气来试试撩撩我" \
  -d ./output

# 复杂情感（哭腔+绝望）
python3 scripts/doubao_tts.py synthesize \
  --text "我逆转时空九十九次救你，你却次次死于同一支暗箭。" \
  --speaker zh_female_gaolengyujie_uranus_bigtts \
  --context-texts "#用颤抖沙哑、带着崩溃与绝望的哭腔，夹杂着质问与心碎的语气说" \
  -d ./output
```

指令示例库见 `doc/auto-generate/api-doc/tts-api/docs-6561-1871062.md`

## 与 ai-manju 的协作模式

### A+ 方案：角色音色参考（推荐）

```bash
# 1. 为每个角色生成标准音色参考
python3 doubao_tts.py synthesize \
  --text "我叫林小夜。你不用帮我。" \
  --speaker zh_male_ruyayichen_uranus_bigtts \
  --emotion coldness --emotion-scale 3 \
  --encoding mp3 \
  -d ./human-design/林小夜/

# 2. 重命名
mv ./human-design/林小夜/tts_*.mp3 ./human-design/林小夜/voice-ref.mp3

# 3. Seedance --audio 挂载
python3 seedance.py create \
  --prompt "..." --image ... --ref-images ... \
  --audio human-design/林小夜/voice-ref.mp3 \
  --ratio 9:16 --duration 15
```

Seedance 的 `--audio` 参数接收参考音频后，模仿其音色风格来生成配音，保持口型同步。

### B 方案：单句替换

```bash
# TTS 重新合成问题句子
python3 doubao_tts.py synthesize \
  --text "这台词的语音效果不好。" \
  --speaker zh_male_qingcang_uranus_bigtts \
  --encoding mp3 -d ./output

# FFmpeg 精确替换对应音频片段
```

---

## 模型版本

| `X-Api-Resource-Id` | 音色版本 | 特点 |
|---------------------|---------|------|
| `seed-tts-2.0` | 2.0 音色（325+） | 情感自动推断、上下文语气指令、高自然度 |
| `seed-tts-1.0` | 1.0 音色（84+） | 多情感、混音、SSML 支持 |
| `seed-icl-2.0` | 声音复刻 2.0 | 个人音色克隆 |

---

## API 详情

- **Endpoint**: `https://openspeech.bytedance.com/api/v3/tts/unidirectional`（HTTP Chunked）
- **备选**: `wss://openspeech.bytedance.com/api/v3/tts/bidirection`（WebSocket 双向）、`/api/v3/tts/unidirectional/sse`（SSE）
- **协议**: HTTP POST，JSON body → Chunked streaming JSON 响应
- **鉴权**: Header `X-Api-Key` + `X-Api-Resource-Id`（新版控制台推荐）
- **计费**: 按字符数，`seed-tts-2.0` 对应「语音合成2.0字符版」
- **文档**: [语音合成大模型 V3 API](https://www.volcengine.com/docs/6561/1329505)，本地：`doc/auto-generate/api-doc/tts-api/`
