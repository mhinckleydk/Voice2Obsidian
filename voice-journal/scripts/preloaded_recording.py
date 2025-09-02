# Process existing audio files from recordings_to_summarize folder
# Transcribes with Whisper and processes through Ollama like journal.py

import json
import os
import shutil
import whisper
import requests
from pathlib import Path
from datetime import datetime

# Load configuration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import config

def get_audio_files():
    """Get all .mp4 and .wav files from recordings_to_summarize folder"""
    recordings_dir = Path('recordings_to_summarize')
    if not recordings_dir.exists():
        print(f"❌ Directory {recordings_dir} does not exist")
        return []
    
    audio_files = []
    for file_path in recordings_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.mp4', '.wav']:
            audio_files.append(file_path)
    
    return audio_files

def transcribe_audio_file(file_path):
    """Transcribe audio file using Whisper"""
    print(f"🔄 Transcribing {file_path.name}...")
    
    try:
        model = whisper.load_model("base")
        result = model.transcribe(str(file_path))
        
        print(f"📝 Transcription complete for {file_path.name}")
        return result['text']
    except Exception as e:
        print(f"❌ Error transcribing {file_path.name}: {e}")
        return None

def summarize_with_ollama(text, filename):
    """Send text to Ollama for summarization using same prompt as journal.py"""
    print(f"🤖 Processing {filename} with Ollama...")
    
    # Use journal prompt with transcript
    prompt = config['journal_prompt'].format(transcript=text)
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                               json={
                                   'model': config['model'],
                                   'prompt': prompt,
                                   'stream': False
                               })
        
        if response.status_code == 200:
            summary = response.json()['response']
            print(f"📋 Summary generated for {filename}")
            
            # Save to configured paths
            from summarize_and_save import save_summary_to_obsidian
            
            # Save to obsidian vault
            obsidian_path = config.get('obsidian_path', './obsidian')
            filepath_obsidian = save_summary_to_obsidian(summary, obsidian_path, config, text)
            print(f"💾 Saved to Obsidian vault: {filepath_obsidian}")

            # Save to transcribed notes folder
            transcribed_path = config.get('transcribed_notes_path', 'D:/Dawnchant/Transcribed Notes')
            filepath_pc = save_summary_to_obsidian(summary, transcribed_path, config, text)
            print(f"💾 Also saved to: {filepath_pc}")
            
            return True
            
        else:
            print(f"❌ Ollama error for {filename}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Ollama for {filename}: {e}")
        return False

def move_to_sessions(file_path):
    """Move processed audio file to sessions folder"""
    sessions_dir = Path('sessions')
    sessions_dir.mkdir(exist_ok=True)
    
    # Create unique filename with timestamp if file already exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    destination = sessions_dir / new_name
    
    try:
        shutil.move(str(file_path), str(destination))
        print(f"📁 Moved {file_path.name} to sessions/{new_name}")
        return True
    except Exception as e:
        print(f"❌ Error moving {file_path.name}: {e}")
        return False

def process_all_recordings():
    """Main function to process all audio files in recordings_to_summarize"""
    print("🎵 Processing preloaded recordings...")
    
    audio_files = get_audio_files()
    
    if not audio_files:
        print("📂 No audio files found in recordings_to_summarize folder")
        return
    
    print(f"🔍 Found {len(audio_files)} audio file(s) to process")
    
    successful_processes = 0
    
    for file_path in audio_files:
        print(f"\n{'='*50}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*50}")
        
        # Step 1: Transcribe
        transcript = transcribe_audio_file(file_path)
        if not transcript:
            print(f"⏭️ Skipping {file_path.name} due to transcription error")
            continue
        
        # Step 2: Summarize with Ollama
        success = summarize_with_ollama(transcript, file_path.name)
        if not success:
            print(f"⏭️ Skipping {file_path.name} due to Ollama error")
            continue
        
        # Step 3: Move to sessions
        if move_to_sessions(file_path):
            successful_processes += 1
            print(f"✅ Successfully processed {file_path.name}")
        else:
            print(f"⚠️ Processed {file_path.name} but failed to move to sessions")
    
    print(f"\n🎉 Processing complete! Successfully processed {successful_processes}/{len(audio_files)} files")

if __name__ == "__main__":
    process_all_recordings()
