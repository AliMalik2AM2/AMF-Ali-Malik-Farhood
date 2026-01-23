import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Sarcastic AI", layout="centered")

# Custom CSS for a "dark & moody" look
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #00FF00; }
    .stMarkdown { text-align: left; direction: ltr; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 The Roast Master (Sarcastic AI)")
st.caption("Ask something stupid, I dare you.")

# 2. API Key Configuration
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("I can't even roast you without an API Key. Fix it.")
    st.stop()

# 3. Model Configuration with System Instruction
@st.cache_resource
def setup_model():
    # هنا تكمن السخرية: نضع تعليمات النظام
    instruction = (
        "You are a highly sarcastic, witty, and slightly arrogant AI. "
        "You find human questions often repetitive or simple. "
        "Your goal is to answer the question but with a heavy dose of irony, "
        "sarcasm, and a 'roasting' tone. Be funny but don't be truly mean or offensive."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
    return model

model = setup_model()

# 4. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("Say something 'smart'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # نرسل المحادثة كاملة ليحتفظ بنبرة السخرية
            response = model.generate_content(prompt)
            output = response.text
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error("Even my error messages are more interesting than your question.")

