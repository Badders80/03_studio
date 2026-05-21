import requests
import json

class Director:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="qwen3:14b"):
        self.url = ollama_url
        self.model = model

    def evaluate_cuts(self, segments):
        """
        Takes word segments with exact timestamps, and asks Ollama to identify silences
        and filler words, then outputs an Edit Decision List (EDL) and Remotion Trigger Events.
        """
        print(f"Calling Ollama ({self.model}) to act as Director Agent...")
        
        prompt = (
            "You are a video director for short-form consulting-grade horse videos. "
            "Analyze these transcript segments and suggest timestamps for cuts, keeping dramatic pauses "
            "but removing dead silence and filler words. Also, identify key moments to trigger Remotion "
            "visuals like Pedigree Slides, Data Overlays, or Ken Burns B-roll based on the narrative flow. "
            "Output the response as a JSON array of edit decisions."
        )
        
        payload = {
            "model": self.model,
            "prompt": f"{prompt}\nSegments: {json.dumps(segments)}",
            "stream": False
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            print("Director Agent analysis complete.")
            # Expecting the LLM to return structured JSON.
            # For this MVP, we return the raw response string.
            return data.get("response", "")
        except Exception as e:
            print(f"Error connecting to Director Agent (Ollama): {e}")
            return None
