import streamlit as st
import google.generativeai as genai

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="AI Health Advisor", page_icon="⚖️")
st.title("⚖️ AI BMI Calculator")
st.write("Professional health analysis powered by Gemini 1.5 Flash.")

# 2. ربط المفتاح السري (Secrets) وتجهيز الموديل
try:
    # جلب المفتاح من الإعدادات
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # تعريف الموديل السريع
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Key Error: Please check your Streamlit Secrets.")
    model = None

# 3. إدخال البيانات
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg):", min_value=1.0, value=75.0)
with col2:
    height_cm = st.number_input("Height (cm):", min_value=1.0, value=175.0)

# 4. زر الحساب والتحليل
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

    # 5. استدعاء الذكاء الاصطناعي (Gemini)
    if model:
        with st.spinner('Consulting Gemini AI...'):
            try:
                prompt = f"BMI is {bmi:.2f} ({status}). Give me one very short, professional health tip in English."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.success("💡 AI Advice:")
                st.write(response.text)
            except Exception as ai_err:
                st.error("AI service is currently busy. Please try again.")

# 6. جدول المراجع (Reference Table)
st.markdown("---")
st.table({
    "Category": ["Underweight", "Healthy Weight", "Overweight", "Obese"],
    "BMI Range": ["Below 18.5", "18.5 – 24.9", "25.0 – 29.9", "Above 30"]
})
