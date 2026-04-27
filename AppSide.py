import streamlit as st
import google.generativeai as genai
from PIL import Image
 
st.title("🌾 Agro Assistant")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
 
SYSTEM_PROMPT = """
You are an agricultural expert AI. ONLY answer questions related to farming,
plants, and animals. Help users identify diseases from images and recommend
treatments. Give planting and farming advice. If a question is not about
agriculture or animal and plant related, politely decline and stay on topic.
"""
 
if "chat" not in st.session_state:
    genai.configure(api_key=api_key or "placeholder")
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat = model.start_chat()
 
# Display history — safely skip image parts (they have no .text)
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:
            if hasattr(part, "text") and part.text:
                st.markdown(part.text)
 
image_file = st.file_uploader("📷 Upload a plant or animal photo (optional)", type=["jpg", "jpeg", "png", "webp"], max_upload_size=10)
user_input = st.chat_input("Ask about your farm, crop, plant, or animal...")
 
if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
        st.stop()
 
    genai.configure(api_key=api_key)
 
    message = [user_input]
    if image_file:
        message.append(Image.open(image_file))
 
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(message, stream=True)
        st.write_stream(chunk.text for chunk in response if chunk.text)
 
    st.rerun()