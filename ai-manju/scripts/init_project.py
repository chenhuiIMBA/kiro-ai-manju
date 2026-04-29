#!/usr/bin/env python3
"""初始化 AI 漫剧项目目录结构。

用法:
    python3 init_project.py <项目名> [--base /root/.openclaw/projects]

创建标准项目目录 + 复制阶段模板文件 + 写入 STATE.md。
"""

import argparse
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta


CST = timezone(timedelta(hours=8))


def main():
    parser = argparse.ArgumentParser(description="初始化 AI 漫剧项目目录")
    parser.add_argument("name", help="项目名称（英文，用于目录名）")
    parser.add_argument("--base", default=None, help="项目根目录（默认：当前目录下的 projects/，OpenClaw 环境下为 /root/.openclaw/projects）")
    args = parser.parse_args()

    # 自动检测环境：OpenClaw 用绝对路径，其他环境用当前目录下的 projects/
    if args.base is None:
        if os.path.isdir("/root/.openclaw"):
            args.base = "/root/.openclaw/projects"
        else:
            args.base = os.path.join(os.getcwd(), "projects")

    project_dir = os.path.join(args.base, args.name)

    # 技能目录（本脚本的父目录的父目录）
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stages_src = os.path.join(skill_dir, "stages")

    if not os.path.isdir(stages_src):
        print(f"❌ 未找到阶段模板目录: {stages_src}", file=sys.stderr)
        return 1

    # 创建产出物目录（按流水线顺序编号）
    dirs = [
        "01-scripts",
        "02-moodboard",
        "03-storyboard",
        "04-human-design",
        "05-videos",
        "06-output",
        "07-consistency-check/faces",
        "07-consistency-check/audio",
    ]

    created = []
    for d in dirs:
        path = os.path.join(project_dir, d)
        os.makedirs(path, exist_ok=True)
        created.append(path)

    # 复制阶段模板文件
    stages_dst = os.path.join(project_dir, "stages")
    os.makedirs(stages_dst, exist_ok=True)

    stage_files = sorted(f for f in os.listdir(stages_src) if f.endswith(".md"))
    for f in stage_files:
        src = os.path.join(stages_src, f)
        dst = os.path.join(stages_dst, f)
        shutil.copy2(src, dst)

    # 复制 references/
    references_src = os.path.join(skill_dir, "references")
    references_dst = os.path.join(project_dir, "references")
    if os.path.isdir(references_src):
        os.makedirs(references_dst, exist_ok=True)
        for f in os.listdir(references_src):
            if f.endswith(".md"):
                shutil.copy2(os.path.join(references_src, f), os.path.join(references_dst, f))

    # 写入 STATE.md
    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
    state_content = f"""# STATE — {args.name}（中文名待定）

**当前阶段**: 01-outline
**状态**: pending
**最后更新**: {now}
**当前集**: ep01
**总集数**: ?
---

## 阶段进度

- [ ] 01-outline
- [ ] 02-moodboard
- [ ] 03-lighting-color
- [ ] 04-character
- [ ] 05-script
- [ ] 06-storyboard
- [ ] 07-video-seg1
- [ ] 08-video-seg2
- [ ] 09-video-seg3
- [ ] 10-video-seg4
- [ ] 11-composite
- [ ] 12-review
- [ ] 13-batch
"""
    with open(os.path.join(project_dir, "STATE.md"), "w") as f:
        f.write(state_content)

    # 创建叙事管理占位文件
    scripts_dir = os.path.join(project_dir, "01-scripts")

    skeleton_path = os.path.join(scripts_dir, "episode-skeleton.md")
    if not os.path.exists(skeleton_path):
        with open(skeleton_path, "w") as f:
            f.write(f"# {args.name} 分段骨架\n\n（阶段 01 步骤 6 生成）\n")

    narrative_path = os.path.join(scripts_dir, "narrative-state.md")
    if not os.path.exists(narrative_path):
        with open(narrative_path, "w") as f:
            f.write(f"# 叙事状态追踪 — {args.name}\n\n**最后更新集**: EP00（初始化）\n\n（阶段 01 步骤 8 填充）\n")

    # 创建 README
    readme_path = os.path.join(project_dir, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write(f"# {args.name}\n\nAI 漫剧项目\n\n开始 → 读 `STATE.md`\n")

    print(f"✅ 项目已初始化: {project_dir}")
    print(f"   📋 STATE.md — 当前进度")
    print(f"   📂 stages/ — {len(stage_files)} 个阶段指令文件")
    for d in created:
        print(f"   📁 {d}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
