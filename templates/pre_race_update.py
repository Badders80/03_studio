from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import os

def create_pre_race_video(horse_name, race_name, date, location, output_path):
    width, height = 1080, 1920
    duration = 8  # seconds

    # Create background
    bg = Image.new('RGB', (width, height), (20, 20, 30))
    draw = ImageDraw.Draw(bg)

    # Try to use a decent font (fallback to default if not found)
    try:
        font_title = ImageFont.truetype("arial.ttf", 90)
        font_normal = ImageFont.truetype("arial.ttf", 48)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()

    # Draw text
    draw.text((width//2, 400), horse_name, fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((width//2, 550), race_name, fill=(200, 200, 200), font=font_normal, anchor="mm")
    draw.text((width//2, 650), f"{date}", fill=(255, 200, 50), font=font_normal, anchor="mm")
    draw.text((width//2, 750), location, fill=(180, 180, 180), font=font_normal, anchor="mm")

    # Save background as image
    bg_path = "output/temp_bg.png"
    os.makedirs("output", exist_ok=True)
    bg.save(bg_path)

    # Create video with MoviePy
    clip = ImageClip(bg_path).with_duration(duration)

    # Simple animation - text moving up slightly
    def move_up(t):
        return ('center', 400 - t * 15)

    # Add animated text overlay
    txt_clip = TextClip(font="templates/arial.ttf", text=horse_name, font_size=90, color='white')
    txt_clip = txt_clip.with_position(move_up).with_duration(duration)

    final = CompositeVideoClip([clip, txt_clip])
    final.write_videofile(output_path, fps=30, codec="libx264")
