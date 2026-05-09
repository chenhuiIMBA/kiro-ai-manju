"""EP02 seg 生成配置 — 最远的宫殿"""

STYLE = "3D渲染，CG动画风格，游戏原画,国风3D动漫,二次元"

NO_MARK = "视频中不要出现水印。保持无字幕，避免画面生成字幕。"

CHARS = {
    "shenluxi": "04-character/shenluxi",
    "liuruyan": "04-character/liuruyan",
    "xiaotao": "04-character/xiaotao",
}

SCENES = {
    "xuanxiu-dadian": "03-scenes/xuanxiu-dadian",
    "lengyuegong": "03-scenes/lengyuegong",
}

SEGS = [
    {
        "id": 1,
        "duration": 5,
        "scene": "xuanxiu-dadian",
        "chars": ["shenluxi"],
        "audio": [],  # 纯动作段
        "start_frame": None,
        "prompt": """宫殿走廊，一群盛装嫔妃鱼贯而入，绫罗绸缎在晨光中流动。

0-2s：特写，华丽裙摆群在晨光中流动，丝绸摩擦，脚步声轻盈。<丝绸摩擦声 + 脚步声>
2-5s：镜头缓缓上推，停在一双格格不入的素色布鞋上，镜头继续上推露出沈鹿溪（Shěn Lùxī）混在队伍最后面打着哈欠。

无对话。""",
    },
    {
        "id": 2,
        "duration": 10,
        "scene": "xuanxiu-dadian",
        "chars": ["liuruyan"],
        "audio": ["liuruyan"],
        "start_frame": 1,
        "prompt": """参考图片3作为起始画面。

选秀大殿内，太监手持名册宣读宫殿分配，柳如烟（Liǔ Rúyān）盛装坐在侧位高椅上冷冷扫视新人。
画面中1个人为主体：柳如烟居中偏右。

0-3s：中远景，大殿内嫔妃们按位次站立，金碧辉煌。
3-7s：中景，柳如烟坐在侧位高椅上，正红华服金丝绣纹，凤钗闪烁，团扇半遮面，丹凤眼冷冷扫视。
7-10s：中远景，太监展开名册。画外音说道："各位小主，今日分配寝宫。按位份高低，依次选取。"（emotion: neutral, speed: 0, loudness: 0.2）""",
    },
    {
        "id": 3,
        "duration": 10,
        "scene": "xuanxiu-dadian",
        "chars": ["liuruyan"],
        "audio": ["liuruyan"],
        "start_frame": 2,
        "prompt": """参考图片3作为起始画面。

选秀大殿内，嫔妃们争相表态想住好位置，柳如烟（Liǔ Rúyān）团扇轻摇不屑一顾。

0-4s：中景，几名嫔妃叽叽喳喳争抢，柳如烟团扇轻摇目光扫过沈鹿溪后不屑移开。
4-10s：中近景，柳如烟团扇半遮面。柳如烟说道："吵什么。都是些……不入流的地方。"（emotion: coldness, speed: -0.1, loudness: -0.1）""",
    },
    {
        "id": 4,
        "duration": 10,
        "scene": "xuanxiu-dadian",
        "chars": ["shenluxi"],
        "audio": ["shenluxi"],
        "start_frame": 3,
        "prompt": """参考图片3作为起始画面。

选秀大殿内，太监念到沈鹿溪名字，沈鹿溪（Shěn Lùxī）从队伍后面走出来打着哈欠，眼睛一亮问出惊人问题。

0-3s：中景，太监念名。画外音说道："沈氏鹿溪，请选寝宫。"（emotion: neutral, speed: 0, loudness: 0.1）
3-7s：中景，沈鹿溪从队伍后面走出，还在打哈欠。
7-10s：中近景，沈鹿溪眼睛一亮。沈鹿溪说道："有没有最偏远的？离皇上寝宫越远越好的那种？"（emotion: excited, speed: 0.1, loudness: 0）""",
    },
    {
        "id": 5,
        "duration": 8,
        "scene": "xuanxiu-dadian",
        "chars": ["shenluxi"],
        "audio": ["shenluxi"],
        "start_frame": 4,
        "prompt": """参考图片3作为起始画面。

选秀大殿内，全场哗然，太监翻名册犹豫，沈鹿溪（Shěn Lùxī）拍手决定。

0-3s：中远景，全场嫔妃面面相觑窃窃私语。
3-6s：中景，太监翻名册犹豫。画外音说道："最偏远的……是冷月宫。年久失修，无人愿住……"（emotion: nervous, speed: -0.1, loudness: -0.1）
6-8s：中近景，沈鹿溪拍手。沈鹿溪说道："就它了！"（emotion: happy, speed: 0.1, loudness: 0.1）""",
    },
    {
        "id": 6,
        "duration": 7,
        "scene": "xuanxiu-dadian",
        "chars": [],  # 嬷嬷无角色库
        "audio": [],  # 画外音用 generate-audio 自动生成
        "start_frame": 5,
        "prompt": """参考图片2作为起始画面。

选秀大殿角落，一名年长嬷嬷微微点头低声对身边人说话。

0-3s：中景，大殿角落一名年长嬷嬷微微点头。
3-7s：中近景，嬷嬷低声像是自言自语。画外音说道："不争不抢……倒是难得。"（emotion: neutral, speed: -0.2, loudness: -0.3）""",
    },
    {
        "id": 7,
        "duration": 12,
        "scene": "lengyuegong",
        "chars": ["shenluxi", "xiaotao"],
        "audio": ["shenluxi", "xiaotao"],
        "start_frame": None,
        "prompt": """冷月宫门前，沈鹿溪（Shěn Lùxī）和小桃（Xiǎo Táo）站在破旧宫殿前。门匾"冷月宫"漆面斑驳，院中杂草丛生，一棵老桂花树枝繁叶茂。
画面中2个人：沈鹿溪在画面左侧，小桃在画面右侧。

0-3s：远景，冷月宫全貌，破旧门匾，杂草院落，老桂花树。
3-7s：中景，小桃嘴巴张成O型。小桃说道："小姐！这……这也太破了吧？隔壁那个翊坤宫可是金碧辉煌——"（emotion: excited, speed: 0.2, loudness: 0.1）
7-12s：中近景，沈鹿溪深吸一口气满意环顾四周。沈鹿溪说道："完美。你看，这里离宫门近，离皇上远，墙矮树多……"（emotion: happy, speed: 0, loudness: 0）""",
    },
    {
        "id": 8,
        "duration": 8,
        "scene": "lengyuegong",
        "chars": ["xiaotao"],
        "audio": ["xiaotao"],
        "start_frame": 7,
        "prompt": """参考图片3作为起始画面。

冷月宫门前，小桃（Xiǎo Táo）双手叉腰吐槽。

0-3s：中近景，小桃双手叉腰，小脸皱成一团。
3-8s：中景，小桃对沈鹿溪说。小桃说道："小姐你又在想那些有的没的！"（emotion: angry, speed: 0.1, loudness: 0.1）""",
    },
    {
        "id": 9,
        "duration": 15,
        "scene": "lengyuegong",
        "chars": ["shenluxi", "xiaotao"],
        "audio": ["shenluxi", "xiaotao"],
        "start_frame": 8,
        "prompt": """参考图片4作为起始画面。

冷月宫殿内，沈鹿溪（Shěn Lùxī）走进破旧殿内看到桌上冷粥咸菜，用筷子夹起咸菜闻了闻皱眉放下。小桃（Xiǎo Táo）凑过来尝了一口吐舌头。
画面中2个人：沈鹿溪在画面左侧，小桃在画面右侧。

0-4s：中景，沈鹿溪走进殿内，桌上一碗冷粥两碟咸菜。
4-8s：特写，筷子夹起咸菜闻了闻，沈鹿溪皱眉放下。沈鹿溪说道："这咸菜……盐放多了，腌的时间不够，还有股子霉味。"（emotion: neutral, speed: 0, loudness: -0.1）
8-12s：中近景，小桃凑过来尝了一口吐舌头。小桃说道："呸！小姐说得对，这也太难吃了！"（emotion: angry, speed: 0.1, loudness: 0）
12-15s：中景，沈鹿溪无奈摇头看着简陋的殿内陈设。""",
    },
    {
        "id": 10,
        "duration": 12,
        "scene": "lengyuegong",
        "chars": ["shenluxi"],
        "audio": ["shenluxi"],
        "start_frame": 9,
        "prompt": """参考图片3作为起始画面。

深夜冷月宫内，只有一盏油灯。沈鹿溪（Shěn Lùxī）趴在桌上研究宫苑图，手指在图上比划标注出宫路线。

0-4s：中景，夜色深沉，油灯微光，沈鹿溪趴在桌上面前摊开宫苑图。
4-8s：特写，手指在图上比划，标注侧门位置。
8-12s：中近景，沈鹿溪低声自语。沈鹿溪说道："这里……侧门，子时换班，有半刻钟空档……"（emotion: neutral, speed: -0.1, loudness: -0.3）""",
    },
    {
        "id": 11,
        "duration": 10,
        "scene": "lengyuegong",
        "chars": ["shenluxi"],
        "audio": ["shenluxi"],
        "start_frame": 10,
        "prompt": """参考图片3作为起始画面。

深夜冷月宫内，沈鹿溪（Shěn Lùxī）从袖中掏出围裙轻轻摩挲绣字，油灯映照表情从专注变为柔软。

0-3s：特写，沈鹿溪从袖中掏出叠整齐的围裙，轻轻摩挲"鹿溪记"绣字。
3-7s：中近景，油灯光映在她脸上，表情从专注变为柔软。
7-10s：中近景，沈鹿溪更轻声。沈鹿溪说道："等我……快了。"（emotion: sad, speed: -0.2, loudness: -0.3）""",
    },
    {
        "id": 12,
        "duration": 8,
        "scene": "lengyuegong",
        "chars": ["shenluxi", "xiaotao"],
        "audio": ["xiaotao"],
        "start_frame": 11,
        "prompt": """参考图片4作为起始画面。

深夜冷月宫内，突然隔壁传来断续压抑的哭声。沈鹿溪（Shěn Lùxī）手一顿抬头看向墙壁方向，小桃（Xiǎo Táo）从被窝里探出头眼睛瞪圆。
画面中2个人：沈鹿溪在画面左侧桌前，小桃在画面右侧床上。

0-3s：中近景，沈鹿溪手一顿抬头看向墙壁方向。<断续压抑的哭声>
3-6s：中景，小桃从被窝里探出头眼睛瞪得溜圆。
6-8s：中近景，小桃声音发颤缩进被子。小桃说道："小……小姐……那是什么声音……"（emotion: nervous, speed: -0.1, loudness: -0.2）""",
    },
    {
        "id": 13,
        "duration": 5,
        "scene": "lengyuegong",
        "chars": ["shenluxi"],
        "audio": [],  # 纯动作段
        "start_frame": 12,
        "prompt": """参考图片3作为起始画面。

深夜冷月宫内，沈鹿溪（Shěn Lùxī）看着墙壁方向，哭声断断续续，她的表情从警觉变为若有所思，画面缓缓渐暗。

0-2s：中近景，沈鹿溪看着墙壁方向，若有所思。<断续压抑的哭声渐弱>
2-5s：中近景，画面缓缓渐暗，沈鹿溪表情停留在若有所思。

无对话。""",
    },
]
