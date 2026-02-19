import streamlit as st
import requests
import urllib.parse
import re

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Force Image Fix)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    # Darouri t-coller s-sarout dyal Gemini hna f s-site mli t-7ello
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
niche = st.text_input("Niche Name (Ex: Fishing Dad):")

if st.button("Generate⚡"):
    if not user_api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk l-issr f s-site!")
    else:
        model_path = find_my_model(user_api_key)
        if not model_path:
            st.error("❌ API Key error. Check it in AI Studio.")
        else:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={user_api_key}"
            
            # Instruction sghira o m7deda bzaf
            prompt_instr = f"Act as a POD expert. Give me 1 quote and 1 image prompt for niche '{niche}'. Format exactly: Quote: [text] | Prompt: [text]. No quotes, no extra words."
            
            with st.spinner("Generating..."):
                try:
                    res = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt_instr}]}]})
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        parts = output.split("|")
                        quote = parts[0].replace("Quote:", "").strip()
                        p_text = parts[1].replace("Prompt:", "").strip()
                        
                        # --- SUPER CLEANING (ALPHA VERSION) ---
                        # Had s-ster kiy-khlli gher l-7rouf o l-ar9am
                        clean_p = re.sub(r'[^a-zA-Z0-9\s]', '', p_text).strip()
                        
                        # --- URL GENERATION ---
                        encoded = urllib.parse.quote(clean_p)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
                        
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            # Tariqa jdida dyal Markdown bach n-t-fadao broken images
                            st.markdown(f"![Design]({image_url})")
                        with col2:
                            st.success(f"**Quote:** {quote}")
                            st.info("**AI Image Prompt:**")
                            st.code(clean_p)
                    else:
                        st.warning("Format error. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
