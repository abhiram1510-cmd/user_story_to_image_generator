#app.py
import streamlit as st #type:ignore
import requests
import io
import os
from PIL import Image #type:ignore
from dotenv import load_dotenv #type:ignore

# --- 1. CONFIGURATION & AI CONNECTION ---
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_hf(payload):
    try:st
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        # SUCCESS
        if response.status_code == 200:
            return response.content, None

        # TRY TO READ JSON ERROR
        try:
            error_json = response.json()
            error_message = error_json.get("error", str(error_json))
        except:
            error_message = response.text

        return None, f"Status {response.status_code}: {error_message}"

    except Exception as e:
        return None, str(e)

# --- 2. PROFESSIONAL UI SETUP ---
st.set_page_config(page_title="Visionary - User Story AI", page_icon="🚀", layout="wide")

# Custom CSS for Modern Styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        transform: scale(1.02);
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #4a4a4a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Project Metadata) ---
with st.sidebar:
    st.title("⚙️ Project Visionary")
    st.markdown("---")
    st.info("**📌 B.Tech III Year Mini Project**\n\n**👤 Developer:** Abhiram")
    
    style = st.selectbox("🎨 Select Visual Style", 
        ["Photorealistic UI", "Digital Illustration", "Technical Sketch", "3D Render", "Cyberpunk Art"])
    
    st.write("---")
    st.write("### How it works:")
    st.caption("1. Input a User Story (Requirement)")
    st.caption("2. AI processes text via HF Router")
    st.caption("3. Stable Diffusion XL generates visual")

# --- 4. MAIN INTERFACE (Split Layout) ---
# Make sure the is exactly like this:
col1, col2 = st.columns(2, gap="large")

with col1:
    st.title("🚀 User Story to Image")
    st.write("Bridge the gap between requirements and design using Generative AI.")
    
    user_story = st.text_area("Enter your User Story here:", height=200, 
        placeholder="As a user, I want a modern food delivery app dashboard showing a map and a list of nearby restaurants...")
    
    generate_btn = st.button(" Generate Visual Concept")

with col2:
    st.subheader("🖼️ Generated Visualization")
    
    if generate_btn:
        if not user_story:
            st.warning("⚠️ Please enter a user story first!")
        else:
            with st.spinner("🤖 AI is dreaming up your design..."):
                # Prompt Augmentation for better results
                enhanced_prompt = f"{style} concept for: {user_story}. High resolution, professional UI/UX design, 8k masterpiece."
                
                img_data, err = query_hf({"inputs": enhanced_prompt})
                
                if err:
                    if "loading" in err.lower():
                        st.info("🕒 The AI model is waking up (loading). Please wait 20 seconds and click 'Generate' again!")
                    else:
                        st.error(f" API Error: {err}")
                elif img_data:
                    # Successful generation
                    image = Image.open(io.BytesIO(img_data))
                    st.image(image, caption=f"Style: {style}", use_container_width=True)
                    st.success("Requirement Visualized Successfully!")
                    
                    # Modern Download Button
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label=" Download Concept PNG",
                        data=buf.getvalue(),
                        file_name="user_story_viz.png",
                        mime="image/png"
                    )
    else:
        # State before user clicks generate
        st.info("Your generated design concept will appear here after you click generate.")