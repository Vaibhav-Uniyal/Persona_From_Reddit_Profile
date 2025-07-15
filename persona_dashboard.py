import streamlit as st
import json
import os
import sys

# Helper to render horizontal bar
def render_bar(label, value, max_value=100):
    bar_width = int((value / max_value) * 100)
    st.markdown(f"<div style='display:flex;align-items:center;'><div style='width:120px;'>{label}</div>"
                f"<div style='background:#eee;width:200px;height:18px;border-radius:5px;overflow:hidden;margin:0 8px;display:inline-block;'><div style='background:#e67e22;width:{bar_width}%;height:18px;'></div></div>"
                f"<div style='width:30px;text-align:right;'>{value}</div></div>", unsafe_allow_html=True)

def render_tags(tags):
    st.markdown(' '.join([f"<span style='background:#eee;border-radius:5px;padding:0.2em 0.7em;margin-right:0.5em;'>{tag['trait'] if isinstance(tag, dict) else tag}</span>" for tag in tags]), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="User Persona Dashboard", layout="wide")
    st.title("User Persona Dashboard")
    st.write("Upload a persona JSON file to visualize the persona in a structured, visually appealing format.")

    # Check for command-line argument for persona JSON file
    persona_json_path = None
    if len(sys.argv) > 1:
        persona_json_path = sys.argv[-1]
        if not os.path.isfile(persona_json_path):
            persona_json_path = None

    data = None
    if persona_json_path:
        with open(persona_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        uploaded_file = st.file_uploader("Upload Persona JSON", type=["json"])
        if uploaded_file is not None:
            data = json.load(uploaded_file)

    if data is not None:
        # Layout: 2 columns (photo+quote | persona info)
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(data.get("profile_photo", "https://via.placeholder.com/300x350.png?text=Profile+Photo"), width=300)
            if data.get("quote"):
                st.markdown(f"<div style='background:#e67e22;color:#fff;padding:1em;border-radius:8px;font-style:italic;margin-top:1em;'>{data['quote']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span style='color:#e67e22;font-size:2rem;font-weight:bold'>{data.get('name', 'Name')}</span>")
            st.write(f"**AGE:** {data.get('age','')}  ",
                     f"**OCCUPATION:** {data.get('occupation','')}")
            st.write(f"**STATUS:** {data.get('status','')}  ",
                     f"**LOCATION:** {data.get('location','')}")
            st.write(f"**ARCHETYPE:** {data.get('archetype','')}")
            if data.get('traits'):
                render_tags(data['traits'])
            st.markdown("---")
            # Motivations
            st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>MOTIVATIONS</span>", unsafe_allow_html=True)
            for mot in data.get('motivations', []):
                render_bar(mot['label'], mot['value'])
            # Personality
            st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>PERSONALITY</span>", unsafe_allow_html=True)
            for pers in data.get('personality', []):
                render_bar(pers['label'], pers['value'])
            # Habits
            st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>BEHAVIOUR & HABITS</span>", unsafe_allow_html=True)
            for habit in data.get('habits', []):
                st.markdown(f"- {habit['text']}")
                st.markdown(f"<span style='font-size:0.85em;color:#888;margin-left:2em;'>{habit['source']}</span>", unsafe_allow_html=True)
            # Frustrations
            st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>FRUSTRATIONS</span>", unsafe_allow_html=True)
            for fr in data.get('frustrations', []):
                st.markdown(f"- {fr['text']}")
                st.markdown(f"<span style='font-size:0.85em;color:#888;margin-left:2em;'>{fr['source']}</span>", unsafe_allow_html=True)
            # Goals & Needs
            st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>GOALS & NEEDS</span>", unsafe_allow_html=True)
            for goal in data.get('goals', []):
                st.markdown(f"- {goal['text']}")
                st.markdown(f"<span style='font-size:0.85em;color:#888;margin-left:2em;'>{goal['source']}</span>", unsafe_allow_html=True)
            # Citations
            if data.get('citations'):
                st.markdown("<span style='color:#e67e22;font-weight:bold;font-size:1.2rem;'>CITATIONS</span>", unsafe_allow_html=True)
                for cite in data['citations']:
                    st.markdown(f"- {cite}")

if __name__ == "__main__":
    main() 