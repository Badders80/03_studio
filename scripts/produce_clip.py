#!/usr/bin/env python3
"""
Evolution Stables Production Clip Builder
Creates branded social reels with intro, transitions, title overlays, logo watermark.
Output: 1080x1920 vertical MP4
"""
import os, sys, argparse, subprocess, tempfile, json

REEL_W, REEL_H = 1080, 1920
LOGO_PATH = '/home/evo/evo_01/02_website/public/images/Evolution-Stables-Logo-White.png'
NAME_LOGO_PATH = '/home/evo/evo_01/02_website/public/images/Evolution-Stables-Name-Logo-White.svg'
BRAND_BLACK = "#050301"
BRAND_GOLD = "#C5A059"

def run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}\nSTDERR: {result.stderr}")
        raise RuntimeError(result.stderr)
    return result

def get_media_info(path):
    """Returns (width, height, duration, has_audio)"""
    r = run(f'ffprobe -v error -show_entries stream=codec_type,width,height -show_entries format=duration '
            f'-of json "{path}"', check=True)
    data = json.loads(r.stdout)
    fmt = data.get('format', {})
    streams = data.get('streams', [])
    w, h, dur = 0, 0, float(fmt.get('duration', 0))
    has_audio = any(s.get('codec_type') == 'audio' for s in streams)
    for s in streams:
        if s.get('codec_type') == 'video':
            w = int(s.get('width', 0))
            h = int(s.get('height', 0))
            break
    return w, h, dur, has_audio

def create_branded_intro(intro_duration=3.0, text="EVOLUTION STABLES", subtitle=""):
    """Create a black intro with centered logo + text."""
    tmpdir = tempfile.mkdtemp()
    intro_path = os.path.join(tmpdir, "intro.mp4")

    # Use ffmpeg to generate the intro directly at exact resolution
    # Black background with logo overlay + text via drawtext
    logo_w = int(REEL_W * 0.40)
    logo_x = (REEL_W - logo_w) // 2
    logo_y = int(REEL_H * 0.35)

    safe_text = text.replace("'", "\\\\'")
    text_y = int(REEL_H * 0.60)

    subtitle_filter = ""
    if subtitle:
        safe_sub = subtitle.replace("'", "\\\\'")
        subtitle_filter = f", drawtext=text='{safe_sub}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=28:fontcolor={BRAND_GOLD}:x=(w-text_w)/2:y={int(REEL_H*0.68)}"

    cmd = (
        f"ffmpeg -y -f lavfi -i color=c={BRAND_BLACK}:s={REEL_W}x{REEL_H}:d={intro_duration}:r=30 "
        f"-i {LOGO_PATH} "
        f"-filter_complex \""
        f"[1:v]scale={logo_w}:-1[logo]; "
        f"[0:v][logo]overlay={logo_x}:{logo_y}[tmp]; "
        f"[tmp]drawtext=text='{safe_text}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y={text_y}"
        f"{subtitle_filter}[vout]\" "
        f"-map [vout] -c:v libx264 -pix_fmt yuv420p -r 30 -t {intro_duration} "
        f"'{intro_path}'"
    )
    run(cmd)
    return intro_path

def normalize_to_reel(input_path, output_path, title="", duration=None):
    """Normalize any video to 1080x1920 vertical with logo watermark + optional title."""
    w, h, dur, has_audio = get_media_info(input_path)
    if duration:
        dur = min(dur, duration)

    # Determine scale/crop based on input aspect ratio
    if w >= h:
        # Landscape: scale height to REEL_H, crop width to REEL_W, center
        vf = f"scale=-1:{REEL_H},crop={REEL_W}:{REEL_H}:(in_w-{REEL_W})/2:0,setsar=1"
    elif w / h < 0.5:
        # Very tall vertical: scale width to REEL_W, pad if needed
        vf = f"scale={REEL_W}:-1,pad={REEL_W}:{REEL_H}:0:(oh-{REEL_H})/2:black,setsar=1"
    else:
        # Portrait-ish: scale width to REEL_W, crop height to REEL_H, center
        vf = f"scale={REEL_W}:-1,crop={REEL_W}:{REEL_H}:0:(in_h-{REEL_H})/2,setsar=1"

    # Logo watermark (bottom right, 18% width, padding 40px)
    logo_w = int(REEL_W * 0.18)
    logo_x = REEL_W - logo_w - 40
    logo_y = REEL_H - int(logo_w * 0.3) - 40

    logo_overlay = f"[0:v]{vf}[scaled];[1:v]scale={logo_w}:-1[logo];[scaled][logo]overlay={logo_x}:{logo_y}:enable='between(t,0,{dur})'[v1]"

    # Title overlay (bottom left, semi-transparent box + white text)
    if title:
        safe_title = title.replace("'", "\\'")
        title_overlay = (
            f"[v1]drawtext=text='{safe_title}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            f"fontsize=32:fontcolor=white:x=20:y=(h-60):box=1:boxcolor=black@0.7:boxborderw=15[vout]"
        )
    else:
        title_overlay = "[v1]copy[vout]"

    # Audio handling
    audio_map = "-map 0:a -c:a aac -b:a 128k" if has_audio else ""

    # Single pass: input (0), logo image (1)
    cmd = (
        f"ffmpeg -y -i \"{input_path}\" -i {LOGO_PATH} "
        f"-filter_complex \"{logo_overlay};{title_overlay}\" "
        f"-map [vout] {audio_map} "
        f"-c:v libx264 -pix_fmt yuv420p -r 30 -t {dur} "
        f"\"{output_path}\""
    )
    run(cmd)
    return output_path

def simple_concat(intro_path, body_path, output_path):
    """Concat intro + body with re-encode (handles mixed resolutions/audio)."""
    listfile = output_path + '.concat.txt'
    with open(listfile, 'w') as f:
        f.write(f"file '{intro_path}'\n")
        f.write(f"file '{body_path}'\n")
    cmd = (
        f'ffmpeg -y -f concat -safe 0 -i {listfile} '
        f'-c:v libx264 -pix_fmt yuv420p -r 30 '
        f'-c:a aac -b:a 128k '
        f'-movflags +faststart '
        f'"{output_path}"'
    )
    run(cmd)
    os.remove(listfile)
    return output_path

def build_clip(name, input_path, title, output_path, intro_text="EVOLUTION STABLES", intro_subtitle="", intro_duration=3.0):
    print(f"\n=== BUILDING: {name} ===")
    print(f"  Input: {input_path}")

    print("  [1/4] Creating branded intro...")
    intro_path = create_branded_intro(intro_duration, intro_text, intro_subtitle)

    print("  [2/4] Normalizing body footage...")
    body_norm = output_path + '.body_norm.mp4'
    normalize_to_reel(input_path, body_norm, title)

    print("  [3/4] Concatenating intro + body...")
    simple_concat(intro_path, body_norm, output_path)

    print("  [4/4] Cleaning up...")
    os.remove(intro_path)
    os.remove(body_norm)

    w, h, dur, _ = get_media_info(output_path)
    print(f"  [DONE] {output_path}")
    print(f"         Resolution: {w}x{h} | Duration: {dur:.1f}s")
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--title', default='')
    parser.add_argument('--intro-text', default='EVOLUTION STABLES')
    parser.add_argument('--intro-subtitle', default='')
    parser.add_argument('--intro-duration', type=float, default=3.0)
    args = parser.parse_args()

    build_clip(
        name=os.path.basename(args.output),
        input_path=args.input,
        title=args.title,
        output_path=args.output,
        intro_text=args.intro_text,
        intro_subtitle=args.intro_subtitle,
        intro_duration=args.intro_duration
    )
