# 03_studio — Live State

**Last updated:** 2026-07-13 (session protocol: continue.md + STATE.md)
**Canonical for agents:** yes — this file + [`README.md`](README.md) are the only required reads for most sessions.

---

## Agent boot (island protocol)

| Order | File | Role |
|-------|------|------|
| **1** | [`continue.md`](continue.md) | **Next action** — overwrite every session wrap |
| **2** | This file (`STATE.md`) | **Current truth** — architecture, live, remaining work |

**Start:** read continue → this file → do Next action.  
**End:** say *“update the end of session notes”* → overwrite continue + patch this file.  
**Protocol:** [`../docs/SESSION_PROTOCOL.md`](../docs/SESSION_PROTOCOL.md)



## Architecture

**OpenMontage render silo** — local GPU (RTX 3060) + Remotion + Python worker.

```
Remotion (remotion-renderer/)  →  visuals, posters, carousels
Python worker (main.py)        →  WhisperX auto-cut, FFmpeg NVENC
templates/                     →  investor update HTML masters + JSON schema
```

Outputs feed `04_comms` / `02_website/public/updates/` for investor emails.

---

## What's live

| Component | Status | Notes |
|-----------|--------|-------|
| **GPU / NVENC** | ✅ | `h264_nvenc` in `cutter.py`; RTX 3060 in WSL |
| **Fast scratch** | ✅ | `data/` → `/mnt/s/studio_scratch` |
| **Remotion** | ✅ | KenBurns, DataOverlay, SocialCarousel, poster engine |
| **Poster CLI** | ✅ | `just make-poster` — headless Remotion PNG |
| **Investor templates** | ✅ | `templates/` — used by `04_comms` pipeline |
| **Python worker** | 🟡 | `main.py` polls Firestore jobs — **depends on GCP** |

---

## Remaining work

1. **GCS download/upload** in `main.py` — currently placeholder local file
2. **WhisperX first-run** — model cache download on first `main.py` run
3. **Decouple Firestore queue** — if GCP stays retired, use local job files or file-drop trigger

---

## Handoffs (human)

| Item | Action |
|------|--------|
| `S:\` drive mounted | Required at `/mnt/s/studio_scratch` |
| Service account JSON | Path in `.env` → `GOOGLE_APPLICATION_CREDENTIALS` (only if using Firestore/GCS) |
| Local Ollama | `qwen3:14b` for auto-cutter director |

---

## Constraints

- **Never writes canonical SSOT** — consumes `01_evolution/` knowledge + `_assets/`
- **Heavy media not in git** — `_assets/studio/raw`, `_assets/studio/output`
- **Firestore job queue** — non-functional while GCP billing delinquent

---

## Verify (every task)

```bash
cd /home/evo/evo_01/03_studio
# Remotion preview:
cd remotion-renderer && npm run build
# Poster:
just make-poster --help
```

---

## Stale docs

- `MEMORY.md` — never customized (template placeholders)
- `BUILD_SUMMARY.md` — accurate for integrations; check this file for current priorities