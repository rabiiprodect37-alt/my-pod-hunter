
import streamlit as st
import requests
import urllib.parse

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Final Fix)")

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
niche = st.text_input("Niche Name (Ex: Fishing Dad):")

if st.button("Generate⚡"):
    if not user_api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk l-issr!")
    else:
        model_path = find_my_model(user_api_key)
        if not model_path:
            st.error("❌ API Key error. Check it in AI Studio.")
        else:
            # Kan-sta3mlo l-model li l9ina (ghaliban flash)
            api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={user_api_key}"
            
            # PROMPT MJHD: Kan-charfo 3la Gemini y-3tina format nqi
            prompt_instr = f"POD Expert: Create 1 short quote and 1 image prompt for niche '{niche}'. Format exactly like this: Quote: [text] | Prompt: [text]. Do not add any other text."
            
            with st.spinner("Generating design..."):
                try:
                    res = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt_instr}]}]})
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        quote = output.split("|")[0].replace("Quote:", "").strip()
                        p_text = output.split("|")[1].replace("Prompt:", "").strip()
                        
                        # --- CLEANING L-PROMPT ---
                        # Bach n-t-fadao ay ktaba zayda kat-khsser l-lien
                        clean_p = p_text.replace("\n", " ").strip()
                        
                        # --- GENERATION DYAL T-SWIRA ---
                        encoded = urllib.parse.quote(clean_p)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=800&nologo=true"
                        
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            # Hna fin t-swira ghadi t-ban darouri
                            st.image(image_url, use_container_width=True)
                        with col2:
                            st.success(f"**Quote:** {quote}")
                            st.info("**AI Image Prompt:**")
                            st.code(clean_p)
                    else:
                        st.warning("Google didn't use the correct format. Try again.")
                        st.write(output)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("POD Tool - Professional Edition")
