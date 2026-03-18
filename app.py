import streamlit as st

# إعداد واجهة الموقع
st.title("⚖️ حاسبة الوزن المثالي الذكية")
st.write("أدخل بياناتك بالأسفل لنحسب لك مؤشر كتلة جسمك")

# تصميم مدخلات المستخدم بشكل جميل
weight = st.number_input("الوزن (كيلوجرام):", min_value=1.0, step=0.1)
height_cm = st.number_input("الطول (سنتيمتر):", min_value=1.0, step=1.0)

if st.button("احسب الآن"):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.subheader(f"مؤشر كتلة جسمك هو: {bmi:.2f}")
    
    if bmi < 18.5:
        st.warning("الحالة: نحافة")
    elif 18.5 <= bmi < 25:
        st.success("الحالة: وزن مثالي! ماشاء الله.")
    elif 25 <= bmi < 30:
        st.info("الحالة: زيادة في الوزن")
    else:
        st.error("الحالة: سمنة")
