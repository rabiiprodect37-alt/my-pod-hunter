import streamlit as st
import requests
import urllib.parse

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Universal Fix)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    # KHLLI HADA KIMA HOWA - MAT-BEDDELHCH B L-KEY DYALK HNA
    user_api_key = st.text_input("AIzaSyCFm8t7_z0JaVyYlLJzyBOfaar20RUUn6o", type="password")

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
            prompt_instr = f"Act as a POD expert. Give me 1 quote and 1 image prompt for niche '{niche}'. Format exactly like this: Quote: [text] | Prompt: [text]. Do not add any extra text or new lines."
            
            with st.spinner("Generating design..."):
                try:
                    res = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt_instr}]}]})
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        parts = output.split("|")
                        quote = parts[0].replace("Quote:", "").strip()
                        p_text = parts[1].replace("Prompt:", "").strip()
                        
                        # Cleaning l-prompt bach tswira t-ban darouri
                        clean_p = p_text.replace("\n", " ").replace("\r", " ").strip()
                        
                        # URL dyal t-swira
                        encoded = urllib.parse.quote(clean_p)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=800&nologo=true"
                        
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            # Hna t-swira ghadi t-ban 100%
                            st.image(image_url, caption=f"Design: {niche}", use_container_width=True)
                        with col2:
                            st.success(f"**Quote:** {quote}")
                            st.info("**AI Image Prompt:**")
                            st.code(clean_p)
                    else:
                        st.warning("Google format error. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
