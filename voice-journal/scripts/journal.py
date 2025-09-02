# Voice Journal - Live transcription with Ollama summarization
# Type 'summarize' to process your recording

import json
import time
import sounddevice as sd
import numpy as np
import whisper
import requests
from pathlib import Path

# Load configuration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import config



# Audio settings
SAMPLE_RATE = 16000
recording_data = []
is_recording = False

def start_recording():
    """Start continuous audio recording"""
    global recording_data, is_recording
    recording_data = []
    is_recording = True
    print("🎤 Recording started... (type 'summarize' to finish)")
    
    def callback(indata, frames, time, status):
        if is_recording:
            recording_data.extend(indata.copy())
    
    # Start recording stream
    stream = sd.InputStream(callback=callback, channels=1, samplerate=SAMPLE_RATE)
    stream.start()
    return stream

def stop_recording_and_transcribe(stream):
    """Stop recording and transcribe with Whisper"""
    global recording_data, is_recording
    is_recording = False
    stream.stop()
    stream.close()
    
    if not recording_data:
        print("No audio recorded")
        return ""
    
    # Save audio to temporary file
    audio_array = np.array(recording_data, dtype=np.float32)
    timestamp = int(time.time())
    
    # Get the parent directory of the scripts folder (voice-journal)
    script_dir = Path(__file__).parent
    sessions_dir = script_dir.parent / "sessions"
    sessions_dir.mkdir(exist_ok=True)  # Create sessions directory if it doesn't exist
    filename = sessions_dir / f"recording_{timestamp}.wav"
    
    from scipy.io.wavfile import write
    write(str(filename), SAMPLE_RATE, (audio_array * 32767).astype(np.int16))
    
    # Transcribe with Whisper
    print("🔄 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(str(filename))
    
    print(f"📝 Transcription:\n{result['text']}")
    return result['text']

def summarize_with_ollama(text):
    """Send text to Ollama for summarization"""
    # Save transcript to settings
    config['transcript'] = text
    # Note: transcript is now stored in memory only, not persisted to file
    
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
            print(f"📋 Summary:\n{summary}")
            
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
            
        else:
            print(f"❌ Ollama error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")

def main():
    """Main journal loop"""
    print("Voice Journal Ready")
    print("Commands: 'summarize' to finish and process recording")
    
    stream = start_recording()
    
    try:
        while True:
            command = input().strip().lower()
            
            if command == 'summarize':
                text = stop_recording_and_transcribe(stream)
                if text:
                    summarize_with_ollama(text)
                break
                
    except KeyboardInterrupt:
        print("\n👋 Journal session ended")
        if is_recording:
            stream.stop()
            stream.close()

def start_journal():
    """Wrapper function to start journal from Python interpreter"""
    main()

if __name__ == "__main__":
    main()
