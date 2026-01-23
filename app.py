import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
# تم تغيير الاسم هنا ليظهر في المتصفح
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stMarkdown { text-align: right; direction: rtl; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# تغيير العنوان الرئيسي للمشروع
st.title("🤖 علي مالك فرهود للذكاء الاصطناعي")

# 2. API Key Configuration
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configuration Error: GOOGLE_API_KEY not found in Secrets.")
    st.stop()

# 3. Dynamic Model Selection
@st.cache_resource
def get_available_model():
    # إضافة تعليمات النظام ليكون الروبوت تفاعلياً وذكياً
    instruction = "أنت مساعد ذكي متطور ضمن مشروع علي مالك فرهود للذكاء الاصطناعي. رد على المستخدم بذكاء وتفاعل معه بناءً على رسائله السابقة."
    return genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

model = get_available_model()

# 4. Session State for Chat History (هنا السر في التفاعل)
if "messages" not in st.session_state:
    st.session_state.messages = []

# إنشاء جلسة شات تحتفظ بالذاكرة
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display Message History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("تحدث مع ذكاء علي مالك..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        try:
            # استخدام chat_session بدلاً من generate_content يجعل الروبوت يتفاعل ويتذكر
            response = st.session_state.chat_session.send_message(prompt)
            output = response.text
            st.markdown(output)
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
