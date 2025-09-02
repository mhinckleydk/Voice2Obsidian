# summarize_and_save.py

from datetime import datetime
from pathlib import Path

def save_summary_to_obsidian(summary_text: str, vault_path: str = "D:/Dawnchant/Transcribed Notes", config: dict = None, transcript: str = None) -> str:
    """
    Save the summary to a markdown file in your Obsidian vault.

    Args:
        summary_text: The journal-style summary from Ollama
        vault_path: Full path to your Obsidian vault (e.g. 'D:/Dawnchant/Transcribed Notes')
        config: Configuration dictionary with filename_prefix and date_format
        transcript: Raw transcript to append at the bottom
    Returns:
        Path to the saved markdown file
    """
    if config:
        date_format = config.get('date_format', '%m-%d-%Y_%H-%M')
        filename_prefix = config.get('filename_prefix', 'Whispers of Wisdom')
        filename_iteration = config.get('filename_iteration', True)
    else:
        date_format = '%m-%d-%Y_%H-%M'
        filename_prefix = 'Whispers of Wisdom'
        filename_iteration = True
    
    date_str = datetime.now().strftime(date_format)
    base_title = f"{filename_prefix} - {date_str}"
    title = f"{base_title}.md"

    target_dir = Path(vault_path)
    target_dir.mkdir(parents=True, exist_ok=True)

    filepath = target_dir / title
    
    # Handle duplicate filenames by appending a number
    if filename_iteration and filepath.exists():
        counter = 1
        while filepath.exists():
            title = f"{base_title} ({counter}).md"
            filepath = target_dir / title
            counter += 1
    with open(filepath, "w", encoding="utf-8") as f:
        # Write the Ollama summary
        f.write(f"\n{summary_text.strip()}\n")
        
        # Add transcript at the bottom if provided
        if transcript:
            f.write(f"\n\n# Transcription\n{transcript.strip()}\n")

    return str(filepath)
