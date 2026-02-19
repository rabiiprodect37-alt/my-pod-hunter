
import streamlit as st
import requests
import urllib.parse
import re

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Designer Pro", layout="wide")
st.title("🚀 POD Designer Pro (Auto-Connect)")

# --- GET API KEY FROM SECRETS ---
# L-app ghadi t-jbed s-sarout bo7dha daba mn l-khba
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None
    st.sidebar.error("❌ API Key missing in Secrets!")

# --- MAIN APP ---
niche = st.text_input("Niche Name (Ex: Funny Mechanic):")

if st.button("Generate Design ⚡"):
    if not api_key:
        st.error("⚠️ Khassk d-dkhl l-key f Streamlit Secrets!")
    elif not niche:
        st.warning("⚠️ Ktb chi niche.")
    else:
        # URL dyal Gemini 1.5 Flash (v1beta m3a Secrets)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        with st.spinner("Processing..."):
            try:
                # Prompt m7ded bach Gemini may-kherbech l-format
                instr = f"POD designer expert. Niche: '{niche}'. Give 1 quote and 1 image prompt. Format exactly: Quote | Prompt. No dots at the end."
                res = requests.post(url, json={"contents": [{"parts": [{"text": instr}]}]})
                output = res.json()['candidates'][0]['content']['parts'][0]['text']
                
                if "|" in output:
                    quote, p_text = output.split("|")
                    # Cleaning l-prompt bach tswira t-ban 100% (Force Clean)
                    clean_p = re.sub(r'[^a-zA-Z0-9\s]', '', p_text).strip()
                    
                    # URL dyal t-swira mn Pollinations
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean_p)}?width=1024&height=1024&nologo=true"
                    
                    st.markdown("---")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        # Force image display with Markdown
                        st.markdown(f"![Design]({img_url})")
                    with col2:
                        st.success(f"**Quote:** {quote.strip()}")
                        st.info("**AI Image Prompt:**")
                        st.code(clean_p)
                else:
                    st.write(output)
            except Exception as e:
                st.error(f"Error: {str(e)}")
