import streamlit as st
import requests
import urllib.parse

# --- UI SETTINGS ---
st.set_page_config(page_title="POD Tool Pro", layout="wide")
st.title("🎨 POD Designer Pro (Universal)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    user_api_key = st.text_input("Gemini API Key", type="password")

# --- AUTO-MODEL DISCOVERY ---
def find_my_model(key):
    # Kan-sowlo Google chnou 3ndna f l-keff (v1beta fiha kolchi)
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models_list = res.json().get('models', [])
            # N-9llbo 3la ay model kayslah l-ktaba (generateContent)
            for m in models_list:
                if 'generateContent' in m['supportedGenerationMethods']:
                    return m['name'] # Kay-rjje3 'models/gemini-1.5-flash' mtlm
    except:
        pass
    return None

# --- MAIN APP ---
niche = st.text_input("Niche Name:")

if st.button("Generate⚡"):
    if not user_api_key:
        st.error("❌ 3afak dkhel l-API Key dyalk l-issr!")
    else:
        with st.spinner("Searching for a working model..."):
            model_path = find_my_model(user_api_key)
            
            if not model_path:
                st.error("❌ Had l-API Key ma-khddama f 7ta model. T2kked menha f AI Studio.")
            else:
                st.info(f"✅ Model khddam: {model_path}")
                # URL daki 3la 7sab l-model li l9ina
                api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={user_api_key}"
                
                payload = {
                    "contents": [{"parts": [{"text": f"POD Expert: Give me 1 quote and 1 image prompt for niche '{niche}'. Format: Quote: [text] | Prompt: [text]"}]}]
                }
                
                try:
                    res = requests.post(api_url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        output = data['candidates'][0]['content']['parts'][0]['text']
                        
                        if "|" in output:
                            quote = output.split("|")[0].replace("Quote:", "").strip()
                            prompt = output.split("|")[1].replace("Prompt:", "").strip()
                            
                            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?nologo=true"
                            
                            st.success(f"Quote: {quote}")
                            st.image(img_url, width=400)
                            st.code(prompt)
                    else:
                        st.error(f"Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
