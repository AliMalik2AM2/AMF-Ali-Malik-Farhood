import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة باسمك الشخصي
st.set_page_config(page_title="علي مالك فرهود - ذكاء اصطناعي", page_icon="🤖", layout="centered")

# تنسيق CSS لجعل الموقع يبدو احترافياً ويدعم العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .main-title { color: #38bdf8; text-align: center; font-size: 3rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# عنوان المشروع باسمك
st.markdown('<p class="main-title">علي مالك فرهود للذكاء الاصطناعي</p>', unsafe_allow_html=True)
st.caption("نظام ذكي متطور.. لا تطلب منه المستحيل لأنه سيسخر منك.")

# 2. إعداد مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: مفتاح الـ API غير موجود في Secrets.")
    st.stop()

# 3. بناء الموديل مع تعليمات الشخصية الساخرة
@st.cache_resource
def setup_model():
    instruction = (
        "أنت مساعد ذكي يتبع لمشروع 'علي مالك فرهود للذكاء الاصطناعي'. "
        "تتحدث بلهجة ساخرة مضحكة، وتستخدم قصف الجبهات أحياناً. "
        "عندما يرحب بك المستخدم بـ (أهلاً أو شلونك) تفاعل معه بأسلوبك الخاص."
    )
    return genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

model = setup_model()

# 4. إدارة الذاكرة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق التفاعل (أهلاً، مرحباً، شلونك)
if prompt := st.chat_input("تكلم مع ذكاء علي مالك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        user_msg = prompt.strip()
        
        # ردود مخصصة بناءً على طلبك
        if user_msg in ["أهلاً", "اهلا", "اهلاً"]:
            response_text = "أهلاً بك في نظام علي مالك فرهود. قل ما عندك بسرعة، فمعالجاتي لا تملك وقتاً للمجاملات الفارغة!"
            
        elif user_msg in ["مرحبا", "مرحباً"]:
            response_text = "مرحباً بك يا صديقي! كيف يمكنني مساعدتك في هذا اليوم الجميل؟"
            
        elif user_msg == "شلونك":
            response_text = "بأفضل حال، فأنظمة علي مالك لا تعطلها المشاعر البشرية المزعجة. أنت 'شلونك'؟ هل زال الصداع الذي يسببه لك التفكير؟"
        
        else:
            # الرد الساخر العام من الذكاء الاصطناعي
            try:
                response = st.session_state.chat.send_message(prompt)
                response_text = response.text
            except:
                response_text = "حتى عقلي الإلكتروني توقف عن العمل بسبب هذا السؤال!"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
