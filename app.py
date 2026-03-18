import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة (يجب أن تكون في البداية)
st.set_page_config(page_title="AI Health Advisor", page_icon="⚖️")

# 2. ربط الذكاء الاصطناعي وإصلاح خطأ الترتيب
try:
    # جلب المفتاح من الأسرار
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # تحديد الموديل السريع 1.5 Flash
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Missing API Key in Streamlit Secrets!")
    model = None

# 3. واجهة المستخدم (باللغة الإنجليزية كما طلبت)
st.title("⚖️ AI BMI Calculator")
st.write("Professional health analysis powered by Gemini 1.5 Flash.")

# تقسيم المدخلات في أعمدة
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg):", min_value=1.0, value=75.0, step=0.1)
with col2:
    height_cm = st.number_input("Height (cm):", min_value=1.0, value=175.0, step=1.0)

# 4. حسابات البرنامج
if st.button("Calculate & Get AI Advice 🚀"):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.divider()
    st.subheader(f"Your BMI: {bmi:.2f}")
    
    # تحديد الحالة الصحية
    if bmi < 18.5:
        status = "Underweight"
        st.warning(f"Category: {status}")
    elif 18.5 <= bmi < 25:
        status = "Healthy Weight"
        st.success(f"Category: {status}")
    elif 25 <= bmi < 30:
        status = "Overweight"
        st.info(f"Category: {status}")
    else:
        status = "Obese"
        st.error(f"Category: {status}")

    # 5. استشارة الذكاء الاصطناعي (بدون تأخير)
    if model:
        with st.spinner('Consulting AI...'):
            try:
                prompt = f"BMI is {bmi:.2f} ({status}). Give one professional 10-word health tip."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.success("💡 AI Professional Advice:")
                st.write(response.text)
            except:
                st.error("AI connection failed. Check
