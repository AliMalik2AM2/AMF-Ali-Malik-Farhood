import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", layout="centered")

# تنسيق اللغة العربية
st.markdown("""
    <style>
    .stMarkdown { text-align: right; direction: rtl; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 علي مالك فرهود للذكاء الاصطناعي")

# 2. إعداد الـ API Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: مفتاح الـ API غير موجود في Secrets.")
    st.stop()

# 3. جلب الموديل (تم إصلاح استدعاء الموديل ليكون تفاعلياً)
@st.cache_resource
def setup_model():
    # تعليمات النظام لضمان التفاعل الذكي
    instruction = "أنت مساعد ذكي متطور في مشروع علي مالك فرهود للذكاء الاصطناعي. تفاعل مع المستخدم بذكاء وتذكر سياق الحديث."
    return genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

model = setup_model()

# 4. إدارة الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# بدء جلسة الشات إذا لم تكن موجودة (هذا الجزء الذي كان فيه الخطأ)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الشات والتفاعل
if prompt := st.chat_input("تحدث مع ذكاء علي مالك..."):
    # إضافة رسالة المستخدم للواجهة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من خلال جلسة الشات المستمرة
    with st.chat_message("assistant"):
        try:
            # استخدام الجلسة لضمان التفاعل (تذكر ما قبله)
            response = st.session_state.chat_session.send_message(prompt)
            output = response.text
            
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {str(e)}")

# إضافة زر لمسح المحادثة في الشريط الجانبي
if st.sidebar.button("مسح المحادثة والبدء من جديد"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
