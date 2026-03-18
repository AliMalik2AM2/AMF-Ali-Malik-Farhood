import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والواجهة (Page Config)
st.set_page_config(page_title="AI Health Advisor", page_icon="⚖️")
st.title("⚖️ AI BMI Calculator")
st.write("Enter your details for a fast AI health analysis.")

# 2. ربط المفتاح السري وتحديد الموديل السريع (The Engine)
try:
    # جلب المفتاح من إعدادات Secrets في Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # تحديد موديل 1.5 فلاش لضمان السرعة القصوى
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Key is missing or invalid in Secrets!")

# 3. خانات إدخال البيانات (User Inputs)
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg):", min_value=1.0, value=75.0, step=0.1)
with col2:
    height_cm = st.number_input("Height (cm):", min_value=1.0, value=175.0, step=1.0)

# 4. زر الحساب واستدعاء الذكاء الاصطناعي
if st.button("Analyze My Data 🚀"):
    # حساب مؤشر كتلة الجسم
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.divider()
    st.subheader(f"Your BMI is: {bmi:.2f}")
    
    # تحديد الحالة الصحية بالألوان
    if bmi < 18.5:
        status, color = "Underweight", "orange"
        st.warning(f"Status: {status}")
    elif 18.5 <= bmi < 25:
        status, color = "Healthy Weight", "green"
        st.success(f"Status: {status}")
    elif 25 <= bmi < 30:
        status, color = "Overweight", "blue"
        st.info(f"Status: {status}")
    else:
        status, color = "Obese", "red"
        st.error(f"Status: {status}")

    # استشارة Gemini 1.5 Flash (سرعة البرق)
    with st.spinner('⏳ Consulting Gemini 1.5 Flash...'):
        try:
            # إرسال البيانات للموديل وطلب نصيحة قصيرة جداً
            prompt = f"I am {weight}kg and {height_cm}cm tall. BMI: {bmi:.2f} ({status}). Give me one professional 10-word health tip in English."
            response = model.generate_content(prompt)
            st.markdown("---")
            st.success("💡 AI Health Tip:")
            st.write(response.text)
        except Exception as e:
            st.error("AI is busy right now. Please try again.")

# 5. جدول المراجع العالمي (BMI Table)
st.markdown("---")
st.subheader("📊 Global BMI Categories")
st.table({
    "Category": ["Underweight", "Healthy Weight", "Overweight", "Obese"],
    "BMI Range": ["Below 18.5", "18.5 – 24.9", "25.0 – 29.9", "30.0 and above"]
})

st.caption("Note: This app is for informational purposes and uses Gemini 1.5 Flash.")
