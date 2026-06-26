import os
import time
from pathlib import Path
from dotenv import load_dotenv

# pip install google-genai
from google import genai
from google.genai import types

load_dotenv()

class VeoGenerator:
    """
    Generates high-quality AI videos using Google's Veo 3.1 model via AI Studio (free tier).
    Requires AI_STUDIO_API_KEY to be set in .env. Vertex AI is retired (2026-06-18).
    """
    def __init__(self, output_dir="/home/evo/studio_scratch/assets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "evolution-engine")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        try:
            # Initialize AI Studio client (NOT Vertex AI — retired 2026-06-18)
            self.client = genai.Client(vertexai=False, api_key=os.getenv("AI_STUDIO_API_KEY", ""))
            print(f"Initialized Veo Generator (AI Studio, free tier)")
        except Exception as e:
            print(f"Error initializing Google GenAI Client: {e}")
            self.client = None

    def generate_video(self, prompt: str, filename_prefix: str = "veo_gen") -> str:
        if not self.client:
            print("Client not initialized. Check your gcloud auth credentials.")
            return ""

        print(f"\n[Veo] Requesting video generation for prompt:\n'{prompt}'\nThis may take a few minutes...")
        
        try:
            # Start the Long Running Operation for Veo 3.1
            operation = self.client.models.generate_videos(
                model="veo-2.0-generate-001",
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    aspect_ratio="16:9",
                    person_generation="ALLOW_ADULT"
                ),
            )
            
            print("[Veo] Operation started. Waiting for completion...")
            while not operation.done:
                print("[Veo] Generating... this can take 3-5 minutes.")
                time.sleep(15)
                operation = self.client.operations.get(operation=operation)
                
            result = operation
            
            if not result.response or not result.response.generated_videos:
                print("[Veo] Error: No videos were generated.")
                return ""
                
            video_data = result.response.generated_videos[0]
            
            # Save the video bytes to a file
            timestamp = int(time.time())
            filename = f"{filename_prefix}_{timestamp}.mp4"
            output_path = self.output_dir / filename
            
            if hasattr(video_data, 'video') and hasattr(video_data.video, 'video_bytes'):
                with open(output_path, "wb") as f:
                    f.write(video_data.video.video_bytes)
                print(f"[Veo] Successfully generated and saved to {output_path}")
                return str(output_path)
            elif hasattr(video_data, 'uri'):
                print(f"[Veo] Video generated at GCS URI: {video_data.uri}")
                print("You may need to download it manually using gsutil.")
                return video_data.uri
            else:
                print("[Veo] Unknown video response format. Please check the result object.")
                print(result)
                return ""
                
        except Exception as e:
            print(f"[Veo] Error during generation: {e}")
            return ""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Veo 3.1 videos")
    parser.add_argument("--prompt", type=str, required=True, help="The video generation prompt")
    parser.add_argument("--prefix", type=str, default="veo_gen", help="Prefix for the output filename")
    args = parser.parse_args()
    
    generator = VeoGenerator()
    generator.generate_video(args.prompt, args.prefix)
