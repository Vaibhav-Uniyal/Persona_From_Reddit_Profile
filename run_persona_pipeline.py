import subprocess
import sys
import os
import json
from reddit_scraper import fetch_user_data
from generate_persona_gemini import call_gemini_flash_api, build_prompt
from dotenv import load_dotenv

# 1. Get Reddit username
username = input("Enter Reddit username (without u/): ")

# 2. Scrape Reddit data
fetch_user_data(username)
json_filename = f"{username}_data.json"

# 3. Load scraped data
with open(json_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 4. Generate persona JSON using Gemini
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    api_key = input("Enter your Gemini API key: ")
profile_photo = data.get('profile_photo')
prompt = build_prompt(username, data['posts'], data['comments'], profile_photo)
print("Sending prompt to Gemini Flash API...")
persona_json_str = call_gemini_flash_api(api_key, prompt)

# 5. Save persona JSON

if persona_json_str.startswith("```json"):
    persona_json_str = persona_json_str[len("'''json"):].lstrip()
if persona_json_str.endswith("```"):
    persona_json_str = persona_json_str[:-3].rstrip()
persona_filename = f"{username}_persona.json"


with open(persona_filename, 'w', encoding='utf-8') as f:
    f.write(persona_json_str)
print(f"Persona JSON saved to {persona_filename}")

# 6. Launch Streamlit dashboard and auto-load the persona JSON
print("Launching Streamlit dashboard...")
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'persona_dashboard.py', '--', persona_filename]) 
