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
    api_key = st.text_input("Gemini API Key", type="password")
    style_choice = st.selectbox("Style", [
        "Vintage Retro Sunset", 
        "Kawaii Cute", 
        "Dark Grunge", 
        "Neon Cyberpunk", 
        "Watercolor"
    ])

# --- MAIN INTERFACE ---
niche_input = st.text_area("Entrez vos niches (une par ligne or comma separated):")

if st.button("Generate Designs ⚡"):
    if not api_key:
        st.error("Nsiti l-API Key!")
    elif not niche_input:
        st.warning("Dkhel chi niche 3afak.")
    else:
        niches = [n.strip() for n in niche_input.replace("\n", ",").split(",") if n.strip()]
        
        results = []
        for niche in niches:
            with st.status(f"Génération pour : {niche}...", expanded=True):
                # Appel API (Direct Request)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                prompt = f"POD Expert: Design concept for niche '{niche}' in style '{style_choice}'. Quote: [text] | Prompt: [AI Image Prompt]"
                
                try:
                    res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                    content = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    quote = content.split("|")[0].replace("Quote:", "").strip()
                    img_prompt = content.split("|")[1].replace("Prompt:", "").strip()
                    
                    # Image Preview
                    encoded = urllib.parse.quote(img_prompt)
                    img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true"
                    
                    # Display Card
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(img_url)
                    with col2:
                        st.subheader(f"Niche: {niche}")
                        st.info(f"**Text:** {quote}")
                        st.code(img_prompt, language="text")
                    
                    results.append({"Niche": niche, "Quote": quote, "Prompt": img_prompt})
                except:
                    st.error(f"Error on {niche}")
        
        # --- EXPORT DATA ---
        if results:
            df = pd.DataFrame(results)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger le rapport CSV 📊", csv, "pod_results.csv", "text/csv")
