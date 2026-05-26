# Evolution Content Pipeline

## What This Is

Caveman tool for turning your raw phone content into production-ready social clips with Evolution brand overlay.

## How It Works

1. **Drop raw content** in `~/evo_01/03_studio/raw/` (manually copy from Google Drive or phone)
2. **Run the script** — it applies brand overlays, cuts formats, adds intro/outro
3. **Get production clips** in `~/evo_01/03_studio/output/`

## Pipeline Steps

### Step 1: Source
- Raw phone video/photos from Google Drive folders
- Copy to `raw/` directory (don't link — actual files)

### Step 2: Brand Overlay
- Evolution logo watermark (bottom-right corner, 15% opacity)
- Color grade: warm, slightly desaturated (Evolution gold tone)
- Subtle vignette (darken edges, focus on horse)

### Step 3: Social Formats
- **Reels/TikTok:** 1080x1920 vertical, 15-60 seconds
- **Instagram Square:** 1080x1080, 15-30 seconds
- **YouTube/Landing:** 1920x1080 landscape, 30-90 seconds

### Step 4: Intro/Outro Cards
- 2-second intro: Black screen + "EVOLUTION STABLES" wordmark fade-in
- 1-second outro: "Join the stable. evolutionstables.nz" + logo

## Quick Start

```bash
cd ~/evo_01/03_studio
python3 scripts/pipeline.py --input raw/prudentia_race.mp4 --output output/prudentia_reel.mp4 --format reel --title "Prudentia | Te Rapa | April 2026"
```

## Files You Need

| File | Purpose |
|------|---------|
| `raw/` | Put your phone video/photos here |
| `assets/brand-kit/logos/` | Logo files for watermark |
| `assets/brand-kit/colors/` | Color palette for grading |
| `output/` | Finished clips appear here |

## Next: Automated Download

I'll add a Google Drive download script so you don't have to manually copy files.
