import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="حاسبة الوزن الذكية", page_icon="⚖️")

# ربط المفتاح السري الذي وضعته في Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("تأكد من وضع المفتاح السري بشكل صحيح في إعدادات Streamlit")

st.title("⚖️ حاسبة الوزن المثالي بالذكاء الاصطناعي")
st.write("أدخل بياناتك لنقدم لك تحليلاً ذكياً")

# مدخلات المستخدم
weight = st.number_input("الوزن (كيلوجرام):", min_value=1.0, value=70.0)
height_cm = st.number_input("الطول (سنتيمتر):", min_value=1.0, value=170.0)

if st.button("احسب النتيجة واطلب نصيحة ذكية"):
    # حساب BMI
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.subheader(f"مؤشر كتلة جسمك هو: {bmi:.2f}")
    
    # تصنيف الحالة
    if bmi < 18.5: status = "نحافة"
    elif 18.5 <= bmi < 25: status = "وزن مثالي"
    elif 25 <= bmi < 30: status = "زيادة في الوزن"
    else: status = "سمنة"
    
    st.info(f"حالتك هي: {status}")

    # استشارة الذكاء الاصطناعي
    with st.spinner('جاري استشارة Gemini...'):
        prompt = f"أنا وزني {weight} كجم وطولي {height_cm} سم، وحالتي هي {status}. أعطني نصيحة صحية واحدة مختصرة باللغة العربية."
        response = model.generate_content(prompt)
        st.success("💡 نصيحة الذكاء الاصطناعي:")
        st.write(response.text)
