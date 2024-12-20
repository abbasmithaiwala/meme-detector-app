import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash-exp")

def detect_meme(image_file):
    image = Image.open(image_file)
    
    response = model.generate_content([image, "Identify the meme in the image. Provide a reference of it in brief. Also Name three memes relevant to the subject of this meme."])
    
    if response and hasattr(response, 'text'):
        detected_meme = response.text.strip()
    else:
        detected_meme = "Could not identify the meme."

    return {
        "Detected Meme": detected_meme
    }

# Streamlit UI
def main():
    st.title("Meme Detector App")
    st.write("Upload an image to detect the meme.")

    uploaded_image = st.file_uploader("Upload Meme Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        with st.spinner("Detecting meme and providing suggestions..."):
            result = detect_meme(uploaded_image)
        
        st.subheader("Results")
        st.write(f"**Detected Meme:** {result['Detected Meme']}")

if __name__ == "__main__":
    main()
