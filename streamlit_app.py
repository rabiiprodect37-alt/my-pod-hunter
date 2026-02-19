import streamlit as st
import requests
import urllib.parse

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Niche Hunter Pro", layout="wide")
st.title("🚀 POD Niche Hunter Pro")

# --- SIDEBAR (Settings) ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("AIzaSyD29Q6dYX8D6Ho5iy4Ke-a0Lg6XK0_4gHA", type="password")
    style_choice = st.selectbox("Style", ["Vintage Retro Sunset", "Kawaii Cute", "Dark Grunge", "Neon Cyberpunk", "Watercolor"])

# --- AUTOMATIC MODEL DISCOVERY ---
def get_available_model(key):
    # Jarreb v1beta hit hiya li fiha l-ghalbiya d les models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models = res.json().get('models', [])
            # N9llbo 3la awwal model kheddam fih 'generateContent'
            for m in models:
                if 'generateContent' in m['supportedGenerationMethods']:
                    return m['name'] # Kayrjje3 matalan 'models/gemini-1.5-flash'
    except:
        pass
    return "models/gemini-pro" # Backup

# --- MAIN LOGIC ---
niche_input = st.text_area("Niches (separées par virgule):", placeholder="Ex: Nurse Life, Fishing Dad")

if st.button("Generate Designs ⚡"):
    if not api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk f l-sidebar!")
    elif not niche_input:
        st.warning("⚠️ Ktb chi niche.")
    else:
        # 1. Scanni l-model li kheddam l-had l-Key b-dabt
        working_model = get_available_model(api_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={api_key}"
        
        niches = [n.strip() for n in niche_input.split(",") if n.strip()]
        for niche in niches:
            with st.spinner(f"🕵️‍♂️ Génération avec {working_model}..."):
                payload = {
                    "contents": [{"parts": [{"text": f"Act as a POD expert. Niche: '{niche}', Style: '{style_choice}'. Provide: 1 catchy Quote and 1 Detailed AI Image Prompt. Format: Quote: [text] | Prompt: [text]"}]}]
                }
                
                try:
                    res = requests.post(url, json=payload)
                    if res.status_code == 200:
                        content = res.json()['candidates'][0]['content']['parts'][0]['text']
                        if "|" in content:
                            quote = content.split("|")[0].replace("Quote:", "").strip()
                            img_prompt = content.split("|")[1].replace("Prompt:", "").strip()
                            
                            encoded = urllib.parse.quote(img_prompt)
                            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true"
                            
                            st.markdown("---")
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.image(img_url)
                            with col2:
                                st.subheader(f"💡 {niche}")
                                st.success(f"Quote: {quote}")
                                st.code(img_prompt)
                    else:
                        st.error(f"❌ Error API: {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Mochkil: {str(e)}")
