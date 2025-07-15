# Reddit User Persona Generator

This project scrapes a Reddit user's posts, comments, and profile photo, generates a detailed user persona using Gemini (Google's LLM), and displays the persona in a beautiful Streamlit dashboard—all with a single command.

---

## Features
- Scrapes Reddit user data (posts, comments, profile photo)
- Generates a structured persona with citations using Gemini
- Visualizes the persona in a modern dashboard (Streamlit)
- Fully automated: just enter a Reddit username!

---

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed.
```
pip install -r requirements.txt
```
If you don't have a `requirements.txt`, install manually:
```
pip install praw streamlit requests python-dotenv
```

### 3. API Credentials
- The required Reddit and Gemini API credentials will be provided for you.
- Ensure your `.env` file (with the Gemini API key) and the Reddit credentials in `reddit_scraper.py` are present in the project folder.

---

## Usage Instructions

### 1. Run the Automated Pipeline
```
python run_persona_pipeline.py
```
- Enter the Reddit username (without `u/`) when prompted.
- The script will:
  - Scrape Reddit data
  - Generate the persona JSON using Gemini
  - Launch the Streamlit dashboard and display the persona automatically

### 2. View the Persona
- The Streamlit app will open in your browser and show the generated persona, including profile photo, traits, motivations, habits, frustrations, goals, citations, and more.

---

## File Overview
- `reddit_scraper.py` — Scrapes Reddit user data
- `generate_persona_gemini.py` — Calls Gemini to generate persona JSON
- `persona_dashboard.py` — Streamlit dashboard for visualization
- `run_persona_pipeline.py` — Orchestrates the full workflow (just run this!)
- `.env` — Stores your Gemini API key

---

## Troubleshooting
- **Reddit API errors:** Double-check your credentials and app type (must be "script").
- **Gemini API errors:** If you see "model overloaded" or 503, wait and try again.
- **Streamlit not opening:** Make sure all dependencies are installed and no firewall is blocking the port.

---

## Credits
- Built with [PRAW](https://praw.readthedocs.io/), [Streamlit](https://streamlit.io/), and [Gemini API](https://ai.google.dev/).

---

## License
MIT License 