# Daily Drum Rudiment

A simple Python desktop app that displays a random drum rudiment each day, with a clickable link to its lesson and a video thumbnail. Built with Tkinter and web scraping.

## Features
- Fetches a random drum rudiment from [40drumrudiments.com](https://www.40drumrudiments.com)
- Displays the rudiment name (clickable to open the lesson)
- Shows a video thumbnail (clickable to open the video)
- Simple, modern Tkinter GUI

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies:
  - beautifulsoup4
  - requests
  - pillow
  - tk

Install dependencies with:
```bash
pip install -r requirements.txt
```

**Tip:** It's recommended to use a virtual environment. You can create one and install requirements in one step:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
Run the app with:
```bash
python main.py
```

## How it works
- `web_scraper.py` scrapes the rudiment list and video links.
- `main.py` builds the GUI, displays the rudiment, and handles user interaction.

## Notes
- The app downloads a thumbnail image for each session and **does not** delete it on exit.
- Requires an internet connection to fetch rudiment data and images.

## License
AGPL-3.0-or-later, see [LICENSE](LICENSE.md) for details.

---

*Made by Ary and [Fluf](https://github.com/ofluffydev/) :3*
