# Voice Journal

A Python-based voice journaling application that records audio, transcribes it using OpenAI Whisper, and creates beautiful journal entries using Ollama AI models.

## Features

- **Live Voice Recording**: Record your thoughts in real-time with simple voice commands
- **Batch Processing**: Process existing audio files (.mp4, .wav) from a folder
- **AI Transcription**: Uses OpenAI Whisper for accurate speech-to-text conversion
- **Intelligent Summarization**: Leverages Ollama to create thoughtful, journal-style summaries
- **Dual Output**: Saves to both local Obsidian vault and external directories
- **Configurable**: Customizable prompts, file naming, and storage locations

## Prerequisites

- **Python 3.8+**
- **Ollama** installed and running locally
  - Download from [https://ollama.ai/](https://ollama.ai/)
  - Install a model (e.g., `ollama pull llama3`)

## Quick Setup

1. **Clone or download this repository**

2. **Run the setup script**:
   ```bash
   python setup.py
   ```
   
   This will:
   - Check your Python version
   - Install all required dependencies
   - Create necessary directories
   - Verify Ollama connectivity
   - Set up the environment

3. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

4. **Configure your settings** (optional):
   Edit `config/settings.py` to customize:
   - AI model to use
   - Output directories
   - Journal prompt style
   - File naming conventions

## Usage

### Live Voice Journaling

```bash
python scripts/journal.py
```

- Start speaking when prompted
- Type `summarize` when finished to process your recording
- Your journal entry will be saved automatically

### Process Existing Audio Files

1. Place audio files (.mp4, .wav) in the `recordings_to_summarize/` folder
2. Run:
   ```bash
   python scripts/preloaded_recording.py
   ```
3. All files will be processed and moved to the `sessions/` folder

## Directory Structure

```
voice-journal/
├── config/
│   └── settings.py          # Configuration settings
├── scripts/
│   ├── journal.py           # Live voice recording
│   ├── preloaded_recording.py # Batch audio processing
│   └── summarize_and_save.py   # Core saving functionality
├── sessions/                # Processed audio files
├── recordings_to_summarize/ # Drop audio files here for batch processing
├── obsidian/
│   └── VoiceNotes/         # Local Obsidian vault output
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
└── README.md              # This file
```

## Configuration

Edit `config/settings.py` to customize:

```python
config = {
    "model": "llama3",  # Ollama model to use
    "obsidian_path": "./obsidian/VoiceNotes",
    "transcribed_notes_path": "D:/Your/Path/Here",
    "filename_prefix": "Whispers of Wisdom",
    "date_format": "%m-%d-%Y",
    "journal_prompt": "Your custom prompt here..."
}
```

## Dependencies

- `sounddevice` - Audio recording
- `numpy` - Numerical operations
- `scipy` - Audio file handling
- `openai-whisper` - Speech transcription
- `requests` - Ollama API communication
- `librosa` & `soundfile` - Enhanced audio format support

## Troubleshooting
- Make sure you adjust the Path to your obsidian
- Double check the prompt that it feeds to Llama3 (which was the best model I could get to work) - you might want to adjust the style

### Common Issues

1. **"Ollama not accessible"**
   - Make sure Ollama is installed and running (`ollama serve`)
   - Check that port 11434 is not blocked

2. **Audio recording issues**
   - Check microphone permissions
   - Verify audio device availability

3. **Import errors**
   - Run `python setup.py` to reinstall dependencies
   - Check Python version (3.8+ required)

### Getting Help

1. Check that all dependencies are installed: `pip list`
2. Verify Ollama is running: `curl http://localhost:11434/api/version`
3. Test microphone: Run a simple recording test

## Development

To contribute or modify:

1. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

2. Run tests:
   ```bash
   pytest
   ```

## License

This project is open source. Feel free to modify and distribute as needed.

---

**Happy Journaling! 🎙️📝**
