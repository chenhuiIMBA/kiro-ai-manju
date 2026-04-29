#!/usr/bin/env python3
"""
Seedance 2.0 视频生成 CLI（火山方舟 Ark API）

用法:
  python3 seedance.py create --prompt "描述" [options]
  python3 seedance.py create --prompt "描述" --image img.jpg [options]
  python3 seedance.py create --prompt "描述" --image first.jpg --last-frame last.jpg
  python3 seedance.py create --prompt "描述" --ref-images ref1.jpg ref2.jpg
  python3 seedance.py create --prompt "描述" --video motion.mp4 --audio bgm.mp3
  python3 seedance.py create --draft-task-id <task_id>
  python3 seedance.py status <task_id>
  python3 seedance.py wait <task_id> [--interval 10] [--download DIR]
  python3 seedance.py list [--status succeeded] [--page 1] [--page-size 10]
  python3 seedance.py delete <task_id>

环境变量:
  ARK_API_KEY - 火山方舟 API Key
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
DEFAULT_MODEL = "doubao-seedance-2-0-260128"

VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".heic", ".heif"}
VALID_VIDEO_EXTS = {".mp4", ".mov", ".webm"}
VALID_AUDIO_EXTS = {".mp3", ".wav"}
MAX_IMAGE_SIZE = 30 * 1024 * 1024
MAX_VIDEO_SIZE = 50 * 1024 * 1024
MAX_AUDIO_SIZE = 15 * 1024 * 1024


def get_api_key():
    key = os.environ.get("ARK_API_KEY", "").strip()
    if not key:
        print("Error: ARK_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API Key at: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method, url, data=None):
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            return resp_data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} {e.reason}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def file_to_data_url(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    ext = path.suffix.lower()
    if ext in VALID_IMAGE_EXTS:
        max_size = MAX_IMAGE_SIZE
    elif ext in VALID_VIDEO_EXTS:
        max_size = MAX_VIDEO_SIZE
    elif ext in VALID_AUDIO_EXTS:
        max_size = MAX_AUDIO_SIZE
    else:
        print(f"Error: Unsupported file format: {ext}", file=sys.stderr)
        sys.exit(1)
    if path.stat().st_size > max_size:
        print(f"Error: File too large ({path.stat().st_size} bytes, max {max_size}): {filepath}", file=sys.stderr)
        sys.exit(1)
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "application/octet-stream"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def resolve_media(media_input, media_type="image"):
    if media_input.startswith("http://") or media_input.startswith("https://") or media_input.startswith("asset://"):
        return media_input
    if media_input.startswith("data:"):
        return media_input
    return file_to_data_url(media_input)


def parse_bool(v):
    if isinstance(v, bool):
        return v
    s = str(v).lower()
    if s in ("true", "1", "yes"):
        return True
    if s in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean value expected, got: {v}")


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def format_task(task):
    lines = [
        f"ID:        {task.get('id', 'N/A')}",
        f"Model:     {task.get('model', 'N/A')}",
        f"Status:    {task.get('status', 'N/A')}",
        f"Created:   {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task.get('created_at', 0)))}",
    ]
    if task.get("updated_at"):
        lines.append(f"Updated:   {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task['updated_at']))}")
    if task.get("error"):
        lines.append(f"Error:     {task['error'].get('code', '')} - {task['error'].get('message', '')}")
    content = task.get("content") or {}
    if content.get("video_url"):
        lines.append(f"Video URL: {content['video_url']}")
    if content.get("last_frame_url"):
        lines.append(f"Last Frame: {content['last_frame_url']}")
    for k in ("seed", "resolution", "ratio", "duration", "frames", "framespersecond"):
        if task.get(k) is not None:
            lines.append(f"{k.replace('_', ' ').title()}: {task[k]}")
    if task.get("generate_audio") is not None:
        lines.append(f"Audio:     {'Yes' if task['generate_audio'] else 'No'}")
    if task.get("draft") is not None:
        lines.append(f"Draft:     {task['draft']}")
    if task.get("draft_task_id"):
        lines.append(f"Draft ID:  {task['draft_task_id']}")
    if task.get("service_tier"):
        lines.append(f"Tier:      {task['service_tier']}")
    usage = task.get("usage") or {}
    if usage.get("completion_tokens"):
        lines.append(f"Tokens:    {usage['completion_tokens']}")
    return "\n".join(lines)


def download_file(url, download_dir, filename):
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    filepath = download_path / filename
    print(f"  Downloading to {filepath} ...")
    urllib.request.urlretrieve(url, str(filepath))
    print(f"  Saved: {filepath}")
    return str(filepath)


def cmd_create(args):
    content = []
    # Text prompt
    if args.prompt:
        content.append({"type": "text", "text": args.prompt})

    # First frame image
    if args.image:
        url = resolve_media(args.image, "image")
        obj = {"type": "image_url", "image_url": {"url": url}}
        role = "first_frame"
        obj["role"] = role
        content.append(obj)

    # Last frame image
    if args.last_frame:
        url = resolve_media(args.last_frame, "image")
        content.append({"type": "image_url", "role": "last_frame", "image_url": {"url": url}})

    # Reference images
    if args.ref_images:
        for img in args.ref_images:
            url = resolve_media(img, "image")
            content.append({"type": "image_url", "role": "reference_image", "image_url": {"url": url}})

    # Reference videos
    if args.video:
        for v in args.video:
            url = resolve_media(v, "video")
            content.append({"type": "video_url", "role": "reference_video", "video_url": {"url": url}})

    # Reference audio
    if args.audio:
        for a in args.audio:
            url = resolve_media(a, "audio")
            content.append({"type": "audio_url", "role": "reference_audio", "audio_url": {"url": url}})

    # Draft task
    if args.draft_task_id:
        content.append({"type": "draft_task", "draft_task": {"id": args.draft_task_id}})

    if not content:
        print("Error: At least one content input is required (prompt, image, video, audio, or draft_task_id).", file=sys.stderr)
        sys.exit(1)

    body = {
        "model": args.model,
        "content": content,
    }

    # Optional parameters
    if args.ratio:
        body["ratio"] = args.ratio
    if args.duration is not None:
        body["duration"] = args.duration
    if args.frames is not None:
        body["frames"] = args.frames
    if args.resolution:
        body["resolution"] = args.resolution
    if args.seed is not None:
        body["seed"] = args.seed
    if args.camera_fixed is not None:
        body["camera_fixed"] = args.camera_fixed
    if args.watermark is not None:
        body["watermark"] = args.watermark
    if args.generate_audio is not None:
        body["generate_audio"] = args.generate_audio
    if args.draft is not None:
        body["draft"] = args.draft
    if args.return_last_frame is not None:
        body["return_last_frame"] = args.return_last_frame
    if args.service_tier:
        body["service_tier"] = args.service_tier
    if args.timeout is not None:
        body["execution_expires_after"] = args.timeout
    if args.callback_url:
        body["callback_url"] = args.callback_url
    if args.safety_id:
        body["safety_identifier"] = args.safety_id
    if args.web_search:
        body["tools"] = [{"type": "web_search"}]

    result = api_request("POST", BASE_URL, body)
    print("Task created:")
    print(format_task(result))
    print_json(result)


def cmd_status(args):
    url = f"{BASE_URL}/{args.task_id}"
    result = api_request("GET", url)
    # --url-only: print video URL and last_frame URL only (for script consumption)
    if args.url_only:
        content = result.get("content") or {}
        video_url = content.get("video_url", "")
        last_frame_url = content.get("last_frame_url", "")
        print(video_url)
        if last_frame_url:
            print(last_frame_url)
        return
    print(format_task(result))


def cmd_wait(args):
    task_id = args.task_id
    interval = max(5, args.interval or 10)
    download_dir = args.download
    start = time.time()

    while True:
        url = f"{BASE_URL}/{task_id}"
        result = api_request("GET", url)
        status = result.get("status", "unknown")
        elapsed = int(time.time() - start)

        if status == "succeeded":
            print(f"\nTask succeeded ({elapsed}s)")
            print(format_task(result))
            content = result.get("content") or {}
            if download_dir:
                video_url = content.get("video_url")
                if video_url:
                    filename = f"seedance_{task_id}_{int(time.time())}.mp4"
                    download_file(video_url, download_dir, filename)
                last_frame_url = content.get("last_frame_url")
                if last_frame_url:
                    download_file(last_frame_url, download_dir, f"lastframe_{task_id}.png")
            return
        elif status == "failed":
            print(f"\nTask failed ({elapsed}s)")
            print(format_task(result))
            sys.exit(1)
        elif status == "cancelled":
            print(f"\nTask cancelled ({elapsed}s)")
            sys.exit(1)
        elif status == "expired":
            print(f"\nTask expired ({elapsed}s)")
            sys.exit(1)
        else:
            print(f"  [{elapsed}s] Status: {status} ...", end="\r", flush=True)
            time.sleep(interval)


def cmd_list(args):
    params = []
    if args.page is not None:
        params.append(f"page_num={args.page}")
    if args.page_size is not None:
        params.append(f"page_size={args.page_size}")
    if args.status:
        params.append(f"filter.status={args.status}")
    if args.task_ids:
        for tid in args.task_ids:
            params.append(f"filter.task_ids={tid}")
    if args.model:
        params.append(f"filter.model={args.model}")
    if args.service_tier:
        params.append(f"filter.service_tier={args.service_tier}")

    url = BASE_URL
    if params:
        url += "?" + "&".join(params)

    result = api_request("GET", url)
    items = result.get("items", [])
    total = result.get("total", 0)
    print(f"Total: {total} task(s)")
    print("-" * 60)
    for item in items:
        print(format_task(item))
        print("-" * 60)


def cmd_delete(args):
    url = f"{BASE_URL}/{args.task_id}"
    api_request("DELETE", url)
    print(f"Task {args.task_id} deleted/cancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Seedance 2.0 Video Generation CLI (Volcengine Ark API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- create ---
    p_create = subparsers.add_parser("create", help="Create a video generation task")
    p_create.add_argument("--prompt", help="Text prompt (Chinese/English, max 500 chars)")
    p_create.add_argument("--image", help="First frame image (local path or URL)")
    p_create.add_argument("--last-frame", help="Last frame image (local path or URL)")
    p_create.add_argument("--ref-images", nargs="+", help="Reference images (1-9, local paths or URLs)")
    p_create.add_argument("--video", nargs="+", help="Reference videos (max 3, local paths or URLs)")
    p_create.add_argument("--audio", nargs="+", help="Reference audio (max 3, local paths or URLs)")
    p_create.add_argument("--draft-task-id", help="Draft task ID to generate final video from")
    p_create.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    p_create.add_argument("--ratio", choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                         help="Aspect ratio")
    p_create.add_argument("--duration", type=int, help="Duration in seconds (4-15 or -1 for auto)")
    p_create.add_argument("--frames", type=int, help="Frame count (25+4n, range 29-289)")
    p_create.add_argument("--resolution", choices=["480p", "720p", "1080p"], help="Resolution")
    p_create.add_argument("--seed", type=int, help="Random seed (-1 for random)")
    p_create.add_argument("--camera-fixed", type=parse_bool, help="Fix camera (true/false)")
    p_create.add_argument("--watermark", type=parse_bool, default=False, help="Add watermark (default: false)")
    p_create.add_argument("--generate-audio", type=parse_bool, help="Generate audio (true/false, default true)")
    p_create.add_argument("--draft", type=parse_bool, help="Draft mode - preview only (1.5 Pro only)")
    p_create.add_argument("--return-last-frame", type=parse_bool, help="Return last frame image (true/false)")
    p_create.add_argument("--service-tier", choices=["default", "flex"],
                         help="Service tier (default=online, flex=offline 50%% cheaper)")
    p_create.add_argument("--timeout", type=int, help="Task timeout in seconds (3600-259200, default 172800)")
    p_create.add_argument("--callback-url", help="Callback URL for status notifications")
    p_create.add_argument("--web-search", action="store_true", help="Enable web search tool (Seedance 2.0)")
    p_create.add_argument("--safety-id", help="End-user safety identifier (max 64 chars)")

    # --- status ---
    # --- wait ---
    p_wait = subparsers.add_parser("wait", help="Wait for task completion and optionally download")
    p_wait.add_argument("task_id", help="Task ID")
    p_wait.add_argument("--interval", type=int, default=10, help="Poll interval in seconds (default: 10)")
    p_wait.add_argument("--download", help="Download directory for output files")

    # --- status ---
    p_status = subparsers.add_parser("status", help="Query task status and URLs")
    p_status.add_argument("task_id", help="Task ID")
    p_status.add_argument("--url-only", action="store_true",
                          help="Output only video URL and last_frame URL (one per line)")

    # --- list ---
    p_list = subparsers.add_parser("list", help="List video generation tasks")
    p_list.add_argument("--page", type=int, help="Page number (1-500)")
    p_list.add_argument("--page-size", type=int, help="Page size (1-500)")
    p_list.add_argument("--status", choices=["queued", "running", "cancelled", "succeeded", "failed", "expired"],
                        help="Filter by status")
    p_list.add_argument("--task-ids", nargs="+", help="Filter by task IDs")
    p_list.add_argument("--model", help="Filter by model ID")
    p_list.add_argument("--service-tier", choices=["default", "flex"], help="Filter by service tier")

    # --- delete ---
    p_delete = subparsers.add_parser("delete", help="Cancel or delete a task")
    p_delete.add_argument("task_id", help="Task ID")

    args = parser.parse_args()
    commands = {
        "create": cmd_create,
        "status": cmd_status,
        "wait": cmd_wait,
        "list": cmd_list,
        "delete": cmd_delete,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
