# 🍱 WasabiGit

> **"The automated sensei that builds my Japanese vocabulary."**

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/pronzzz/wasabigit/daily.yml?label=Daily%20Drill)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**WasabiGit** is a GitHub repository maintenance bot that automates daily Japanese vocabulary learning. Unlike other "commit bots" that generate garbage data, WasabiGit builds a useful database of vetted vocabulary.

---

## 📅 Daily Vocabulary
*Updated automatically at midnight UTC.*

<!-- VOCAB_START -->

**Current Status:** Learning for Japan 2027 🇯🇵
**Total Words Archived:** 4

## 📅 Word of the Day: 2026-01-17

| Kanji | Reading | Meaning |
|-------|---------|---------|
| **月** | つき | Moon |

<!-- VOCAB_END -->

---

## ✨ Features

- **Daily Trigger**: Runs automatically every day at 00:00 UTC via GitHub Actions.
- **Smart Fetching**: Pulls real data (Kanji, Reading, Meaning) from the [Jisho.org API](https://jisho.org/).
- **Data Persistence**: Archives every word into `vocabulary_archive.json`.
- **Dynamic Profile**: Updates this README with the "Card of the Day".
- **Zero Maintenance**: Once setup, it runs entirely on GitHub.

## 🚀 Setup & Usage

### 1. Installation
Clone the repository or verify the files are in place:
```bash
git clone https://github.com/pronzzz/wasabigit.git
cd wasabigit
```

### 2. Configuration
- **Seed List**: Edit `words_seed.txt` to add or remove words you want to learn.
- **Schedule**: Modify `.github/workflows/daily.yml` to change the cron schedule (default: `0 0 * * *`).

### 3. Manual Run
You can run the bot locally to test it:
```bash
pip install requests
python daily_bot.py
```

## 🛠️ Project Structure

- `daily_bot.py`: Main logic script.
- `words_seed.txt`: Source list of vocabulary words.
- `vocabulary_archive.json`: Database of learned words.
- `.github/workflows/daily.yml`: Automation configuration.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
