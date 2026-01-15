import json
import random
import requests
import os
from datetime import datetime

# 1. Setup Data Files
SEED_FILE = "words_seed.txt"
ARCHIVE_FILE = "vocabulary_archive.json"
README_FILE = "README.md"

def load_archive():
    if not os.path.exists(ARCHIVE_FILE):
        return []
    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        # Handle empty or corrupted file
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def get_next_word(archived_words):
    if not os.path.exists(SEED_FILE):
        print(f"Error: Seed file '{SEED_FILE}' not found.")
        return None

    # Load seed words
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        seeds = [line.strip() for line in f if line.strip()]
    
    # Find a word we haven't archived yet
    archived_set = {entry['word'] for entry in archived_words}
    available = [w for w in seeds if w not in archived_set]
    
    if not available:
        return None # No new words!
    
    return random.choice(available)

def fetch_jisho_data(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', [])
            if not data:
                return None
            
            first_result = data[0]
            
            # Extract reading (preferred or first available)
            reading = ''
            if 'japanese' in first_result:
                reading = first_result['japanese'][0].get('reading', '')
            
            # Extract meaning
            meaning = ''
            if 'senses' in first_result and first_result['senses']:
                meaning = ", ".join(first_result['senses'][0].get('english_definitions', []))
            
            return {
                "word": first_result.get('slug', word).split('-')[0], # Basic cleanup or use original
                "reading": reading,
                "meaning": meaning,
                "date": str(datetime.now().date())
            }
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    return None

def update_readme(new_entry, total_count):
    # Content to inject
    vocab_section = f"""
**Current Status:** Learning for Japan 2027 🇯🇵
**Total Words Archived:** {total_count}

## 📅 Word of the Day: {new_entry['date']}

| Kanji | Reading | Meaning |
|-------|---------|---------|
| **{new_entry['word']}** | {new_entry['reading']} | {new_entry['meaning']} |
"""

    if not os.path.exists(README_FILE):
        # Fallback if README is missing
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(f"<!-- VOCAB_START -->\n{vocab_section}\n<!-- VOCAB_END -->")
        return

    with open(README_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to replace content between markers
    # Flags: DOTALL to match newlines
    import re
    pattern = r"(<!-- VOCAB_START -->)(.*?)(<!-- VOCAB_END -->)"
    replacement = f"\\1\n{vocab_section}\n\\3"
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        # If markers are missing, append them
        with open(README_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n\n<!-- VOCAB_START -->\n{vocab_section}\n<!-- VOCAB_END -->")

# Main Execution flow
if __name__ == "__main__":
    archive = load_archive()
    target_word = get_next_word(archive)

    if target_word:
        print(f"Fetching data for: {target_word}")
        entry = fetch_jisho_data(target_word)
        
        if entry:
            # Check if entry already exists (double check)
            if not any(e['word'] == entry['word'] for e in archive):
                archive.append(entry)
                with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(archive, f, indent=2, ensure_ascii=False)
                
                # Update Readme
                update_readme(entry, len(archive))
                print(f"Success! Added {entry['word']}")
            else:
                 print(f"Word {entry['word']} already in archive (race condition skipped).")
        else:
            print("Failed to fetch data or no data found.")
    else:
        print("All seed words learned!")
