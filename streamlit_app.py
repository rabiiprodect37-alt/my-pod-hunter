import streamlit as st
import requests
import urllib.parse

# --- UI ---
st.set_page_config(page_title="POD Tool", layout="wide")
st.title("🎨 POD Designer Pro")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    # KHLLI HADI KIMA HIYA - MATBEDDELHCH B L-KEY DYALK HNA
    user_api_key = st.text_input("Gemini API Key", type="password")

# --- APP ---
niche = st.text_input("Niche Name (Ex: Fishing Mom):")

if st.button("Generate⚡"):
    if not user_api_key:
        st.error("❌ 3afak dkhl l-API Key dyalk f l-sidebar (Settings)!")
    else:
        # URL dyal v1 (Stable ga3)
        api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={user_api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"POD Expert: Give me 1 quote and 1 image prompt for niche '{niche}'. Format: Quote: [text] | Prompt: [text]"}]}]
        }
        
        with st.spinner("Processing..."):
            try:
                res = requests.post(api_url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    output = data['candidates'][0]['content']['parts'][0]['text']
                    
                    if "|" in output:
                        quote = output.split("|")[0].replace("Quote:", "").strip()
                        prompt = output.split("|")[1].replace("Prompt:", "").strip()
                        
                        # Image
                        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?nologo=true"
                        
                        st.success(f"Quote: {quote}")
                        st.image(img_url, width=400)
                        st.code(prompt)
                else:
                    # Hna ghadi nchoufo l-ghalat b d-dabt
                    st.error(f"Google Response: {res.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
