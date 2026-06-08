# 03_studio Build Summary

## Current State: Operational ✅
The `03_studio` OpenMontage Render Silo is fully built and capable of end-to-end programmatic editing. The infrastructure has been established to run heavy AI models locally via the RTX 3060.

## Completed Integrations
- **GPU Pass-through:** `nvidia-smi` successfully detects the RTX 3060 in WSL. Hardware encoding (`h264_nvenc`) is wired directly into `cutter.py`.
- **Fast Storage:** `data/` is successfully symlinked to `/mnt/s/studio_scratch`, ensuring the C: drive is not bloated by 4K video rendering.
- **The Nervous System:** `main.py` is fully wired to Firestore, successfully polling the `jobs` collection.
- **Python Backend:** `.venv` is created, and all critical dependencies are installed (`whisperx`, `firebase-admin`, `requests`, `torch`).
- **Remotion Visuals:** Bypassed the interactive `create-video` CLI and manually constructed the `KenBurns` and `DataOverlay` cinematic React components.
- **Social Media Carousel:** Manually engineered the `SocialCarousel` composition using custom spring physics, typewriter character reveal loops, SVG path stroke-dashoffset circle drawing, staggered bento reveals, and outro color transitions/glow filters. Programmatically swiped via horizontal translations and successfully compiled the 1080x1080 square video at `out/social_carousel.mp4`.
- **Evolution Stables Headless Agentic Poster Engine:** Pivot to a 100% headless agentic pipeline. Built a Python wrapper CLI `just make-poster` that uses `gemini-3.5-flash` to parse natural language requests, automatically match jockey/horse imagery, and render double-resolution print-ready posters (2160x2700 PNG) headlessly using Remotion.
- **Premium Social Media Graphics (Prudentia Race Announcement):** Successfully compiled a gorgeous 1080x1350px (4:5) vertical poster announcing Prudentia's race at Te Rapa this Saturday. Overrode all default template gold-accent styles to use muted grey `#8E8E93` in `Poster.css`, satisfying the strict brand guideline of "Champagne Gold used only once (on the horse name)". Hand-configured fallback cursive typography (`Alex Brush`) to emulate Benedict script and aligned the layout using the classic single-event telemetry bar.

## What is Missing / Next Steps
- **GCS Download/Upload Logic:** `main.py` currently points to a placeholder local file (`raw_input.mp4`). The next feature phase will be to wire up the Google Cloud Storage (GCS) SDK to automatically download raw video, and upload the final stitched asset back to the cloud.
- **WhisperX Model Caching:** Be aware that the very first run of `main.py` will take a moment to download the WhisperX/Wav2Vec2 models to your local HuggingFace cache. 
