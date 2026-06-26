import os
import subprocess
import time
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Import our new pipeline components
from src.transcriber import Transcriber
from src.director import Director
from src.cutter import Cutter

def check_gpu():
    print("Verifying GPU pass-through with nvidia-smi...")
    try:
        subprocess.run(['nvidia-smi'], capture_output=True, text=True, check=True)
        print("GPU is accessible!")
    except Exception as e:
        print(f"ERROR: GPU check failed. Ensure NVIDIA drivers and CUDA are installed: {e}")
        exit(1)

def run_pipeline(job_id, job_data):
    """
    Executes the OpenMontage Auto-Cutter Pipeline.
    """
    print(f"\n--- Starting Pipeline for Job: {job_id} ---")
    
    # 1. Download raw asset (simulated)
    # raw_video_path = download_from_gcs(job_data['raw_video_url'])
    raw_video_path = "/home/evo/studio_scratch/raw_input.mp4" # Placeholder
    
    # Initialize components
    transcriber = Transcriber(model_name="base", device="cuda")
    director = Director(model="qwen3:14b")
    cutter = Cutter(scratch_dir="/home/evo/studio_scratch")
    
    # 2. Transcription (WhisperX)
    print("Step 1: Running WhisperX transcription & alignment...")
    segments = transcriber.transcribe(raw_video_path)
    
    # 3. Director Agent (Ollama)
    print("Step 2: Director Agent analyzing narrative flow...")
    edl_and_remotion_triggers = director.evaluate_cuts(segments)
    
    # Parse simulated EDL (In real use, we parse JSON from LLM)
    # For now, we simulate an EDL payload
    simulated_edl = [{'start': 0.0, 'end': 5.0}, {'start': 6.5, 'end': 12.0}]
    
    # 4. Mechanical Editing (FFmpeg)
    print("Step 3: Mechanical cutting via NVENC FFmpeg...")
    cut_video_path = f"/home/evo/studio_scratch/cut_{job_id}.mp4"
    cutter.process_cuts(raw_video_path, simulated_edl, cut_video_path)
    
    # 5. Remotion Render (Trigger Node.js)
    print("Step 4: Triggering Remotion for overlays and Ken Burns...")
    # Trigger Remotion CLI here passing the JSON triggers
    # subprocess.run(["npx", "remotion", "render", "remotion-renderer/src/index.ts", ...])
    
    print(f"Job {job_id} complete! Asset ready at {cut_video_path}")

def on_snapshot(col_snapshot, changes, read_time):
    print(f"\n--- Received snapshot at {read_time} ---")
    for change in changes:
        if change.type.name == 'ADDED':
            job_id = change.document.id
            job_data = change.document.to_dict()
            print(f"[NEW JOB] ID: {job_id}")
            
            # Trigger the pipeline for the new job
            try:
                run_pipeline(job_id, job_data)
            except Exception as e:
                print(f"Pipeline failed for {job_id}: {e}")
                
        elif change.type.name == 'MODIFIED':
            print(f"[MODIFIED JOB] ID: {change.document.id}")
        elif change.type.name == 'REMOVED':
            print(f"[REMOVED JOB] ID: {change.document.id}")

def main():
    load_dotenv()
    check_gpu()

    project_id = os.getenv("GCP_PROJECT_ID", "evolution-engine")
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not cred_path or not os.path.exists(cred_path):
        print(f"WARNING: GOOGLE_APPLICATION_CREDENTIALS path '{cred_path}' does not exist or is not set.")
    
    try:
        print(f"Initializing Firebase Admin for project '{project_id}'...")
        firebase_admin.initialize_app()
        db = firestore.client()
        
        print("Connecting to Firestore 'jobs' collection...")
        col_query = db.collection('jobs')
        col_query.on_snapshot(on_snapshot)
        
        print("Listening for jobs. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Error initializing Firestore listener: {e}")

if __name__ == "__main__":
    main()
