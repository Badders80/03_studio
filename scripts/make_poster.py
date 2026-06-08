import os
import sys
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

# 1. Load environment variables
load_dotenv("/home/evo/.env")
load_dotenv("/home/evo/evo_01/03_studio/.env")

# Ensure Vertex AI mode is NOT forced for the developer API client
if "GOOGLE_GENAI_USE_VERTEXAI" in os.environ:
    del os.environ["GOOGLE_GENAI_USE_VERTEXAI"]
if "GOOGLE_CLOUD_PROJECT" in os.environ:
    del os.environ["GOOGLE_CLOUD_PROJECT"]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment or .env file.")
    sys.exit(1)

# 2. Define the Pydantic schema for Gemini parsing & multimodal image alignment
class PosterMetadata(BaseModel):
    # Layout Archetype Selection
    layout_type: Literal["quote", "next_up", "announcement", "race_details"] = Field(
        default="next_up",
        description="The layout archetype to use based on the user's request: 'quote' for quote cards/testimonials, 'next_up' for single or multi-race preview schedules, 'announcement' for list-of-updates/segment boards, or 'race_details' for rich telemetry/race results and metric updates."
    )
    
    # Generic fields (common across layouts)
    context_tag: str = Field(description="Scrubbed context tag/header, e.g., 'NEXT UP...' or 'STABLE UPDATE...'. Colons must be replaced with '...'. If none, default appropriately.")
    hero_title: str = Field(description="The horse name (e.g. 'Prudentia') or main highlighted entity, written in Title Case. If not mentioned, look for context clues or leave empty.")
    jockey_name: str = Field(description="Name of the jockey mentioned (e.g. 'Masa Hashizume' or 'Seina Imamura'), or empty if none.")
    horse_description: str = Field(description="Brief description of the horse or jockey silks mentioned, if any.")

    # Traditional Single-Event Fallback columns (Layout 2A capsule box)
    column_count: int = Field(default=2, description="Number of columns to render in the classic details box (1 or 2).")
    col1_primary: str = Field(default="", description="Primary detail for column 1 (e.g., 'MASA HASHIZUME' or '28 MAY'). Uppercase.")
    col1_sublabel: str = Field(default="", description="Sublabel for column 1 (e.g., 'CONFIRMED JOCKEY' or 'DATE'). Uppercase.")
    col2_primary: str = Field(default="", description="Primary detail for column 2 (e.g., 'TE RAPA' or 'RATING 75'). Empty if column_count is 1. Uppercase.")
    col2_sublabel: str = Field(default="", description="Sublabel for column 2 (e.g., 'THIS WEEKEND' or 'RESULT'). Empty if column_count is 1. Uppercase.")

    # Layout 1: Quote Card Fields
    quote_text: str = Field(default="", description="The text of the quote, desegregated into clean prose, without surrounding quotation marks.")
    quote_attribution: str = Field(default="", description="The author and title/stable of the quote, e.g., 'ANDREW SCOTT TRAINER, WEXFORD STABLES'. Uppercase.")

    # Layout 2B: Multi-Event Grid Fields (Schedule)
    event1_date: str = Field(default="", description="Date of the first event, e.g. '30 MAY'. Uppercase.")
    event1_location: str = Field(default="", description="Location of the first event, e.g. 'TE RAPA'. Uppercase.")
    event1_detail: str = Field(default="", description="Rating/distance of first event, e.g. 'RATING 75 | 1200 METERS'. Uppercase.")
    event2_date: str = Field(default="", description="Date of second event, e.g. '13 JUNE'. Uppercase.")
    event2_location: str = Field(default="", description="Location of second event, e.g. 'TE RAPA'. Uppercase.")
    event2_detail: str = Field(default="", description="Rating/distance of second event, e.g. 'RATING 75 | 1200 METERS'. Uppercase.")

    # Layout 3: Stable Announcements Segments
    announcement1_title: str = Field(default="", description="Title of the first update segment, e.g. horse name 'Hottathanafantasy'. Uppercase.")
    announcement1_desc: str = Field(default="", description="Uppercase description of the first segment, ending with attribution if any.")
    announcement2_title: str = Field(default="", description="Title of the second segment, e.g., 'I Stole a Manolo'. Uppercase.")
    announcement2_desc: str = Field(default="", description="Uppercase description of the second segment.")
    announcement3_title: str = Field(default="", description="Title of the third segment, e.g., 'Turn Me Loose x Yearn Filly'. Uppercase.")
    announcement3_desc: str = Field(default="", description="Uppercase description of the third segment.")

    # Layout 4: Race Details Metric Updates
    metric1_value: str = Field(default="", description="Primary metric value, typically placing result, e.g. '1ST PLACE' or '1ST'. Uppercase.")
    metric1_label: str = Field(default="RESULT", description="Label for metric 1, e.g. 'RESULT' or 'PLACING'. Uppercase.")
    metric2_value: str = Field(default="", description="Metric 2 value, e.g. jockey name 'MASA HASHIZUME'. Uppercase.")
    metric2_label: str = Field(default="JOCKEY", description="Label for metric 2, e.g. 'CONFIRMED JOCKEY'. Uppercase.")
    metric3_value: str = Field(default="", description="Metric 3 value, e.g., location 'TE RAPA'. Uppercase.")
    metric3_label: str = Field(default="TRACK", description="Label for metric 3, e.g. 'TRACK LOCATION' or 'TRACK'. Uppercase.")
    metric4_value: str = Field(default="", description="Metric 4 value, e.g. distance '1200 METERS'. Uppercase.")
    metric4_label: str = Field(default="DISTANCE", description="Label for metric 4, e.g. 'DISTANCE'. Uppercase.")
    metric5_value: str = Field(default="", description="Metric 5 value, e.g. time '1:10.24'. Uppercase.")
    metric5_label: str = Field(default="WINNING TIME", description="Label for metric 5, e.g. 'WINNING TIME' or 'TIME'. Uppercase.")
    metric6_value: str = Field(default="", description="Metric 6 value, e.g. margin '1.5 LENGTHS'. Uppercase.")
    metric6_label: str = Field(default="MARGIN", description="Label for metric 6, e.g. 'WINNING MARGIN' or 'MARGIN'. Uppercase.")

    # Multimodal image layout analysis parameters
    image_scale: float = Field(default=1.0, description="Ideal CSS scale factor (between 1.0 and 2.5) to zoom in on the horse's head or the racing action, making sure it feels cinematic and properly cropped.")
    image_focus_x: int = Field(default=50, description="Ideal X focal coordinate (0 to 100) to center the action. If the main subject is on the left, use a lower number. If centered, use 50. If on the right, use a higher number.")
    image_focus_y: int = Field(default=50, description="Ideal Y focal coordinate (0 to 100) to center the action. Ensure Y is between 30 and 60 so horse details are positioned in the top/middle viewport and not covered by bottom text containers.")

def parse_prompt_with_gemini(user_prompt: str, image_path: Path = None) -> PosterMetadata:
    print(f"Parsing prompt: '{user_prompt}' using Gemini...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    system_instruction = """
    You are the Evolution Stables Agent. Your task is to parse a natural language poster request into a structured JSON configuration aligning with one of our four (4) core premium layout archetypes.
    
    If an image is provided, you must ALSO perform a multimodal layout analysis of the image to determine the ideal centering and scaling parameters for the poster canvas (aspect ratio 4:5, 1080px width, 1350px height).
    
    Layout Selection & Parsing Logic:
    
    1. 'quote' Archetype (Layout 1: Testimonials / Quotes):
       - Trigger: If the prompt contains quotes, mentions what trainers/jockeys are saying, or explicitly mentions "quote", "testimonial", "quote card", e.g. "Andrew Scott trainer says...".
       - Fill: quote_text (the prose), quote_attribution (uppercase author + role, e.g. 'ANDREW SCOTT TRAINER, WEXFORD STABLES'), hero_title (horse name in title case).
       - Context Tag: Set to empty or 'NEWS'.
       
    2. 'next_up' Archetype (Layout 2: Pre-race Schedule & Preview):
       - Trigger: Standard default layout. Previews one or two upcoming races.
       - Fill: If single event, you can use col1_primary/col1_sublabel and col2_primary/col2_sublabel.
         If multi-event grid is needed (two upcoming dates), populate event1_date, event1_location, event1_detail and event2_date, event2_location, event2_detail.
       - Context Tag: Defaults to 'NEXT UP...'. Colon must be scrubbed out to '...'.
       - Hero Title: Horse name in title case.
       
    3. 'announcement' Archetype (Layout 3: Segment Board & Stable Updates):
       - Trigger: If the request lists news segments, announcements, shares available, update lists for multiple horses (e.g. "Other Stable News: Hottathanafantasy back in training... and I Stole a Manolo listing soon...").
       - Fill: announcement1_title, announcement1_desc, announcement2_title, etc. Keep description text concise and all-uppercase.
       - Context Tag: e.g. 'OTHER STABLE NEWS...' or 'STABLE UPDATES...'.
       
    4. 'race_details' Archetype (Layout 4: Technical Post-race/Pre-race Telemetry Metric Update):
       - Trigger: If the prompt describes a detailed race update with multiple metrics like placings, winning times, jockey name, track, distance, margin (e.g., "Make me a race details update for Prudentia: Result 1st place, Jockey Masa Hashizume, Track Te Rapa, Distance 1200 meters, Time 1:10.24, Margin 1.5 lengths").
       - Fill: metric1_value/metric1_label to metric6_value/metric6_label. Map results/placings to Metric 1, Jockey to Metric 2, Track to Metric 3, Distance to Metric 4, Winning Time to Metric 5, Margin to Metric 6. Ensure labels are uppercase like 'RESULT', 'JOCKEY', 'TRACK LOCATION', 'DISTANCE', 'WINNING TIME', 'MARGIN'.
       - Context Tag: e.g. 'RACE UPDATE...' or 'RESULTS STATUS...'.
       - Hero Title: Horse name in title case.

    Text Formatting Rules:
    - ALWAYS scrub colons from the context_tag: Replace ':' with '...'.
    - Convert horse names to title case for the hero_title (e.g., 'Prudentia').
    - NEVER include the corporate brand tagline block "GROUNDED IN TRADITION. EVOLVED THROUGH INNOVATION. OWNERSHIP TRANSFORMED." in any text block. It is completely excluded.

    Multimodal Image Alignment Rules (Only applicable if an image is provided):
    - Analyze the subject of the image (typically a horse, a jockey, or both).
    - Center the primary subject (usually the horse's head or the jockey's helmet) inside our poster.
    - Set image_scale: A float from 1.0 to 2.5 representing how much we should zoom.
      * Use 1.0 - 1.2 if the subject is already nicely framed and occupies most of the image.
      * Use 1.3 - 2.0 to zoom in on a smaller or distant subject (e.g., a horse running on a track).
    - Set image_focus_x: An integer from 0 to 100 representing the horizontal center of the subject.
    - Set image_focus_y: An integer from 0 to 100 representing the vertical center of the subject.
      * CRITICAL WARNING: The bottom 350px of our 1350px height (roughly the bottom 25-30% of the image) is covered by a black text overlay box and a gradient fade.
      * Therefore, the subject's head or the primary action MUST NOT sit in the bottom 30% of the canvas.
      * Adjust image_focus_y so that the subject's main features are positioned in the top or middle portion of the visible canvas (ideally around Y=30 to Y=60 in the final viewport).
    
    If no image is provided, default to:
    - image_scale = 1.0
    - image_focus_x = 50
    - image_focus_y = 50
    """
    
    contents = []
    if image_path and image_path.exists():
        try:
            from PIL import Image
            img = Image.open(image_path)
            contents.append(img)
            print(f"Loaded image '{image_path.name}' for multimodal layout analysis.")
        except Exception as e:
            print(f"Warning: Failed to load image for multimodal analysis: {e}")
            
    contents.append(f"Please parse this natural language request into the structured poster config: '{user_prompt}'")
    
    import time
    
    # Tiered Model Routing: Try gemini-2.5-flash, fall back to gemini-2.5-flash-lite
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
    
    for model_name in models_to_try:
        max_retries = 2
        backoff = 1
        for attempt in range(max_retries):
            try:
                print(f"Trying Gemini model: {model_name} (attempt {attempt + 1}/{max_retries})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        response_schema=PosterMetadata,
                        temperature=0.1
                    )
                )
                # Parse the JSON response
                data = json.loads(response.text)
                print(f"Successfully generated poster config using {model_name}!")
                return PosterMetadata(**data)
            except Exception as e:
                print(f"Gemini model {model_name} attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    print(f"Model {model_name} exhausted all attempts.")
                    
    print("All Gemini API models failed. Falling back to default layout.")
    # If all retries failed, return fallback metadata (outside the loop)
    return PosterMetadata(
        layout_type="next_up",
        context_tag="NEXT UP...",
        hero_title="Prudentia",
        column_count=2,
        col1_primary="MASA HASHIZUME",
        col1_sublabel="CONFIRMED JOCKEY",
        col2_primary="TE RAPA",
        col2_sublabel="THIS WEEKEND",
        jockey_name="Masa Hashizume",
        horse_description="",
        image_scale=1.0,
        image_focus_x=50,
        image_focus_y=50
    )

def resolve_image_path(image_arg: str, content_dump: Path) -> Path:
    print(f"Resolving image argument: '{image_arg}'...")
    
    # 1. Check if it's a direct absolute or relative path
    path = Path(image_arg)
    if path.exists() and path.is_file():
        print(f"Found image file directly: {path}")
        return path
        
    # 2. Check if it exists inside Content_Dump
    dump_path = content_dump / image_arg
    if dump_path.exists() and dump_path.is_file():
        print(f"Found image inside Content_Dump: {dump_path}")
        return dump_path
        
    # 3. Try fuzzy/substring match in Content_Dump
    png_files = list(content_dump.glob("*.png"))
    for file in png_files:
        if image_arg.lower() in file.name.lower():
            print(f"Matched image in Content_Dump: '{file.name}'")
            return file
            
    # 4. Try searching recursively in subdirectories of Content_Dump
    all_png_files = list(content_dump.rglob("*.png"))
    for file in all_png_files:
        if image_arg.lower() in file.name.lower():
            print(f"Matched image recursively in Content_Dump: '{file.name}'")
            return file
            
    raise FileNotFoundError(f"Could not resolve image path or filename for: '{image_arg}'")

def find_best_image(jockey_name: str, content_dump: Path) -> Path:
    print(f"Searching for best jockey/horse image matching '{jockey_name}' in {content_dump}...")
    
    jockey_lower = jockey_name.lower() if jockey_name else ""
    
    # Fuzzy match on standard jockey assets
    if "masa" in jockey_lower or "wexford" in jockey_lower or "hashizume" in jockey_lower:
        matched = content_dump / "image_2d0967.png"
        if matched.exists():
            print(f"Matched Wexford Jockey (Masa Hashizume) -> {matched.name}")
            return matched
            
    if "seina" in jockey_lower or "imamura" in jockey_lower:
        matched = content_dump / "image_2d02c3.png"
        if matched.exists():
            print(f"Matched Seina Imamura -> {matched.name}")
            return matched

    # Fallback to general Content_Dump images (e.g. 1.png, 2.png, 3.png etc.)
    # If the user has numbered images in Content_Dump, let's prefer horse action images (like 2.png or 3.png)
    for num_img in ["3.png", "2.png", "4.png", "1.png"]:
        path = content_dump / num_img
        if path.exists():
            print(f"Using Content_Dump asset -> {num_img}")
            return path

    # Fallback search - find any png file
    png_files = list(content_dump.glob("*.png"))
    if png_files:
        default_img = content_dump / "image_2d0967.png"
        if default_img.exists():
            print(f"Using default Wexford Jockey image -> {default_img.name}")
            return default_img
        print(f"Using fallback first image found -> {png_files[0].name}")
        return png_files[0]
        
    raise FileNotFoundError(f"No PNG jockey images found in Content_Dump directory: {content_dump}")

def main():
    parser = argparse.ArgumentParser(description="Headless Agentic Poster Generator")
    parser.add_argument("prompt", type=str, nargs="*", help="Natural language description of the poster")
    parser.add_argument("--context", type=str, help="Natural language description of the poster (alternative flag)")
    parser.add_argument("--image", type=str, help="Path or filename of the image to use, overriding auto-selection")
    args = parser.parse_args()
    
    user_prompt = " ".join(args.prompt) if args.prompt else args.context
    
    # Define directories
    base_dir = Path("/home/evo/evo_01/03_studio")
    content_dump_dir = base_dir / "Content_Dump"
    remotion_dir = base_dir / "remotion-renderer"
    output_dir = base_dir / "output"
    
    # If no prompt or context is provided, let's default to a generic "NEXT UP..." with the image name or a basic fallback
    if not user_prompt:
        if args.image:
            user_prompt = f"NEXT UP... featuring the image {args.image}"
            print(f"No prompt provided, but image was specified. Creating default context: '{user_prompt}'")
        else:
            print("Error: Please provide a natural language prompt or at least an image.")
            parser.print_help()
            sys.exit(1)
            
    # 1. Resolve image (either explicitly provided or via local text heuristic to save API quota)
    matched_image_path = None
    if args.image:
        try:
            matched_image_path = resolve_image_path(args.image, content_dump_dir)
        except Exception as e:
            print(f"Error resolving image: {e}")
            sys.exit(1)
    else:
        # Local quick text-heuristic matching to find image BEFORE making any API call.
        # This preserves daily/minute API quota by making exactly ONE multimodal API call.
        prompt_lower = user_prompt.lower()
        
        # 1. Fuzzy match horse name or keywords in the prompt to files in Content_Dump
        words_to_check = [w.strip(".,!?\"'()[]:;") for w in prompt_lower.split()]
        # Filter out common short words and template keywords
        ignored_words = {"this", "weekend", "race", "make", "poster", "with", "from", "ride", "been", "confirm", "confirmed", "to", "for", "me", "next", "up", "the", "and", "a", "is", "at", "in", "on", "of"}
        keywords = [w for w in words_to_check if len(w) > 3 and w not in ignored_words]
        
        found_by_keyword = None
        for kw in keywords:
            # Look for png files in Content_Dump containing the keyword (e.g. "prudentia" -> prudentia_action_shot.png)
            for file_path in content_dump_dir.glob("*.png"):
                if kw in file_path.name.lower() and file_path.name.lower() not in ["1.png", "2.png", "3.png"]:
                    found_by_keyword = file_path
                    break
            if found_by_keyword:
                break
                
        if found_by_keyword:
            matched_image_path = found_by_keyword
            print(f"Heuristically resolved image: '{matched_image_path.name}' by matching keyword '{kw}' from prompt.")
        elif "masa" in prompt_lower or "wexford" in prompt_lower or "hashizume" in prompt_lower:
            matched_image_path = content_dump_dir / "image_2d0967.png"
        elif "seina" in prompt_lower or "imamura" in prompt_lower:
            matched_image_path = content_dump_dir / "image_2d02c3.png"


    # Differentiate raw photography background assets from slide mockups
    is_slide_mockup = False
    if matched_image_path:
        name_lower = matched_image_path.name.lower()
        if name_lower in [f"{i}.png" for i in range(1, 11)] or "slide" in name_lower or "deck22may" in str(matched_image_path).lower():
            is_slide_mockup = True

    if is_slide_mockup:
        print(f"WARNING: Image '{matched_image_path.name}' is a pre-rendered slide mockup, NOT a raw horse photo.")
        # Fallback to a raw background image from Content_Dump to prevent double-rendering text!
        prompt_lower = user_prompt.lower()
        if "seina" in prompt_lower or "imamura" in prompt_lower:
            fallback_img = content_dump_dir / "image_2d02c3.png"
        else:
            fallback_img = content_dump_dir / "image_2d0967.png" # Wexford default
        
        if fallback_img.exists():
            print(f"Falling back to raw horse photography asset: '{fallback_img.name}'")
            matched_image_path = fallback_img
        else:
            print("No raw horse photography assets found in Content_Dump. Using absolute black background.")
            matched_image_path = None

    # 2. Parse natural language prompt using Gemini
    # If image is resolved (either explicitly or via local heuristic), we run exactly ONE multimodal call.
    if matched_image_path and matched_image_path.exists():
        metadata = parse_prompt_with_gemini(user_prompt, matched_image_path)
        print("\nParsed Poster Metadata (with alignment):")
        print(json.dumps(metadata.model_dump(), indent=2))
    else:
        # If no image is resolved yet, run a text-only call
        metadata = parse_prompt_with_gemini(user_prompt, None)
        print("\nParsed Poster Metadata (text-only):")
        print(json.dumps(metadata.model_dump(), indent=2))
        # Then search for image using the extracted jockey name
        try:
            matched_image_path = find_best_image(metadata.jockey_name, content_dump_dir)
            print(f"Heuristically resolved image: '{matched_image_path.name}' based on parsed jockey '{metadata.jockey_name}'")
        except Exception as e:
            print(f"Error locating image: {e}")
            sys.exit(1)
            
    # 4. Create public/ directory in remotion-renderer and copy image there
    public_dir = remotion_dir / "public"
    public_dir.mkdir(exist_ok=True)
    
    temp_image_name = "temp_jockey.png"
    target_image_path = public_dir / temp_image_name
    print(f"Copying {matched_image_path.name} to {target_image_path}...")
    shutil.copy2(matched_image_path, target_image_path)
    
    # 5. Prepare props JSON payload for Remotion (including scale and focal coordinates)
    props = {
        "layoutType": metadata.layout_type,
        "contextTag": metadata.context_tag,
        "heroTitle": metadata.hero_title if metadata.hero_title else "Prudentia",
        "columnCount": metadata.column_count,
        "col1Primary": metadata.col1_primary,
        "col1Sublabel": metadata.col1_sublabel,
        "col2Primary": metadata.col2_primary,
        "col2Sublabel": metadata.col2_sublabel,
        "imageSrc": f"/{temp_image_name}", # Loaded relative to Remotion public/ server root
        "imageScale": metadata.image_scale,
        "imageFocusX": metadata.image_focus_x,
        "imageFocusY": metadata.image_focus_y,
        
        # Quote card fields (Layout 1)
        "quoteText": metadata.quote_text,
        "quoteAttribution": metadata.quote_attribution,
        
        # Next Up events fields (Layout 2B grid)
        "event1Date": metadata.event1_date,
        "event1Location": metadata.event1_location,
        "event1Detail": metadata.event1_detail,
        "event2Date": metadata.event2_date,
        "event2Location": metadata.event2_location,
        "event2Detail": metadata.event2_detail,
        
        # Stable Announcements segments (Layout 3)
        "announcement1Title": metadata.announcement1_title,
        "announcement1Desc": metadata.announcement1_desc,
        "announcement2Title": metadata.announcement2_title,
        "announcement2Desc": metadata.announcement2_desc,
        "announcement3Title": metadata.announcement3_title,
        "announcement3Desc": metadata.announcement3_desc,
        
        # Race details metric updates (Layout 4)
        "metric1Value": metadata.metric1_value,
        "metric1Label": metadata.metric1_label,
        "metric2Value": metadata.metric2_value,
        "metric2Label": metadata.metric2_label,
        "metric3Value": metadata.metric3_value,
        "metric3Label": metadata.metric3_label,
        "metric4Value": metadata.metric4_value,
        "metric4Label": metadata.metric4_label,
        "metric5Value": metadata.metric5_value,
        "metric5Label": metadata.metric5_label,
        "metric6Value": metadata.metric6_value,
        "metric6Label": metadata.metric6_label,
    }
    props_str = json.dumps(props)
    
    # 6. Execute headless Remotion still engine
    temp_output_path = remotion_dir / "out" / "poster_temp.png"
    temp_output_path.parent.mkdir(exist_ok=True)
    
    # Remotion render command
    # Scale: 2 is used to compile at double resolution (2160x2700) for Retina / print density
    cmd = [
        "npx", "remotion", "still",
        "src/index.ts",
        "Poster",
        str(temp_output_path),
        f"--props={props_str}",
        "--scale=2",
        "--overwrite"
    ]
    
    print(f"\nExecuting Remotion render command:\n{' '.join(cmd)}")
    try:
        # Run command and capture output
        res = subprocess.run(cmd, cwd=str(remotion_dir), check=True, capture_output=True, text=True)
        print("Remotion render completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Remotion render: {e}")
        print(f"Stdout:\n{e.stdout}")
        print(f"Stderr:\n{e.stderr}")
        # Clean up temp image
        if target_image_path.exists():
            target_image_path.unlink()
        sys.exit(1)
        
    # 7. Copy final output to target directory and clean up
    output_dir.mkdir(exist_ok=True)
    final_output_path = output_dir / "poster.png"
    print(f"Copying rendered image to {final_output_path}...")
    shutil.copy2(temp_output_path, final_output_path)
    
    # Clean up temp files
    print("Cleaning up temporary render files...")
    if target_image_path.exists():
        target_image_path.unlink()
    if temp_output_path.exists():
        temp_output_path.unlink()
        
    print(f"\nSUCCESS: High-DPI Poster generated at {final_output_path}")

if __name__ == "__main__":
    main()
