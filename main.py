from templates.pre_race_update import create_pre_race_video

if __name__ == "__main__":
    create_pre_race_video(
        horse_name="Lucky Strike",
        race_name="Maiden 1200m",
        date="15 March 2025",
        location="Te Rapa Racecourse",
        output_path="output/pre_race_lucky_strike.mp4"
    )
