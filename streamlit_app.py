import streamlit as st
import requests
import urllib.parse
import re

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Universal Fix)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    user_api_key = st.text_input("Gemini API Key", type="password")

# --- AUTO-MODEL DISCOVERY ---
def find_my_model(key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models_list = res.json().get('models', [])
            for m in models_list:
                if 'generateContent' in m['supportedGenerationMethods']:
                    return m['name']
    except: pass
    return None

# --- MAIN APP ---
niche = st.text_input("Niche Name (Ex: Funny Dog):")

if st.button("Generate⚡"):
    if not user_api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk l-issr f s-site!")
    else:
        model_path = find_my_model(user_api_key)
        if not model_path:
            st.error("❌ API Key error. Check it in AI Studio.")
        else:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={user_api_key}"
            prompt_instr = f"Act as a POD expert. Give me 1 short quote and 1 detailed image prompt for niche '{niche}'. Format exactly: Quote: [text] | Prompt: [text]. No dots at the end."
            
            with st.spinner("Generating..."):
                try:
                    res = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt_instr}]}]})
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        parts = output.split("|")
                        quote = parts[0].replace("Quote:", "").strip()
                        p_text = parts[1].replace("Prompt:", "").strip()
                        
                        # --- CLEANING L-PROMPT (MOUHIM BZAFF) ---
                        # Kan-7iydu ay 7aja mashi 7rouf awla ar9am bach l-lien may-t-khrbech
                        clean_p = re.sub(r'[^a-zA-Z0-9\s]', '', p_text).strip()
                        
                        # URL dyal t-swira (Pollinations AI)
                        encoded = urllib.parse.quote(clean_p)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&seed=42"
                        
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            # Kan-st3mlu had l-format bach n-forcew t-swira t-ban
                            st.image(image_url, use_container_width=True)
                        with col2:
                            st.success(f"**Quote:** {quote}")
                            st.info("**AI Image Prompt:**")
                            st.code(clean_p)
                    else:
                        st.warning("Format error. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
