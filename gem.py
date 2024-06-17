import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

if 'chat_history' not in st.session_state:  # Initialize chat history in session state if not present
    st.session_state.chat_history = []
chat_history_str=""
#Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = model.start_chat(history=[])
    

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini-Chatbot!",
    page_icon="🤖",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("Gemini-Chatbot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(f"You: {user_prompt}")#new

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.session_state.chat_history.append(f"Assistant: {gemini_response.text}")
    chat_history_str = "\n".join(st.session_state.chat_history)
    # Display Gemini-Pro's response

    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

#sidebar
st.sidebar.button('Clear Chat History', on_click=clear_chat_history())
st.sidebar.download_button(label="Download chat",
    data=chat_history_str,
    file_name="chat_history.txt",
    mime="text/plain")

