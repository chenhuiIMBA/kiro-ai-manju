#!/usr/bin/env python3
"""
Seedream 5.0 图片生成 CLI（火山方舟 Ark API）

用法:
  python3 seedream.py create -p "描述" [options]
  python3 seedream.py create -p "描述" -i ref.png [options]
  python3 seedream.py create -p "描述" -i img1.png img2.png --seq auto --max-images 5
  python3 seedream.py create -p "描述" --size 2K --web-search
  python3 seedream.py models

环境变量:
  ARK_API_KEY - 火山方舟 API Key（与 Seedance 共用）
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


BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_MODEL = "doubao-seedream-5-0-260128"

MODELS = {
    "5.0": "doubao-seedream-5-0-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4.0": "doubao-seedream-4-0-250828",
    "3.0": "doubao-seedream-3-0-t2i-250415",
}

SIZE_PRESETS = {
    "2K": {
        "1:1": "2048x2048", "4:3": "2304x1728", "3:4": "1728x2308",
        "16:9": "2848x1600", "9:16": "1600x2848", "3:2": "2496x1664",
        "2:3": "1664x2496", "21:9": "3136x1344",
    },
    "3K": {
        "1:1": "3072x3072", "4:3": "3456x2592", "3:4": "2592x3456",
        "16:9": "4096x2304", "9:16": "2304x4096", "3:2": "3744x2496",
        "2:3": "2496x3744", "21:9": "4704x2016",
    },
}

VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024


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
        with urllib.request.urlopen(req, timeout=180) as resp:
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
    if ext not in VALID_IMAGE_EXTS:
        print(f"Error: Unsupported image format: {ext}", file=sys.stderr)
        sys.exit(1)
    if path.stat().st_size > MAX_IMAGE_SIZE:
        print(f"Error: File too large ({path.stat().st_size} bytes, max {MAX_IMAGE_SIZE}): {filepath}", file=sys.stderr)
        sys.exit(1)
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def resolve_image(image_input):
    if image_input.startswith("http://") or image_input.startswith("https://"):
        return image_input
    if image_input.startswith("data:"):
        return image_input
    return file_to_data_url(image_input)


def parse_bool(v):
    if isinstance(v, bool):
        return v
    s = str(v).lower()
    if s in ("true", "1", "yes"):
        return True
    if s in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean value expected, got: {v}")


def resolve_size(size_input):
    """Resolve size input: preset (2K/3K), ratio (16:9), or WxH."""
    if not size_input:
        return None

    # Direct resolution presets
    upper = size_input.upper()
    if upper in SIZE_PRESETS:
        return upper

    # WxH format
    if "x" in size_input.lower():
        return size_input

    # Ratio shorthand - map to 2K default
    ratio_map = {
        "1:1": "2048x2048", "4:3": "2304x1728", "3:4": "1728x2308",
        "16:9": "2848x1600", "9:16": "1600x2848", "3:2": "2496x1664",
        "2:3": "1664x2496", "21:9": "3136x1344",
    }
    if size_input in ratio_map:
        return ratio_map[size_input]

    return size_input


def download_image(image_url, download_dir, prefix="image"):
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    filepath = download_path / f"{prefix}_{timestamp}.jpg"
    print(f"  Downloading to {filepath} ...")
    urllib.request.urlretrieve(image_url, str(filepath))
    print(f"  Saved: {filepath}")
    return str(filepath)


def cmd_create(args):
    # Resolve model
    model_id = MODELS.get(args.model, args.model)

    body = {
        "model": model_id,
        "prompt": args.prompt,
    }

    # Image input
    if args.image:
        images = args.image
        if len(images) == 1:
            body["image"] = resolve_image(images[0])
        else:
            body["image"] = [resolve_image(img) for img in images]

    # Size
    size = resolve_size(args.size)
    if size:
        body["size"] = size

    # Seed (only for 3.0)
    if args.seed is not None:
        body["seed"] = args.seed

    # Sequential image generation (组图)
    if args.seq:
        body["sequential_image_generation"] = args.seq
        if args.max_images is not None:
            body["sequential_image_generation_options"] = {"max_images": args.max_images}

    # Web search
    if args.web_search:
        body["tools"] = [{"type": "web_search"}]

    # Stream
    if args.stream:
        body["stream"] = True

    # Output format
    if args.format:
        body["output_format"] = args.format

    # Response format
    if args.response_format:
        body["response_format"] = args.response_format

    # Watermark
    if args.watermark is not None:
        body["watermark"] = args.watermark

    # Optimize prompt
    if args.optimize_prompt:
        body["optimize_prompt_options"] = {"mode": args.optimize_prompt}

    result = api_request("POST", BASE_URL, body)

    # Check for request-level error
    if result.get("error"):
        err = result["error"]
        print(f"Error: {err.get('code', '')} - {err.get('message', '')}", file=sys.stderr)
        sys.exit(1)

    # Display results
    model_name = result.get("model", "")
    created = result.get("created", 0)
    print(f"Model:  {model_name}")
    print(f"Time:   {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created))}")

    data = result.get("data", [])
    success_count = 0
    for i, item in enumerate(data):
        if item.get("error"):
            err = item["error"]
            print(f"  Image {i+1} failed: {err.get('code', '')} - {err.get('message', '')}")
            continue
        success_count += 1
        url = item.get("url", "")
        b64 = item.get("b64_json", "")
        size = item.get("size", "")
        print(f"  Image {i+1}: size={size}")
        if url:
            print(f"    URL: {url}")
            if args.download:
                download_image(url, args.download, prefix=f"seedream_{i+1}")
        if b64 and not url:
            print(f"    Base64: {b64[:100]}...")

    usage = result.get("usage", {})
    if usage:
        print(f"Usage:   {usage.get('generated_images', success_count)} image(s), "
              f"{usage.get('output_tokens', 0)} tokens")
    if not args.download and not args.no_download:
        print("\nTip: Use --download DIR to save images locally.")

    # Print tools usage if present
    tools = result.get("tools", [])
    if tools:
        for tool in tools:
            print(f"Tool:    {tool.get('type', '')}")
    tool_usage = (usage or {}).get("tool_usage", {})
    if tool_usage.get("web_search"):
        print(f"Web search calls: {tool_usage['web_search']}")


def cmd_models(args):
    print("Available Seedream models:\n")
    print(f"{'Alias':<6} {'Model ID':<40} {'Note'}")
    print("-" * 80)
    for alias, model_id in MODELS.items():
        note = " <-- default" if alias == "5.0" else ""
        print(f"{alias:<6} {model_id:<40}{note}")


def main():
    parser = argparse.ArgumentParser(
        description="Seedream Image Generation CLI (Volcengine Ark API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- create ---
    p_create = subparsers.add_parser("create", help="Generate image(s)")
    p_create.add_argument("-p", "--prompt", required=True, help="Text prompt (Chinese/English)")
    p_create.add_argument("-i", "--image", nargs="+", help="Reference image(s) (local path or URL, max 14)")
    p_create.add_argument("-m", "--model", default="5.0",
                          help=f"Model alias or ID: {', '.join(MODELS.keys())} (default: 5.0)")
    p_create.add_argument("--size", help="Size: 2K/3K, ratio (16:9), or WxH (2048x2048)")
    p_create.add_argument("--seed", type=int, help="Random seed (only 3.0-t2i)")
    p_create.add_argument("--seq", choices=["auto", "disabled"], default=None,
                          help="Sequential image generation: auto=group images, disabled=single (default: disabled)")
    p_create.add_argument("--max-images", type=int, help="Max images for seq mode (1-15, default 15)")
    p_create.add_argument("--web-search", action="store_true", help="Enable web search (5.0 only)")
    p_create.add_argument("--stream", action="store_true", help="Enable streaming output")
    p_create.add_argument("--format", choices=["png", "jpeg"], help="Output format (5.0 only, default: jpeg)")
    p_create.add_argument("--response-format", choices=["url", "b64_json"], default="url",
                          help="Response format (default: url)")
    p_create.add_argument("--watermark", type=parse_bool, default=False, help="Add watermark (default: false)")
    p_create.add_argument("--optimize-prompt", choices=["standard", "fast"],
                          help="Prompt optimization mode (5.0/4.5/4.0)")
    p_create.add_argument("-d", "--download", help="Download directory for output images")
    p_create.add_argument("--no-download", action="store_true", help="Don't download, only print URLs")

    # --- models ---
    p_models = subparsers.add_parser("models", help="List available models")

    args = parser.parse_args()
    commands = {
        "create": cmd_create,
        "models": cmd_models,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
