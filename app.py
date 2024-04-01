from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai 

# Configure Google API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set page title and description
st.set_page_config(
    page_title="Conversational Chat Bot",
    page_icon=":speech_balloon:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS style
custom_css = """
<style>
body {
    background-color: #f9f9f9;
    font-family: Arial, sans-serif;
    color: #333;
}

.stTextInput>div>div>input,
.stTextInput>div>div>textarea {
    background-color: #fff;
    color: #333;
    border-color: #ccc;
    border-radius: 5px;
    padding: 10px;
}

.stButton>button {
    background-color: #4CAF50;
    color: #fff;
    border-color: #4CAF50;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #45a049;
}

.stMarkdown a {
    color: #4CAF50;
}

.sidebar {
    padding: 20px;
    background-color: #f2f2f2;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar p {
    font-size: 14px;
    line-height: 1.5;
}
</style>
"""

# Display custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("About")
st.sidebar.write("This chat bot is powered by Gemini LLm.")
st.sidebar.write("It can respond to your questions based on the provided input.")
st.sidebar.write("Libraries and models used:")
st.sidebar.write("- Google GenerativeAI")
st.sidebar.write("- Gemini-Pro model")

# Center-aligned content
st.title("Conversational Chat Bot")
st.markdown("---")

# Image banner
image_url = "https://barhead.com/wp-content/uploads/2022/05/20220407_How-to-send-random-GIFs-via-your-Power-Virtual-Agents1901x444.jpg"
st.image(image_url, use_column_width=True)

# Input textbox
input_text = st.text_area("You:", key="input", value="", height=10, help="Type your message here")

# Button to send question
submit_button = st.button("ASK", key="submit", help="Click to send your message :envelope:")

# Check if chat history exists in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Handle question submission
if submit_button and input_text:
    response = get_gemini_response(input_text)
    st.session_state["chat_history"].append(("you", input_text))  # Append a tuple ('you', input)
    for chunk in response:
        st.session_state["chat_history"].append(("bot", chunk.text))  # Append a tuple ('bot', chunk.text)

# Chat history
for role, text in st.session_state["chat_history"]:
    if role == "you":
        st.write(f":bust_in_silhouette: You: {text}")
    else:
        st.write(f":robot_face: Bot: {text}")
