import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class VoiceEngine:
    """
    A unified wrapper for generating Voiceovers.
    Currently uses Edge-TTS (free, human-sounding Microsoft neural voices)
    Can easily be swapped to Piper (local offline) or ElevenLabs in the future.
    """
    def __init__(self, output_dir="/mnt/s/studio_scratch/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Default voice - friendly and professional male voice
        self.default_voice = "en-US-ChristopherNeural"

    def generate_audio(self, text: str, filename: str, voice: str = None) -> str:
        """
        Generates audio using edge-tts.
        Ensure edge-tts is installed: pip install edge-tts
        """
        if not voice:
            voice = self.default_voice
            
        output_path = self.output_dir / filename
        print(f"Generating voiceover for text: '{text[:30]}...' using voice {voice}")
        
        # We use edge-tts CLI directly via subprocess
        command = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", str(output_path)
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Voiceover saved to {output_path}")
            return str(output_path)
        except FileNotFoundError:
            print("Error: edge-tts is not installed. Run: pip install edge-tts")
            return ""
        except subprocess.CalledProcessError as e:
            print(f"Error generating voice: {e.stderr.decode()}")
            return ""

if __name__ == "__main__":
    engine = VoiceEngine()
    # engine.generate_audio("Welcome to the Hybrid Studio toolkit.", "test_voice.mp3")
