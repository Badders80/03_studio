# Evolution Stables — Developer & Antigravity Template System

This folder contains the official, locked-in master templates for Evolution Stables Investor Updates, along with a lightweight Python compiler. 

By utilizing **Antigravity (your AI partner)** alongside these templates, you bypass brittle UI builders that break whenever you want a custom layout shift. You can manage, tweak, and deploy beautiful updates directly via raw text prompts or structured JSON files.

---

## 📂 System Architecture

*   **[`landing_page_master.html`](file:///home/evo/evo_01/03_studio/templates/landing_page_master.html)** — Premium dark-themed editorial layout. Self-contained, responsive, utilizes Google Fonts (Playfair Display + Inter), and includes the signature golden branding colors (#d4a964) and micro-animations.
*   **[`investor_update_email_master.html`](file:///home/evo/evo_01/03_studio/templates/investor_update_email_master.html)** — **Gold standard** full-content race-preview email (600px table layout). Locked from Prudentia 27 Jun 2026. See `race_preview_update.schema.json` + `04_comms/.agents/skills/investor-update-pipeline/`.
*   **[`email_teaser_master.html`](file:///home/evo/evo_01/03_studio/templates/email_teaser_master.html)** — Lightweight teaser linking to hosted update (optional; full email preferred for investors).
*   **[`generate_update.py`](file:///home/evo/evo_01/03_studio/templates/generate_update.py)** — Zero-dependency Python 3 utility that parses a structured JSON input file and instantly generates both landing page and email HTML files directly inside the website's public updates folder (`02_website/public/updates/`).
*   **[`example_update.json`](file:///home/evo/evo_01/03_studio/templates/example_update.json)** — An example data structure representing our highly successful May 28 update for *Prudentia*.

---

## ⚡ Direct Generation (Via Antigravity)

Because Antigravity can read, edit, and write files directly inside your workspace, you don't even need to touch the command line. When you have a new update, simply send a message like:

> **"Hey Antigravity, let's make a new update for [Horse Name] on [Date]. Here are the draft details: [Paste Draft / Email / Transcript]. Please use the master templates to generate and deploy it."**

Antigravity will:
1. Parse your draft details.
2. Structure them into the correct parameter schema.
3. Automatically execute `generate_update.py` behind the scenes.
4. Verify the builds, check the rendering paths, and hand you the staging URL.

---

## 🛠 Manual CLI Compilation

If you prefer to compile updates locally on your machine via the terminal, use the provided Python script:

```bash
# From the 03_studio/templates directory:
python3 generate_update.py example_update.json
```

### Options:
*   `--dry-run`: Runs compilation in memory, printing output characteristics without writing files.
*   `--output-dir`: Manually redirect where compiled updates are saved.

---

## 📝 Structured JSON Schema Reference

Every update is driven by a single flat JSON configuration. Below is a summary of the keys used:

| Key | Description | Type / Example |
| :--- | :--- | :--- |
| `slug` | File safety prefix used for saving the files (e.g. `Prudentia_Update_28May2026`). | `string` |
| `preheader` | Hidden text shown in email clients before opening the message. | `string` |
| `title` | Title with optional custom inline styled italic text. | `string` |
| `hero_media` | Embed iframe or custom raw HTML element for the website landing page. | `string` |
| `hero_image_email` | Fully qualified absolute link to the image rendered in email clients. | `string` |
| `hero_caption` | Full-caps small caption text placed below the hero image/video. | `string` |
| `standfirst` | Intro paragraph styled with premium Playfair Display font. | `string` |
| `body_1` / `body_2` / `body_3` | Standard body copy paragraphs (renders as high-readability Inter font). | `string` |
| `quote` | Object with nested `text`, `author`, and `affiliation` keys for editorial pull-quotes. | `object` |
| `revisit_links` | List of items containing `text` and `url` to render play-button list links. | `array of objects` |
| `tactical_analysis` | Includes `subtitle` and an array of 4 card objects (each with `id`, `title`, `badge`, `text`). | `object` |
| `cta` | Object containing nested `description`, custom button `text`, and target `link`. | `object` |
| `sender` | Object containing nested `name`, `title`, and local `signature_image` path. | `object` |
