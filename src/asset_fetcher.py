import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class AssetFetcher:
    def __init__(self, output_dir="/mnt/s/studio_scratch/assets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # We will use Pexels API for free stock footage/images
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")

    def fetch_broll(self, query: str, limit: int = 3, video: bool = True):
        """Fetches B-roll video or images matching the query."""
        if not self.pexels_api_key:
            print("Warning: PEXELS_API_KEY not set. Cannot fetch B-roll.")
            return []

        print(f"Fetching {'video' if video else 'image'} B-roll for: {query}")
        
        headers = {"Authorization": self.pexels_api_key}
        endpoint = "videos/search" if video else "v1/search"
        url = f"https://api.pexels.com/{endpoint}?query={query}&per_page={limit}&orientation=landscape"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching from Pexels: {response.status_code}")
            return []

        data = response.json()
        items = data.get("videos" if video else "photos", [])
        
        downloaded_files = []
        for i, item in enumerate(items):
            # Get the best download link
            if video:
                # Find highest quality mp4
                files = [f for f in item.get("video_files", []) if f["file_type"] == "video/mp4"]
                if not files: continue
                files.sort(key=lambda x: x.get("width", 0), reverse=True)
                download_url = files[0]["link"]
                ext = ".mp4"
            else:
                download_url = item["src"]["original"]
                ext = ".jpg"

            safe_query = query.replace(" ", "_").lower()
            filename = self.output_dir / f"broll_{safe_query}_{i}{ext}"
            
            print(f"Downloading {filename}...")
            r = requests.get(download_url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
            
            downloaded_files.append(str(filename))
            
        return downloaded_files

if __name__ == "__main__":
    fetcher = AssetFetcher()
    # fetcher.fetch_broll("server rack", limit=1)
