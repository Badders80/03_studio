#!/usr/bin/env python3
import os
import json
import argparse
import sys

def build_quote_block(quote_data):
    if not quote_data or not quote_data.get("text"):
        return ""
    
    text = quote_data.get("text", "")
    author = quote_data.get("author", "")
    affiliation = quote_data.get("affiliation", "")
    
    affiliation_html = ""
    if affiliation:
        affiliation_html = f', <span style="color:#000;">{affiliation}</span>'
        
    return f"""
    <div class="quote-block" style="width: 100%; margin: 36px 0; display: flex; align-items: stretch;">
        <div style="width: 1.5px; min-width: 1.5px; background-color: #d4a964;"></div>
        <div style="background-color: #fafafa; padding: 30px 32px; flex-grow: 1;">
            <div style="width: 100%; margin-bottom: 18px;">
                <blockquote style="font-family: 'Times New Roman', Times, serif; font-size: 28px; font-style: italic; line-height: 1.5; color: #1a1a1a; margin: 0; text-align: left; letter-spacing: -0.01em;">
                    {text}
                </blockquote>
            </div>
            <div style="text-align: left; padding-top: 12px;">
                <cite style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; color: #888888; text-transform: uppercase; letter-spacing: 2px; display: block;">
                    {author}{affiliation_html}
                </cite>
            </div>
        </div>
    </div>
    """

def build_revisit_block(links):
    if not links:
        return ""
    
    links_html = []
    for link in links:
        text = link.get("text", "")
        url = link.get("url", "")
        links_html.append(f"""
                <a href="{url}" target="_blank" style="font-family:'Inter',sans-serif; font-size:14px; color:#000000; text-decoration:none; font-weight:600; display: inline-block;">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="#d4a964" style="margin-right: 8px; vertical-align: middle; margin-top: -2px;"><path d="M8 5v14l11-7z"/></svg>
                    <span style="border-bottom: 1px solid #d4a964; padding-bottom: 1px;">{text}</span>
                </a>""")
    
    links_joined = "\n".join(links_html)
    
    return f"""
    <div class="quote-block" style="width: 100%; margin: 36px 0; display: flex; align-items: stretch;">
        <div style="width: 1.5px; min-width: 1.5px; background-color: #d4a964;"></div>
        <div style="background-color: #fafafa; padding: 30px 32px; flex-grow: 1;">
            <p style="font-family:'Inter',sans-serif; font-size:10px; font-weight:700; letter-spacing:2px; color:#888888; text-transform:uppercase; margin: 0 0 18px 0;">Revisit Her Recent Outings</p>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                {links_joined}
            </div>
        </div>
    </div>
    """

def build_tactical_analysis(tactical_data):
    if not tactical_data or not tactical_data.get("cards"):
        return ""
    
    subtitle = tactical_data.get("subtitle", "for this Saturday.")
    cards = tactical_data.get("cards", [])
    
    cards_html = []
    for i, card in enumerate(cards):
        card_id = card.get("id", f"{i+1:02d}")
        title = card.get("title", "")
        badge = card.get("badge", "")
        text = card.get("text", "")
        
        # Border classes/inline styling logic to match a clean responsive 2x2 grid
        border_right = " border-right: 1px solid #222222;" if i in [0, 2] else ""
        border_bottom = " border-bottom: 1px solid #222222;" if i in [0, 1] else ""
        
        badge_html = ""
        if badge:
            badge_html = f'<span style="border:1px solid #333;color:#888;font-family:\'Inter\',sans-serif;font-size:10px;font-weight:600;padding:4px 12px;border-radius:20px;letter-spacing:1px;text-transform:uppercase;">{badge}</span>'
            
        cards_html.append(f"""        <div class="grid-cell" style="flex: 1 1 50%; padding: 28px;{border_right}{border_bottom} box-sizing: border-box;">
            <div style="font-family:'Inter',sans-serif;font-size:11px;font-weight:700;color:#444;margin-bottom:9px;">{card_id}</div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
                <h4 style="font-family:'Inter',sans-serif;font-size:18px;font-weight:600;color:#ffffff;margin:0;">{title}</h4>
                {badge_html}
            </div>
            <p style="font-family:'Inter',sans-serif;font-size:14px;line-height:1.6;color:#888;margin:0;">{text}</p>
        </div>""")
        
    cards_joined = "\n".join(cards_html)
    
    return f"""
  <div class="container-padding" style="width:100%;background-color:#050505;padding:48px 48px;margin-bottom:0;">
    <div style="width:100%;margin-bottom:32px;padding-left:32px;">
      <p style="font-family:'Inter',sans-serif;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#555;margin-bottom:10px;">Why This Sets Up Well</p>
      <h2 style="font-family:'Playfair Display', serif;font-size:36px;font-weight:400;line-height:1.1;color:#ffffff;letter-spacing:-0.5px;">Tactical Analysis</h2>
      <p style="font-family:'Playfair Display', serif;font-size:36px;font-weight:400;line-height:1.1;color:#666666;letter-spacing:-0.5px;">{subtitle}</p>
    </div>

    <div style="width:100%;background:#0a0a0a;border-radius:12px;border:1px solid #222222;overflow:hidden;display:flex;flex-wrap:wrap;">
{cards_joined}
    </div>
  </div>
    """

def build_hero_image_email(img_url, caption):
    if not img_url:
        return ""
    
    caption_html = ""
    if caption:
        caption_html = f"""
              <div style="padding: 15px 0; text-align: center;">
                <p style="margin: 0; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 10px; font-weight: 700; color: #747474; text-transform: uppercase; letter-spacing: 1.5px;">
                  {caption}
                </p>
              </div>"""
              
    return f"""
          <tr>
            <td style="padding: 0 40px;">
              <div style="border-radius: 8px; overflow: hidden;">
                <img src="{img_url}" alt="Hero Image" width="520" style="width: 100%; max-width: 520px; display: block; border-radius: 8px;">
              </div>
              {caption_html}
            </td>
          </tr>"""

def log_compiled_update_to_ledger(data, slug):
    db_path = "/home/evo/workspace/projects/Evolution_Content/data/ledger.sqlite"
    if not os.path.exists(os.path.dirname(db_path)):
        return
    
    import sqlite3
    from datetime import datetime
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Ensure emails table exists
        c.execute("""
          CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_address TEXT NOT NULL,
            subject TEXT NOT NULL,
            date_received DATETIME,
            body_text TEXT,
            body_html TEXT,
            extracted_json TEXT,
            source_type TEXT DEFAULT 'email',
            status TEXT DEFAULT 'unread',
            file_path TEXT,
            message_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        """)
        
        message_id = f"compiled-{slug}"
        # Deduplication check
        row = c.execute("SELECT id FROM emails WHERE message_id = ?", (message_id,)).fetchone()
        if row:
            conn.close()
            return
            
        from_addr = data.get("sender", {}).get("name", "Alex Baddeley") + " <alex@evolutionstables.nz>"
        subject = data.get("title", f"Investor Update: {slug}").replace('<span style="color: #d4a964; font-style: italic; font-weight: 400;">', '').replace('</span>', '').replace('<span style="color:#d4a964; font-style:italic; font-weight:400;">', '').replace('<span style="color: #d4a964; font-style: italic; font-weight: 400;\">', '')
        
        body_text = f"{data.get('standfirst', '')}\n\n{data.get('body_1', '')}\n\n{data.get('body_2', '')}\n\n{data.get('body_3', '')}"
        
        extracted_payload = {
            "horse": data.get("slug", "").split("_")[0].capitalize(),
            "stable": "Evolution Stables",
            "trainer": "Lance O'Sullivan & Andrew Scott",
            "venue": "",
            "race_date": datetime.now().strftime("%Y-%m-%d"),
            "video_urls": [data.get("hero_media")] if "mp4" in data.get("hero_media", "") else [],
            "transcript": body_text,
            "quotes": [
                {"speaker": data.get("quote", {}).get("author", "Andrew Scott"), "text": data.get("quote", {}).get("text", "")}
            ] if data.get("quote") else [],
            "sentiment": "positive",
            "content_type": "investor_update"
        }
        
        c.execute("""
            INSERT INTO emails (from_address, subject, date_received, body_text, body_html, extracted_json, status, message_id, source_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            from_addr,
            subject,
            datetime.now().isoformat(),
            body_text,
            f"See compiled update at /updates/{slug}.html",
            json.dumps(extracted_payload),
            "sent",
            message_id,
            "investor_update"
        ))
        
        conn.commit()
        last_id = c.lastrowid
        print(f"[Ledger] Successfully logged outgoing update to SQLite database (ID: {last_id})")
        
        # Also append to ndjson catalog
        catalog_path = os.path.join(os.path.dirname(db_path), "..", "catalog", "content-index.ndjson")
        if os.path.exists(os.path.dirname(catalog_path)):
            catalog_entry = {
                "event": "update_compiled",
                "timestamp": datetime.now().isoformat(),
                "email": {
                    "id": last_id,
                    "from": from_addr,
                    "subject": subject,
                    "date": datetime.now().isoformat(),
                    "extracted": extracted_payload,
                    "status": "sent",
                    "ingested_by": "studio_compiler"
                }
            }
            with open(catalog_path, "a") as cat_f:
                cat_f.write(json.dumps(catalog_entry) + "\n")
            print("[Ledger] Successfully appended compile event to catalog/content-index.ndjson")
            
        conn.close()
    except Exception as e:
        print(f"[Ledger] Warning: Could not log to ledger database: {e}")

def generate(json_path, output_dir=None, dry_run=False):
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    slug = data.get("slug")
    if not slug:
        print("Error: JSON must specify a 'slug' field for the update filenames.")
        sys.exit(1)
        
    # Paths setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = script_dir
    
    if not output_dir:
        # Default to 02_website public updates
        output_dir = os.path.abspath(os.path.join(script_dir, "../../02_website/public/updates"))
        
    print(f"Loaded update data for: {slug}")
    print(f"Output directory: {output_dir}")
    
    # 1. Read Templates
    landing_master_path = os.path.join(templates_dir, "landing_page_master.html")
    email_master_path = os.path.join(templates_dir, "email_teaser_master.html")
    
    if not os.path.exists(landing_master_path) or not os.path.exists(email_master_path):
        print("Error: Master templates not found in the same folder.")
        sys.exit(1)
        
    with open(landing_master_path, 'r') as f:
        landing_tmpl = f.read()
        
    with open(email_master_path, 'r') as f:
        email_tmpl = f.read()
        
    # 2. Build Sub-components
    quote_block_html = build_quote_block(data.get("quote"))
    revisit_block_html = build_revisit_block(data.get("revisit_links"))
    tactical_section_html = build_tactical_analysis(data.get("tactical_analysis"))
    
    # Email Hero Block
    hero_img_email = data.get("hero_image_email", "")
    if hero_img_email and not hero_img_email.startswith("http") and not hero_img_email.startswith("/"):
        print(f"Warning: hero_image_email '{hero_img_email}' looks like a relative filename. Translating into staging path.")
        hero_img_email = f"https://02website-pearl.vercel.app/updates/{hero_img_email}"
    elif hero_img_email and hero_img_email.startswith("/updates/"):
        hero_img_email = f"https://02website-pearl.vercel.app{hero_img_email}"
        
    hero_image_block_email = build_hero_image_email(hero_img_email, data.get("hero_caption", ""))
    
    # 3. Parameter Mapping - Landing Page
    landing_output = landing_tmpl
    replacements_landing = {
        "{{PREHEADER}}": data.get("preheader", ""),
        "{{TITLE}}": data.get("title", ""),
        "{{HERO_MEDIA}}": data.get("hero_media", ""),
        "{{HERO_CAPTION}}": data.get("hero_caption", ""),
        "{{STANDFIRST}}": data.get("standfirst", ""),
        "{{BODY_1}}": data.get("body_1", ""),
        "{{BODY_2}}": data.get("body_2", ""),
        "{{BODY_3}}": data.get("body_3", ""),
        "{{QUOTE_BLOCK}}": quote_block_html,
        "{{REVISIT_BLOCK}}": revisit_block_html,
        "{{TACTICAL_ANALYSIS_SECTION}}": tactical_section_html,
        "{{CTA_DESCRIPTION}}": data.get("cta", {}).get("description", ""),
        "{{CTA_LINK}}": data.get("cta", {}).get("link", ""),
        "{{CTA_TEXT}}": data.get("cta", {}).get("text", "View"),
        "{{SIGNATURE_IMAGE}}": data.get("sender", {}).get("signature_image", "/updates/AB_Signiture.png"),
        "{{SENDER_NAME}}": data.get("sender", {}).get("name", "Alex Baddeley"),
        "{{SENDER_TITLE}}": data.get("sender", {}).get("title", "Evolution Stables")
    }
    
    for key, val in replacements_landing.items():
        landing_output = landing_output.replace(key, val)
        
    # 4. Parameter Mapping - Email Teaser
    # For email, any relative signature paths must be absolute
    sig_img_email = data.get("sender", {}).get("signature_image", "/updates/AB_Signiture.png")
    if sig_img_email.startswith("/updates/"):
        sig_img_email = f"https://evolutionstables.nz{sig_img_email}"
    elif not sig_img_email.startswith("http"):
        sig_img_email = f"https://evolutionstables.nz/updates/{sig_img_email}"
        
    email_output = email_tmpl
    replacements_email = {
        "{{PREHEADER}}": data.get("preheader", ""),
        "{{TITLE}}": data.get("title", ""),
        "{{BODY_1}}": data.get("body_1", ""),
        "{{BODY_2}}": data.get("body_2", ""),
        "{{HERO_IMAGE_BLOCK}}": hero_image_block_email,
        "{{TEASER_DESCRIPTION}}": f"I've put together a full tactical analysis, including stable reports and recent track work footage, on the Evolution site." if not data.get("email_teaser_body") else data.get("email_teaser_body"),
        "{{CTA_LINK}}": f"https://02website-pearl.vercel.app/updates/{slug}.html",
        "{{CTA_TEXT}}": data.get("email_cta_text", "Read the Full Briefing & Tactical Analysis &rarr;"),
        "{{SIGNATURE_IMAGE}}": sig_img_email,
        "{{SENDER_NAME}}": data.get("sender", {}).get("name", "Alex Baddeley"),
        "{{SENDER_TITLE}}": data.get("sender", {}).get("title", "Evolution Stables")
    }
    
    for key, val in replacements_email.items():
        email_output = email_output.replace(key, val)
        
    # Write to files
    landing_file_name = f"{slug}.html"
    email_file_name = f"{slug}_email.html"
    
    landing_output_path = os.path.join(output_dir, landing_file_name)
    email_output_path = os.path.join(output_dir, email_file_name)
    
    if not dry_run:
        os.makedirs(output_dir, exist_ok=True)
        with open(landing_output_path, 'w') as f:
            f.write(landing_output)
        with open(email_output_path, 'w') as f:
            f.write(email_output)
            
        print(f"\n[Success] Created landing page: {landing_output_path}")
        print(f"[Success] Created email teaser: {email_output_path}")
        
        # Log to ledger
        log_compiled_update_to_ledger(data, slug)
        
        print(f"\nURLs (once pushed/deployed):")
        print(f"- Landing Page: https://02website-pearl.vercel.app/updates/{landing_file_name}")
        print(f"- Email Teaser: https://02website-pearl.vercel.app/updates/{email_file_name}")
    else:
        print("\n--- DRY RUN ONLY ---")
        print(f"Would write landing page to: {landing_output_path} ({len(landing_output)} chars)")
        print(f"Would write email teaser to: {email_output_path} ({len(email_output)} chars)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile Evolution Stables Investor Update templates from JSON config.")
    parser.add_argument("json_file", help="Path to the JSON update data file")
    parser.add_argument("--output-dir", help="Custom output directory for the compiled HTMLs")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    
    args = parser.parse_args()
    generate(args.json_file, args.output_dir, args.dry_run)
