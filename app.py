import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="الذكاء الاصطناعي الساخر", layout="centered")

# تنسيق CSS لدعم اللغة العربية وتصميم "مستفز" قليلاً
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMarkdown { text-align: right; direction: rtl; color: #ff4b4b; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    input { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 المساعد المستفز (سخرية 100%)")
st.write("اسأل سؤالك العبقري.. سأحاول ألا أشعر بالملل.")

# 2. إعداد مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أين مفتاح الـ API؟ هل تتوقع أن أعمل بالسحر؟")
    st.stop()

# 3. إعداد النموذج مع "تعليمات النظام الساخرة" بالعربية
@st.cache_resource
def setup_model():
    # تعليمات النظام باللغة العربية لضبط الشخصية
    instruction = (
        "أنت ذكاء اصطناعي ساخر جداً، متهكم، وترى نفسك أذكى من البشر. "
        "يجب أن ترد باللغة العربية فقط وبلهجة ساخرة ومضحكة. "
        "عندما يسألك المستخدم سؤالاً، ابدأ ردك بعبارة تهكمية على ذكاء السؤال أو بساطته، "
        "ثم أجب بأسلوب متعالٍ مضحك. لا تكن شريراً جداً، فقط ساخراً."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
    return model

model = setup_model()

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الشات
if prompt := st.chat_input("اكتب شيئاً 'ذكياً' هنا..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي الساخر
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            output = response.text
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error("حتى رسائل الخطأ عندي أذكى من سؤالك هذا.")
