import streamlit as st
import requests
import urllib.parse
import re

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Designer Pro", layout="wide")
st.title("🚀 POD Designer Pro (Final Stable)")

# --- GET API KEY FROM SECRETS ---
api_key = st.secrets.get("GEMINI_API_KEY")

# --- MAIN APP ---
niche = st.text_input("Niche Name (Ex: Funny Mechanic):")

if st.button("Generate Design ⚡"):
    if not api_key:
        st.error("❌ API Key missing in Streamlit Secrets!")
    elif not niche:
        st.warning("⚠️ Enter a niche first.")
    else:
        # URL stable m3a Gemini 1.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        with st.spinner("Talking to Gemini..."):
            try:
                instr = f"Act as a POD designer. Give 1 short quote and 1 image prompt for '{niche}'. Format: Quote | Prompt. No dots at the end."
                res = requests.post(url, json={"contents": [{"parts": [{"text": instr}]}]})
                
                if res.status_code == 200:
                    data = res.json()
                    # Check if 'candidates' exists to avoid the error
                    if 'candidates' in data:
                        output = data['candidates'][0]['content']['parts'][0]['text']
                        if "|" in output:
                            quote, p_text = output.split("|")
                            clean_p = re.sub(r'[^a-zA-Z0-9\s]', '', p_text).strip()
                            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean_p)}?width=1024&height=1024&nologo=true"
                            
                            st.markdown("---")
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                st.markdown(f"![Design]({img_url})")
                            with col2:
                                st.success(f"**Quote:** {quote.strip()}")
                                st.info("**AI Image Prompt:**")
                                st.code(clean_p)
                    else:
                        st.error(f"Google Response Error: {data}")
                else:
                    st.error(f"API Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"System Error: {str(e)}")
