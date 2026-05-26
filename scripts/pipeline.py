#!/usr/bin/env python3
"""
Evolution Content Pipeline
Turns raw phone content into branded production clips.

Usage:
    python scripts/pipeline.py --input raw/prudentia_race.mp4 --output output/prudentia_reel.mp4 --format reel --title "Prudentia | Te Rapa | April 2026"

Formats:
    reel    - 1080x1920 vertical (TikTok/Reels)
    square  - 1080x1080 (Instagram)
    landscape - 1920x1080 (YouTube/Website)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Default paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent.resolve()
STUDIO_DIR = SCRIPT_DIR.parent
DEFAULT_LOGO = STUDIO_DIR / "assets/brand-kit/logos/lockups/lockup-horizontal-white.png"

# Format dimensions
FORMATS = {
    "reel": {"width": 1080, "height": 1920, "label": "Reel (9:16)"},
    "square": {"width": 1080, "height": 1080, "label": "Square (1:1)"},
    "landscape": {"width": 1920, "height": 1080, "label": "Landscape (16:9)"},
}

# Color grade: warm, slightly desaturated (Evolution gold tone)
COLOR_GRADE = "eq=contrast=1.05:saturation=0.85:brightness=0.02"

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_info(path):
    """Get width, height, duration of input video."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-show_entries", "format=duration",
        "-of", "csv=s=x:p=0",
        str(path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return None, None, None
    dims = lines[0].split("x")
    width = int(dims[0]) if dims[0].isdigit() else None
    height = int(dims[1]) if len(dims) > 1 and dims[1].isdigit() else None
    duration = float(lines[1]) if lines[1].replace(".","").isdigit() else None
    return width, height, duration

def build_filter_complex(input_w, input_h, target_w, target_h, logo_path, title_text, duration):
    """
    Build ffmpeg filter_complex string for:
    - Format crop/pad
    - Color grade
    - Logo watermark
    - Title overlay
    """
    # Scale and crop to target format (center crop)
    # If input is already target aspect, just scale. If not, crop center.
    target_aspect = target_w / target_h
    input_aspect = input_w / input_h

    if abs(input_aspect - target_aspect) < 0.01:
        # Same aspect ratio, just scale
        scale_filter = f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease"
    else:
        # Need to crop or pad
        if input_aspect > target_aspect:
            # Input is wider, crop sides
            new_w = int(input_h * target_aspect)
            crop_filter = f"crop={new_w}:{input_h}"
            scale_filter = f"{crop_filter},scale={target_w}:{target_h}"
        else:
            # Input is taller, crop top/bottom
            new_h = int(input_w / target_aspect)
            crop_filter = f"crop={input_w}:{new_h}"
            scale_filter = f"{crop_filter},scale={target_w}:{target_h}"

    # Color grade
    graded = f"{scale_filter},{COLOR_GRADE}"

    # Logo overlay (bottom-right, 15% opacity)
    # Logo size: 20% of width
    logo_w = int(target_w * 0.20)
    logo_x = target_w - logo_w - 30
    logo_y = target_h - int(logo_w * 0.3) - 30
    logo_overlay = f"[{graded}][1:v]overlay={logo_x}:{logo_y}:format=auto,format=yuv420p"

    # Title text overlay (top-left or bottom-left)
    # Use drawtext filter
    font_size = int(target_w * 0.04)
    text_x = 40
    text_y = target_h - 120
    title_overlay = f"drawtext=text='{title_text}':fontsize={font_size}:fontcolor=white@0.9:x={text_x}:y={text_y}:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black@0.5:boxborderw=10"

    # Combine: color grade -> logo -> title
    # Actually we need to do it in stages with split if using filter_complex properly
    # Simpler approach: chain filters
    final_filter = f"{scale_filter},{COLOR_GRADE},drawtext=text='{title_text}':fontsize={font_size}:fontcolor=white@0.9:x={text_x}:y={text_y}:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black@0.5:boxborderw=10"

    return final_filter

def process_video(input_path, output_path, format_name, title_text, logo_path, trim=None):
    """Main processing function."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return False

    target = FORMATS.get(format_name)
    if not target:
        print(f"ERROR: Unknown format '{format_name}'. Use: reel, square, landscape")
        return False

    # Get input info
    width, height, duration = get_video_info(input_path)
    if not width or not height:
        print("ERROR: Could not read input video info")
        return False

    print(f"Input: {width}x{height}, {duration:.1f}s")
    print(f"Target: {target['label']} ({target['width']}x{target['height']})")
    print(f"Title: {title_text}")

    # Build ffmpeg command
    target_w, target_h = target["width"], target["height"]

    # Build scale/crop filter
    target_aspect = target_w / target_h
    input_aspect = width / height

    if abs(input_aspect - target_aspect) < 0.01:
        vf = f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,setsar=1"
    elif input_aspect > target_aspect:
        new_w = int(height * target_aspect)
        vf = f"crop={new_w}:{height},scale={target_w}:{target_h},setsar=1"
    else:
        new_h = int(width / target_aspect)
        vf = f"crop={width}:{new_h},scale={target_w}:{target_h},setsar=1"

    # Add color grade
    vf += f",eq=contrast=1.05:saturation=0.85:brightness=0.02"

    # Add title text
    font_size = max(24, int(target_w * 0.035))
    text_y = target_h - int(font_size * 2.5)
    vf += f",drawtext=text='{title_text}':fontsize={font_size}:fontcolor=white@0.85:x=40:y={text_y}:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black@0.4:boxborderw=8"

    # Add logo if provided and exists
    logo_filter = ""
    if logo_path and Path(logo_path).exists():
        logo_w = int(target_w * 0.18)
        logo_x = target_w - logo_w - 25
        logo_y = target_h - int(logo_w * 0.25) - 25
        # Logo needs to be a separate input stream
        # We'll use -i for logo and overlay in filter_complex
        pass  # Handle below

    # Build command
    cmd = ["ffmpeg", "-y"]

    # Trim options
    if trim:
        start, end = trim
        cmd += ["-ss", str(start), "-to", str(end)]

    # Input video
    cmd += ["-i", str(input_path)]

    # Logo input and filter
    has_logo = False
    if logo_path and Path(logo_path).exists():
        has_logo = True
        cmd += ["-i", str(logo_path)]
        # Calculate logo position
        logo_w = int(target_w * 0.18)
        logo_x = target_w - logo_w - 25
        logo_y = target_h - int(logo_w * 0.25) - 25
        # Build filter chain with overlay
        vf = f"[0:v]{vf}[v];[1:v]scale={logo_w}:-1:flags=lanczos[logo];[v][logo]overlay={logo_x}:{logo_y}:format=auto[vout]"
    else:
        # No logo, just use video filter directly
        vf = f"[0:v]{vf}[v]"
        # But ffmpeg -vf doesn't accept stream labels, so just use the chain
        pass

    # Audio: keep original, normalize slightly
    cmd += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"]

    # Video codec settings
    cmd += [
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
    ]

    # Add video filter
    if has_logo:
        cmd += ["-filter_complex", vf]
        # Map the output of the filter_complex
        cmd += ["-map", "[vout]", "-map", "0:a"]
    else:
        # Simple -vf filter (strip stream labels)
        simple_vf = vf.replace("[0:v]", "").replace("[v]", "").strip()
        # Remove leading/trailing commas
        simple_vf = simple_vf.strip(",")
        cmd += ["-vf", simple_vf]

    cmd += [str(output_path)]

    print(f"\nRunning: {' '.join(cmd)}")
    print("Processing...")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: ffmpeg failed")
        print(result.stderr[-500:])  # Last 500 chars of error
        return False

    # Verify output
    out_w, out_h, out_dur = get_video_info(output_path)
    if out_w and out_h:
        print(f"\nDone: {output_path}")
        print(f"Output: {out_w}x{out_h}, {out_dur:.1f}s")
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"Size: {size_mb:.1f} MB")
        return True
    else:
        print("ERROR: Output file is invalid")
        return False

def main():
    parser = argparse.ArgumentParser(description="Evolution Content Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Input video file path")
    parser.add_argument("--output", "-o", required=True, help="Output video file path")
    parser.add_argument("--format", "-f", default="reel", choices=["reel", "square", "landscape"], help="Output format")
    parser.add_argument("--title", "-t", default="", help="Title text overlay")
    parser.add_argument("--logo", "-l", default=str(DEFAULT_LOGO) if DEFAULT_LOGO.exists() else None, help="Logo image path")
    parser.add_argument("--trim", help="Trim to start,end in seconds (e.g. 5,25)")

    args = parser.parse_args()

    if not check_ffmpeg():
        print("ERROR: ffmpeg not found. Install it first.")
        sys.exit(1)

    trim = None
    if args.trim:
        try:
            parts = args.trim.split(",")
            trim = (float(parts[0]), float(parts[1]))
        except (ValueError, IndexError):
            print("ERROR: Trim format is start,end (e.g. 5,25)")
            sys.exit(1)

    success = process_video(args.input, args.output, args.format, args.title, args.logo, trim)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
