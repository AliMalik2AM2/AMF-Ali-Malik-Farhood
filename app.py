import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Chatbot", layout="centered")

# Custom CSS for English support (Left-to-Right)
st.markdown("""
    <style>
    .stMarkdown { text-align: left; direction: ltr; }
    div[data-testid="stChatMessageContent"] { text-align: left; direction: ltr; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Gemini AI Assistant")

# 2. API Key Configuration
# Note: Ensure the API key is set in .streamlit/secrets.toml
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configuration Error: GOOGLE_API_KEY not found in Secrets.")
    st.stop()

# 3. Dynamic Model Selection
@st.cache_resource
def get_available_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if '1.5' in m.name:  # Prefers Gemini 1.5 Flash or Pro
                return m.name
    return 'gemini-pro'  # Fallback

model_name = get_available_model()
model = genai.GenerativeModel(model_name)

# 4. Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Message History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("Enter your message..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            output = response.text
            st.markdown(output)
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

