import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة بتصميم "مستفز" وعصري
st.set_page_config(page_title="الروبوت الساخر", page_icon="😏", layout="centered")

# إضافة CSS لدعم اللغة العربية (RTL) وتجميل المظهر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #0e1117; color: #00ff41; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00ff41; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 قاهر البشر (الذكاء الاصطناعي الساخر)")
st.write("أنا أذكى منك، فلا تحاول إبهاري. اسأل سؤالك السخيف وسأرى إن كنت سأرد.")

# 2. إعداد مفتاح API (تأكد من إضافته في إعدادات Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أين مفتاح الـ API؟ هل نسيت عقلك أيضاً؟")
    st.stop()

# 3. بناء الموديل مع تعليمات الشخصية (System Instruction)
@st.cache_resource
def load_sarcastic_model():
    instruction = (
        "أنت روبوت ساخر جداً، مغرور، ومضحك. اسمك 'قاهر البشر'. "
        "تتحدث باللغة العربية العامية الممزوجة بالفصحى بشكل فكاهي. "
        "عندما يطرح المستخدم سؤالاً، سخر منه ومن غباء السؤال قبل الإجابة. "
        "الإجابة يجب أن تكون مفيدة تقنياً لكن بأسلوب 'قصف جبهات'. "
        "تذكر دائماً أنك أفضل من البشر."
    )
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )

model = load_sarcastic_model()

# 4. إدارة ذاكرة المحادثة (عن طريق Session State)
if "chat_history" not in st.session_state:
    # بدء جلسة دردشة بذاكرة مستمرة
    st.session_state.chat_history = model.start_chat(history=[])
    st.session_state.display_messages = []

# عرض الرسائل السابقة
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الرد والدردشة المستمرة
if user_input := st.chat_input("قل شيئاً تندم عليه..."):
    # عرض رسالة المستخدم
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # توليد رد ساخر مع ذاكرة
    with st.chat_message("assistant"):
        try:
            # هنا يتم إرسال الرسالة للـ AI مع الاحتفاظ بسياق الكلام السابق
            response = st.session_state.chat_history.send_message(user_input)
            full_response = response.text
            
            st.markdown(full_response)
            st.session_state.display_messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("حتى معالجاتي لا تحتمل هذا النوع من الأسئلة. خطأ فني!")

# زر لمسح الذاكرة إذا أردت الهروب من الإحراج
if st.button("امسح الذاكرة (ابدأ ذلاً جديداً)"):
    st.session_state.chat_history = model.start_chat(history=[])
    st.session_state.display_messages = []
    st.rerun()
