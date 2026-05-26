#!/usr/bin/env python3
"""
Evolution Stables — Social Media Post Template Generator
Generates branded square/vertical static cards for pre-race updates,
race results, nominations, etc.

Usage:
    python3 produce_post.py \
        --type pre_race \
        --horse "Prudentia" \
        --jockey "Joe Kamaruddin" \
        --trainer "Andrew Forsman" \
        --race "R7" \
        --venue "Te Rapa" \
        --date "Saturday 31 May 2026" \
        --photo /path/to/horse.jpg \
        --out /path/to/output.jpg

Types: pre_race, race_result, nominated, syndicate_open
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ── Brand constants ───────────────────────────────────────────────
W, H = 1080, 1350            # Instagram portrait (4:5) — good for feed + stories
BRAND_BLACK = "#1C1C1E"
BRAND_GOLD  = "#C9A227"
BRAND_WHITE = "#FFFFFF"
BRAND_DARK_GRAY = "#2C2C2E"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_MAIN = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
FONT_SUB  = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_COND = os.path.join(FONT_DIR, "DejaVuSansCondensed-Bold.ttf")

LOGO_PATH = "/home/evo/evo_01/02_website/public/images/Evolution-Stables-Logo-White.png"

# ── Helpers ───────────────────────────────────────────────────────
def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def fit_text(draw, text, font_path, max_w, start_size=120, min_size=40):
    """Shrink font until text fits max_w width."""
    size = start_size
    while size >= min_size:
        font = load_font(font_path, size)
        w, h = text_size(draw, text, font)
        if w <= max_w:
            return font, w, h
        size -= 4
    font = load_font(font_path, min_size)
    w, h = text_size(draw, text, font)
    return font, w, h

def gradient_bg(img, top_color, bottom_color):
    """Draw vertical gradient."""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def add_logo(img, box, opacity=255):
    """Paste logo into a region, scaling to fit."""
    if not os.path.exists(LOGO_PATH):
        return
    logo = Image.open(LOGO_PATH).convert("RGBA")
    bx, by, bw, bh = box
    # Scale logo preserving aspect ratio
    lw, lh = logo.size
    scale = min(bw / lw, bh / lh)
    new_w, new_h = int(lw * scale), int(lh * scale)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)
    # Center in box
    px = bx + (bw - new_w) // 2
    py = by + (bh - new_h) // 2
    if opacity < 255:
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity / 255))
        logo.putalpha(alpha)
    img.paste(logo, (px, py), logo)

def round_rect(draw, xy, radius, fill):
    """Draw rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

# ── Template builders ─────────────────────────────────────────────
def build_pre_race(args):
    img = Image.new("RGB", (W, H))
    top_rgb = hex_to_rgb(BRAND_BLACK)
    bot_rgb = hex_to_rgb(BRAND_DARK_GRAY)
    gradient_bg(img, top_rgb, bot_rgb)
    draw = ImageDraw.Draw(img)

    margin = 60
    y = 50

    # ── Top-right logo ──
    add_logo(img, (W - 220, 30, 200, 100), opacity=220)

    # ── Date line ──
    font_date = load_font(FONT_SUB, 28)
    draw.text((margin, y), args.date.upper(), font=font_date, fill=BRAND_GOLD)
    _, dh = text_size(draw, args.date.upper(), font_date)
    y += dh + 10

    # ── Headline: "RACING TODAY" ──
    font_head, hw, hh = fit_text(draw, "RACING TODAY.", FONT_COND, W - margin * 2, 110, 60)
    draw.text((margin, y), "RACING TODAY.", font=font_head, fill=BRAND_WHITE)
    y += hh + 5

    # ── Venue / context line ──
    venue_text = f"{args.venue.upper()}  |  {args.race.upper()}"
    font_venue = load_font(FONT_SUB, 36)
    draw.text((margin, y), venue_text, font=font_venue, fill=BRAND_WHITE)
    _, vh = text_size(draw, venue_text, font_venue)
    y += vh + 40

    # ── Gold separator line ──
    draw.rectangle([margin, y, W - margin, y + 4], fill=BRAND_GOLD)
    y += 30

    # ── Horse name bar ──
    bar_h = 90
    round_rect(draw, [margin, y, W - margin, y + bar_h], 10, BRAND_GOLD)
    font_horse, _, _ = fit_text(draw, args.horse.upper(), FONT_MAIN, W - margin * 2 - 40, 80, 50)
    _, th = text_size(draw, args.horse.upper(), font_horse)
    ty = y + (bar_h - th) // 2
    draw.text((margin + 20, ty), args.horse.upper(), font=font_horse, fill=BRAND_BLACK)
    y += bar_h + 20

    # ── Jockey & Trainer row ──
    font_detail = load_font(FONT_SUB, 32)
    detail_text = f"Jockey: {args.jockey}    Trainer: {args.trainer}"
    draw.text((margin, y), detail_text, font=font_detail, fill=BRAND_WHITE)
    _, dh = text_size(draw, detail_text, font_detail)
    y += dh + 30

    # ── Horse photo ──
    photo_h = H - y - margin - 80  # leave room for bottom logo
    if args.photo and os.path.exists(args.photo):
        photo = Image.open(args.photo).convert("RGB")
        pw, ph = photo.size
        # Crop to aspect ratio of target box
        target_ar = (W - margin * 2) / photo_h
        src_ar = pw / ph
        if src_ar > target_ar:
            # Source is wider — crop width
            new_w = int(ph * target_ar)
            left = (pw - new_w) // 2
            photo = photo.crop((left, 0, left + new_w, ph))
        else:
            # Source is taller — crop height
            new_h = int(pw / target_ar)
            top = (ph - new_h) // 2
            photo = photo.crop((0, top, pw, top + new_h))
        photo = photo.resize((W - margin * 2, photo_h), Image.LANCZOS)
        # Optional: subtle vignette / dark overlay for text readability
        img.paste(photo, (margin, y))
        # Slight dark overlay at top of photo for contrast if we add text there
    else:
        # Placeholder dark box with gold border
        draw.rectangle([margin, y, W - margin, y + photo_h], outline=BRAND_GOLD, width=2)
        font_ph = load_font(FONT_SUB, 40)
        msg = "[ HORSE PHOTO ]"
        pw, ph = text_size(draw, msg, font_ph)
        draw.text(((W - pw) // 2, y + photo_h // 2 - ph // 2), msg, font=font_ph, fill=BRAND_GOLD)

    # ── Bottom logo strip ──
    add_logo(img, (W - 200, H - 90, 160, 60), opacity=180)
    font_url = load_font(FONT_SUB, 20)
    draw.text((margin, H - 50), "evolutionstables.nz", font=font_url, fill=BRAND_GOLD)

    return img


def build_race_result(args):
    """Race result card — adds result banner (WINNER / PLACED / UNPLACED)"""
    img = build_pre_race(args)
    draw = ImageDraw.Draw(img)

    # Overlay result banner at top center
    banner_h = 70
    banner_w = 360
    bx = (W - banner_w) // 2
    by = 180

    result = getattr(args, "result", "WINNER").upper()
    if result == "WINNER":
        banner_color = "#22C55E"  # green
    elif result == "PLACED":
        banner_color = BRAND_GOLD
    else:
        banner_color = "#6B7280"  # gray

    draw.rounded_rectangle([bx, by, bx + banner_w, by + banner_h], radius=10, fill=banner_color)
    font_res = load_font(FONT_MAIN, 44)
    rw, rh = text_size(draw, result, font_res)
    draw.text((bx + (banner_w - rw) // 2, by + (banner_h - rh) // 2), result, font=font_res, fill=BRAND_BLACK)

    return img


def build_nominated(args):
    """Nomination announcement — simpler, just horse + date + venue"""
    img = Image.new("RGB", (W, H))
    top_rgb = hex_to_rgb(BRAND_BLACK)
    bot_rgb = hex_to_rgb(BRAND_DARK_GRAY)
    gradient_bg(img, top_rgb, bot_rgb)
    draw = ImageDraw.Draw(img)

    margin = 60
    y = 50

    add_logo(img, (W - 220, 30, 200, 100), opacity=220)

    font_date = load_font(FONT_SUB, 28)
    draw.text((margin, y), args.date.upper(), font=font_date, fill=BRAND_GOLD)
    _, dh = text_size(draw, args.date.upper(), font_date)
    y += dh + 20

    font_head, _, hh = fit_text(draw, "NOMINATED", FONT_COND, W - margin * 2, 120, 70)
    draw.text((margin, y), "NOMINATED", font=font_head, fill=BRAND_WHITE)
    y += hh + 10

    venue_text = f"{args.venue.upper()}  |  {args.race.upper()}"
    font_venue = load_font(FONT_SUB, 36)
    draw.text((margin, y), venue_text, font=font_venue, fill=BRAND_WHITE)
    _, vh = text_size(draw, venue_text, font_venue)
    y += vh + 40

    draw.rectangle([margin, y, W - margin, y + 4], fill=BRAND_GOLD)
    y += 30

    bar_h = 100
    round_rect(draw, [margin, y, W - margin, y + bar_h], 10, BRAND_GOLD)
    font_horse, _, _ = fit_text(draw, args.horse.upper(), FONT_MAIN, W - margin * 2 - 40, 90, 60)
    _, th = text_size(draw, args.horse.upper(), font_horse)
    ty = y + (bar_h - th) // 2
    draw.text((margin + 20, ty), args.horse.upper(), font=font_horse, fill=BRAND_BLACK)
    y += bar_h + 30

    font_detail = load_font(FONT_SUB, 32)
    detail = f"Jockey: {args.jockey}    Trainer: {args.trainer}"
    draw.text((margin, y), detail, font=font_detail, fill=BRAND_WHITE)
    _, dh = text_size(draw, detail, font_detail)
    y += dh + 30

    # Photo
    photo_h = H - y - margin - 80
    if args.photo and os.path.exists(args.photo):
        photo = Image.open(args.photo).convert("RGB")
        pw, ph = photo.size
        target_ar = (W - margin * 2) / photo_h
        src_ar = pw / ph
        if src_ar > target_ar:
            new_w = int(ph * target_ar)
            left = (pw - new_w) // 2
            photo = photo.crop((left, 0, left + new_w, ph))
        else:
            new_h = int(pw / target_ar)
            top = (ph - new_h) // 2
            photo = photo.crop((0, top, pw, top + new_h))
        photo = photo.resize((W - margin * 2, photo_h), Image.LANCZOS)
        img.paste(photo, (margin, y))
    else:
        draw.rectangle([margin, y, W - margin, y + photo_h], outline=BRAND_GOLD, width=2)
        font_ph = load_font(FONT_SUB, 40)
        msg = "[ HORSE PHOTO ]"
        pw, ph = text_size(draw, msg, font_ph)
        draw.text(((W - pw) // 2, y + photo_h // 2 - ph // 2), msg, font=font_ph, fill=BRAND_GOLD)

    add_logo(img, (W - 200, H - 90, 160, 60), opacity=180)
    font_url = load_font(FONT_SUB, 20)
    draw.text((margin, H - 50), "evolutionstables.nz", font=font_url, fill=BRAND_GOLD)

    return img


# ── Main ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Evolution Stables Social Post Generator")
    parser.add_argument("--type",    required=True, choices=["pre_race", "race_result", "nominated", "syndicate_open"])
    parser.add_argument("--horse",   required=True)
    parser.add_argument("--jockey",  default="TBC")
    parser.add_argument("--trainer", default="TBC")
    parser.add_argument("--race",    default="R1")
    parser.add_argument("--venue",   default="TBC")
    parser.add_argument("--date",    default="TBC")
    parser.add_argument("--photo",   default="")
    parser.add_argument("--result",  default="WINNER", help="For race_result type: WINNER, PLACED, UNPLACED")
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)

    if args.type == "pre_race":
        img = build_pre_race(args)
    elif args.type == "race_result":
        img = build_race_result(args)
    elif args.type == "nominated":
        img = build_nominated(args)
    else:
        # syndicate_open — placeholder for now
        img = build_pre_race(args)

    img.save(args.out, "JPEG", quality=95)
    print(f"Saved: {args.out}  ({W}x{H})")

if __name__ == "__main__":
    main()
