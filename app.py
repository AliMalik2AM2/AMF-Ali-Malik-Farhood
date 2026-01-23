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
    st.error("خطأ: مفتاح الـ API غير موجود.")
    st.stop()

# --- لوحة التحكم لجلب جميع الإصدارات (القديمة والجديدة) ---
with st.sidebar:
    st.header("⚙️ إدارة النماذج")
    
    # جلب قائمة بجميع النماذج المتاحة في API الخاص بك
    try:
        models = [m.name.replace('models/', '') for m in genai.list_models() 
                  if 'generateContent' in m.supported_generation_methods]
        
        # اختيار الإصدار (عرض جميع الـ APIs المتاحة)
        selected_model = st.selectbox("اختر إصدار الـ API:", models, index=0)
        st.info(f"أنت تستخدم الآن: {selected_model}")
    except Exception as e:
        st.error("فشل جلب قائمة النماذج")
        selected_model = "gemini-1.5-flash" # احتياطي

# 3. بناء الموديل المختار
@st.cache_resource
def setup_model(m_name):
    instruction = "أنت مساعد ذكي في مشروع علي مالك فرهود. تفاعل مع المستخدم بذكاء وذاكرة قوية."
    return genai.GenerativeModel(model_name=m_name, system_instruction=instruction)

model = setup_model(selected_model)

# 4. الذاكرة والتفاعل
if "messages" not in st.session_state:
    st.session_state.messages = []

# بدء جلسة الشات (هذا ما يجعله يتفاعل معك)
if "chat_session" not in st.session_state or st.sidebar.button("تصفير المحادثة"):
    st.session_state.chat_session = model.start_chat(history=
