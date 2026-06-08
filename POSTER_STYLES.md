# Evolution Stables — Visual Poster Styles & Design Specification

This document is the definitive design specification for all Evolution Stables high-end social and investor posters.

---

## 🎨 1. Core Creative Philosophy

- **Understated Authority:** Quiet confidence over loud marketing hype.
- **The Sparing Gold & Logo Rule:** We do not over-use custom handwritten logos. Use them only when it suits the layout to add a bit of panache. Otherwise, render the horse's name in crisp, elegant editorial serif or sans-serif typography. Champagne Gold (`#D4A964`) is used ultra-sparingly to preserve its premium impact.
- **Contrasted Harmony:** Rigid, clean mathematical layouts balanced with an organic, human touch (the signature logos).

---

## 📸 2. Locked-In Photographic Styles

### Style 1: The Isolated Hero (Absolute Backdrop)
- **The Aesthetic:** A razor-sharp portrait of the horse/jockey isolated against an absolute black backdrop (`#000000` / `#0B0B0F`).
- **Lighting:** Strong, clean studio lighting defining muscle structure and coat texture.
- **Ideal Overlay:** Technical metrics, bento boxes, dense split-times, and post-race statistics.

### Style 2: The Moody Noir (High-Contrast & Tactile Grain)
- **The Aesthetic:** An active, highly dramatic photo styled like a classic analog darkroom film print. Deep shadows, rich desaturated tones, and heavy vignettes.
- **Lighting & Texture:** Intense side-lighting catching kicking dirt, sweat, or steam. Subtle, tactile fine-art paper grain/noise.
- **Ideal Overlay:** Trainer/Jockey Quote cards, emotional stable announcements, or major race-day previews.

### Style 3: The Soft-Focus Editorial (Warm Shallow Depth)
- **The Aesthetic:** An intimate close-up (helmet, ears, reins, or trackwork detail) with an extremely shallow depth of field (creamy background bokeh).
- **Lighting:** Warm, golden-hour natural sunlight filtering in, bringing out natural champagne, rich bay, and gold undertones.
- **Ideal Overlay:** "Stable Insights," behind-the-scenes updates, and weekly reports.

### Style 4: The High-Speed Telemetry (Overcast Motion Blur)
- **The Aesthetic:** A high-action panning shot of the horse running at full pace. Subject is in sharp focus; background is a desaturated, horizontal motion blur.
- **Lighting:** Cool, neutral, overcast lighting emphasizing silhouettes and muscle definition.
- **Ideal Overlay:** Speed metrics, sectional splits, and multi-race schedules.

---

## 📐 3. Context-Aware Composition & Layout Rules

### A. Dynamic Layout Placement (The Negative Space Rule)
To prevent a cheap "generic template" look, **overlays must be dynamically bound to the visual composition and negative space of the background image.** We never blindly force text into a static position if it covers the main visual subject (the horse or jockey).
- **Left-Empty Composition:** If the horse/jockey is positioned on the right, the text, quote, or telemetry overlays must align on the **left**.
- **Right-Empty Composition:** If the horse/jockey is positioned on the left, the overlays must align on the **right**.
- **Top-Empty Composition:** If the main subject is positioned in the lower viewport, the overlays must sit cleanly at the **top**.
- **Bottom-Empty Composition:** If the main subject is positioned in the upper viewport, the overlays must sit cleanly at the **bottom**.

### B. The Hero Identity & Separators
- **Horse Name:** Can be represented by a custom SVG signature logo (e.g. `Prudentia_Logo` or `Hottathen_Logo`) for panache, or set in clean editorial serif/sans-serif.
- **Context Tag:** Spaced, uppercase monospaced text at the top-left (e.g., `N E X T   U P   |   E V O L U T I O N`) in slate-grey (`#8E8E93`).
- **Inline Separator Rule:** **Never** use bullet points (`•`) or dots between inline text words or metrics. **Always use the pipe character `|`** as the clean, technical separator (e.g. `TE RAPA | DATE` or `MASA HASHIZUME | CONFIRMED JOCKEY`).

### C. The Translucent Telemetry Bar
- **Material:** A horizontal/vertical box with a dark translucent fill (matte charcoal at 40% opacity) and a heavy backdrop-blur filter.
- **Dividers:** 1px vertical hairline dividers in low-opacity grey (`#8E8E93` at 20% opacity) separating data columns.
- **Data Layout:** Bold, technical sans-serif numbers (e.g., `1ST` or `1:10.24`) with tiny, uppercase technical labels (`RESULT` or `TIME`) aligned underneath in slate-grey.

### D. The Minimalist Quote Block
- **Layout:** Left-aligned text block utilizing beautiful high-contrast italic serif.
- **Minimalism Rule:** **Never** use surrounding quotation marks. Quotation marks are replaced by a single, ultra-thin vertical accent line on the left margin, letting negative space carry the quote.
- **Signature:** A small, clean, uppercase attribution at the bottom (e.g., `— LANCE O'SULLIVAN | TRAINER | WEXFORD STABLES`).

### E. Segmented Glass Cards
- **Structure:** Floating vertical cards with rounded corners, a deep backdrop blur, and a thin, low-opacity white border.
- **Dividers:** Clean horizontal hairline dividers separating individual segments.
- **Highlights:** White titles for each horse, followed by a muted sentence-case description below. Key action phrases (e.g., **BACK IN TRAINING** or **SHARES LISTED**) are highlighted in a slightly heavier font weight in soft white or Champagne Gold.

---

## 🛠️ 4. Integration with `/ui-ux-pro-max`

This design specification inherits core intelligence from our `/ui-ux-pro-max` design system skill:
- **Hierarchy & Proportions:** Strict margin ratios (minimum 48px/5% padding container safety margins) so text never touches the edge.
- **Stable Hover & Interactivity:** Clean color/opacity transitions on any active items.
- **No Emojis:** Rely strictly on professional SVG icons (like Lucide or custom logos).
- **High Contrast Contrast:** Standard contrast ratio compliance (minimum 4.5:1) ensuring all text remains extremely crisp and readable regardless of image brightness behind it.
