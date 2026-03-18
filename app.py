import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="مستشارك الصحي الذكي", page_icon="🏃‍♂️")

# 2. تفعيل الذكاء الاصطناعي (Gemini)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدمنا فلاش لأنه أسرع بكثير في الرد
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ خطأ في إعدادات المفتاح السري (Secrets)")

st.title("⚖️ حاسبة الوزن المثالي الذكية")
st.markdown("---")

# 3. إدخال البيانات في أعمدة
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("الوزن (كيلوجرام):", min_value=10.0, value=75.0, step=0.1)
with col2:
    height_cm = st.number_input("الطول (سنتيمتر):", min_value=50.0, value=175.0, step=1.0)

# 4. زر التنفيذ والحساب
if st.button("حلل بياناتي الآن 🚀"):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.divider()
    st.subheader(f"مؤشر كتلة جسمك (BMI) هو: {bmi:.2f}")

    # تحديد الحالة بالألوان
    if bmi < 18.5:
        st.warning("الحالة: نحافة")
    elif 18.5 <= bmi < 25:
        st.success("الحالة: وزن مثالي! حافظ على نمط حياتك.")
    elif 25 <= bmi < 30:
        st.info("الحالة: زيادة في الوزن")
    else:
        st.error("الحالة: سمنة")

    # 5. استشارة الذكاء الاصطناعي
    with st.spinner('⏳ جاري طلب نصيحة مخصصة من Gemini...'):
        try:
            prompt = f"أنا شخص وزني {weight} كجم وطولي {height_cm} سم ومؤشر كتلة جسمي {bmi:.2f}. أعطني نصيحة صحية واحدة " \
                     f"مختصرة جداً ومحفزة باللغة العربية."
            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)
        except:
            st.error("تعذر الاتصال بالذكاء الاصطناعي حالياً.")

# 6. إضافة جدول المراجع في الأسفل بشكل جميل
st.markdown("---")
st.subheader("📊 مرجع تصنيفات الوزن العالمي")
st.table({
    "التصنيف": ["نحافة", "وزن مثالي", "زيادة وزن", "سمنة مفرطة"],
    "مؤشر الـ BMI": ["أقل من 18.5", "18.5 - 24.9", "25 - 29.9", "30 فأكثر"]
})
