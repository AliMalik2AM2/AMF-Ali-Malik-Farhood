import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة باسمك
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", layout="centered")

# تنسيق اللغة العربية (RTL)
st.markdown("""
    <style>
    .stMarkdown { text-align: right; direction: rtl; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 علي مالك فرهود للذكاء الاصطناعي")

# 2. إعداد مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: مفتاح الـ API غير موجود في إعدادات Secrets.")
    st.stop()

# 3. دالة ذكية تجلب أحدث وأفضل موديل متاح تلقائياً (تغطية كل الإصدارات)
@st.cache_resource
def get_best_available_model():
    try:
        # جلب قائمة بكل الموديلات المتاحة في حسابك (القديمة والجديدة)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # اختيار الأفضل بالترتيب: 1.5 Pro ثم 1.5 Flash ثم 1.0 Pro
        target_models = ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']
        
        for target in target_models:
            if target in available_models:
                # وضع تعليمات النظام ليكون تفاعلياً
                instruction = "أنت مساعد ذكي في مشروع علي مالك فرهود للذكاء الاصطناعي. تفاعل مع المستخدم بذكاء وتذكر سياق الكلام."
                return genai.GenerativeModel(model_name=target, system_instruction=instruction)
        
        # إذا لم يجد شيئاً محدداً، يأخذ أول موديل متاح
        return genai.GenerativeModel(model_name=available_models[0])
    except Exception as e:
        st.error(f"فشل جلب الموديلات: {e}")
        return genai.GenerativeModel(model_name='gemini-1.5-flash')

model = get_best_available_model()

# 4. إدارة الذاكرة والتفاعل (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# بدء جلسة شات تفاعلية مستمرة (تتذكر كل شيء)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض الرسائل السابقة في الواجهة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الشات (إرسال واستقبال وتفاعل)
if prompt := st.chat_input("تحدث مع ذكاء علي مالك..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد تفاعلي
    with st.chat_message("assistant"):
        try:
            # استخدام send_message لضمان التفاعل مع الكلام السابق
            response = st.session_state.chat_session.send_message(prompt)
            output = response.text
            
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error(f"حدث خطأ في النظام: {str(e)}")

# زر جانبي لمسح الذاكرة
if st.sidebar.button("تصفير المحادثة"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
