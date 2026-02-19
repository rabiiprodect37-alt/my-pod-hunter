import streamlit as st
import requests
import urllib.parse

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Full Version)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    # KHLLI HADA KIMA HOWA - MAT-BEDDELHCH B L-KEY DYALK HNA
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
        st.error("❌ 3afak dkhel l-API Key dyalk l-issr!")
    else:
        model_path = find_my_model(user_api_key)
        if not model_path:
            st.error("❌ Had l-API Key ma-khddama f 7ta model.")
        else:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={user_api_key}"
            prompt_instr = f"POD Expert: Give me 1 short quote and 1 image prompt for niche '{niche}'. Format: Quote: [text] | Prompt: [text]"
            
            with st.spinner("Generating..."):
                try:
                    res = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt_instr}]}]})
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        quote = output.split("|")[0].replace("Quote:", "").strip()
                        p_text = output.split("|")[1].replace("Prompt:", "").strip()
                        
                        # --- HADA HOWA S-STER DYAL T-SAWER ---
                        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p_text)}?width=512&height=512&nologo=true"
                        
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.image(img_url, caption=f"Design: {niche}")
                        with col2:
                            st.success(f"**Quote:** {quote}")
                            st.info("**AI Image Prompt:**")
                            st.code(p_text)
                    else:
                        st.write(output)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
