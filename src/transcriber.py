import whisperx
import gc 
import torch

class Transcriber:
    def __init__(self, model_name="base", device="cuda", compute_type="float16"):
        self.device = device
        self.model_name = model_name
        self.compute_type = compute_type
        print(f"Loading WhisperX {model_name} model on {device}...")
        self.model = whisperx.load_model(model_name, device, compute_type=compute_type)
        
    def transcribe(self, audio_file):
        print(f"Transcribing {audio_file}...")
        audio = whisperx.load_audio(audio_file)
        result = self.model.transcribe(audio, batch_size=16)
        
        # Load alignment model
        print("Loading alignment model...")
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        print("Aligning output for exact timestamps...")
        result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
        
        return result["segments"]
