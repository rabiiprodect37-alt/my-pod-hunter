
import streamlit as st
import requests
import urllib.parse
import pandas as pd

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Niche Hunter", layout="wide")
st.title("🚀 POD Niche Hunter Pro")
st.write("Générer des designs en masse avec l'intelligence artificielle.")

# --- SIDEBAR (Settings) ---
with st.sidebar:
    st.header("Settings")
    # Hna fin khassk t-coller s-sarout dyalk
    api_key = st.text_input("Gemini API Key", type="password", help="Dkhel l-API Key dyalk li katsali b ...4gHA")
    style_choice = st.selectbox("Style", [
        "Vintage Retro Sunset", 
        "Kawaii Cute", 
        "Dark Grunge", 
        "Neon Cyberpunk", 
        "Watercolor"
    ])

# --- MAIN INTERFACE ---
niche_input = st.text_area("Entrez vos niches (séparées par des virgules) :", placeholder="Ex: Cat Mom, Fishing Dad, Gamer")

if st.button("Generate Designs ⚡"):
    if not api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk f l-sidebar (jiha dyal l-issr)!")
    elif not niche_input:
        st.warning("⚠️ Ktb chi niche bach n9drou nkhdmou.")
    else:
        niches = [n.strip() for n in niche_input.split(",") if n.strip()]
        
        for niche in niches:
            with st.spinner(f"🕵️‍♂️ Gemini kay9lleb 3la afkar l: {niche}..."):
                # URL dyal Gemini Pro (Hada howa li stable)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Act as a POD expert. For the niche '{niche}' and style '{style_choice}', give me: 1 catchy Quote and 1 Image Prompt. Format: Quote: [text] | Prompt: [text]"
                        }]
                    }]
                }
                
                try:
                    res = requests.post(url, json=payload)
                    if res.status_code == 200:
                        content = res.json()['candidates'][0]['content']['parts'][0]['text']
                        
                        # Parsing
                        if "|" in content:
                            quote = content.split("|")[0].replace("Quote:", "").strip()
                            img_prompt = content.split("|")[1].replace("Prompt:", "").strip()
                            
                            # Image Preview
                            encoded = urllib.parse.quote(img_prompt)
                            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true"
                            
                            # Affichage
                            st.markdown("---")
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.image(img_url, caption=niche)
                            with col2:
                                st.subheader(f"💡 Niche: {niche}")
                                st.success(f"**Quote:** {quote}")
                                st.text_area("AI Image Prompt (Copy this):", img_prompt, height=100)
                        else:
                            st.write(content)
                    else:
                        st.error(f"❌ Error API ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Mochkil: {str(e)}")

st.markdown("---")
st.caption("Powered by Gemini Pro & Pollinations AI")
