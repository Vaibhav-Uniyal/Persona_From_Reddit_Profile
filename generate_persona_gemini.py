import json
import requests
import os
from dotenv import load_dotenv

def build_prompt(username, posts, comments, profile_photo=None):
    prompt = f"""
You are an expert at building user personas. Given the following Reddit posts and comments from a user, generate a detailed persona as a JSON object with the following fields:

{{
  "name": "",
  "age": "",
  "occupation": "",
  "status": "",
  "location": "",
  "archetype": "",
  "traits": [{{"trait": "", "source": ""}}],
  "motivations": [{{"label": "", "value": 0, "source": ""}}],
  "personality": [{{"label": "", "value": 0, "source": ""}}],
  "habits": [{{"text": "", "source": ""}}],
  "frustrations": [{{"text": "", "source": ""}}],
  "goals": [{{"text": "", "source": ""}}],
  "quote": "",
  "citations": [""],
  "profile_photo": ""
}}

- For each trait, motivation, personality, habit, frustration, and goal, include a 'source' field with the Reddit post or comment URL you used to infer that information.
- For motivations and personality, use numbers from 0 to 100 for the 'value' field to represent bar length.
- The 'profile_photo' field MUST be set to this Reddit profile photo URL: {profile_photo if profile_photo else '[NO PHOTO AVAILABLE]'}
- The 'citations' field should be a list of all unique Reddit URLs referenced in the persona.
- Output ONLY a valid JSON object. DO NOT include any markdown, do not wrap the output in ```json or ``` or any other formatting, and do not add any extra text before or after the JSON.

Reddit Data:
"""
    for post in posts[:10]:
        prompt += f"\nPOST: Title: {post['title']} | Body: {post['body'][:200]} | URL: {post['url']}"
    for comment in comments[:10]:
        prompt += f"\nCOMMENT: {comment['body'][:200]} | URL: {comment['url']}"
    prompt += "\n\nGenerate the persona as described above."
    return prompt

def call_gemini_flash_api(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        print("Error from Gemini API:", response.text)
        return None

def main():
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    json_filename = input("Enter the Reddit data JSON filename (e.g., kojied_data.json): ")
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    username = data['username']
    posts = data['posts']
    comments = data['comments']
    profile_photo = data.get('profile_photo')
    prompt = build_prompt(username, posts, comments, profile_photo)
    print("Sending prompt to Gemini Flash API...")
    persona = call_gemini_flash_api(api_key, prompt)
    if persona:
        output_filename = f"{username}_persona.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(persona)
        print(f"Persona saved to {output_filename}")
    else:
        print("Failed to generate persona.")

if __name__ == "__main__":
    main() 