# 03_studio: OpenMontage Render Silo

This is your **Autonomous Local Render Node**. It lives inside WSL and uses your RTX 3060 to programmatically edit videos, strip out filler words, and overlay high-end "consulting-grade" graphics using Remotion.

It sits quietly and listens to the `01_evolution` Hub (via Firestore) for new jobs.

---

## 🎨 The Two Engines (Paint by Numbers)

This project has two distinct sides. Follow these simple instructions to launch whatever you need.

### 1. The Visual Editor (Remotion Canvas)
If you want to tweak the design of the Ken Burns effects, the Glass-morphism Data Overlays, or the Subtitles, you do that here.

**How to Start the Visuals:**
```bash
cd /home/evo/evo_01/03_studio/remotion-renderer
npm run start
```
*This opens a browser window where you can visually inspect and code the React animations.*

### 2. The Auto-Cutter (Python Worker)
This is the headless background worker. It uses `WhisperX` to find exact word boundaries, `Ollama` as the Director to decide what to cut, and `FFmpeg` to physically slice the video on your high-speed `S:\` drive.

**How to Start the Auto-Cutter:**
```bash
cd /home/evo/evo_01/03_studio
source .venv/bin/activate
python main.py
```
*Leave this running in a terminal. It will check your GPU, connect to Firebase, and instantly pick up any jobs sent from the Hub.*

---

## ⚙️ First-Time Setup Checklist

Before you run the worker for the very first time, ensure:
- [ ] Your `S:\` drive is mounted and available at `/mnt/s/studio_scratch`.
- [ ] You have placed your Google Cloud Service Account JSON file securely on your machine (e.g., `/home/evo/.env/service-account.json`).
- [ ] Your `.env` file in the `03_studio` root has the exact path to that JSON file in the `GOOGLE_APPLICATION_CREDENTIALS` variable.
- [ ] Local Ollama is running in the background with the `qwen3:14b` model ready.

---

## 📂 Architecture

```
03_studio/
├── data/                  → Symlink to /mnt/s/studio_scratch (Fast NVMe storage)
├── src/                   → Python Logic
│   ├── transcriber.py     → WhisperX audio analysis
│   ├── director.py        → Ollama narrative cutting logic
│   └── cutter.py          → FFmpeg hardware-accelerated splicing
├── remotion-renderer/     → React Visual Engine
│   └── src/components/    → Ken Burns & Glass-morphism React components
├── main.py                → The entry point that listens to Firestore
├── requirements.txt       → Python dependencies
└── .env                   → Firebase credentials
```
