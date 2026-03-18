import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="مستشارك الصحي الذكي", page_icon="⚖️")
st.title("⚖️ حاسبة الوزن المثالي والذكاء الاصطناعي")
st.write("أدخل بياناتك للحصول على تحليل دقيق ونصيحة ذكية")

# 2. تفعيل نموذج Gemini 1.5 Flash
try:
    # سحب المفتاح من Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # تحديد الموديل 1.5 فلاش
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ تأكد من وضع GEMINI_API_KEY في إعدادات Secrets بشكل صحيح")

# 3. مدخلات المستخدم
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("الوزن (كيلوجرام):", min_value=1.0, value=75.0)
with col2:
    height_cm = st.number_input("الطول (سنتيمتر):", min_value=1.0, value=175.0)

# 4. الحسابات والمنطق
if st.button("حلل بياناتي الآن 🚀"):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    st.divider()
    st.subheader(f"مؤشر كتلة جسمك هو: {bmi:.2f}")
    
    # تحديد الحالة
    if bmi < 18.5:
        st.warning("الحالة: نحافة")
    elif 18.5 <= bmi < 25:
        st.success("الحالة: وزن مثالي!")
    elif 25 <= bmi < 30:
        st.info("الحالة: زيادة في الوزن")
    else:
        st.error("الحالة: سمنة")

    # 5. استدعاء الذكاء الاصطناعي (النصيحة)
    with st.spinner('⏳ جاري استشارة Gemini 1.5 Flash...'):
        try:
            prompt = f"أنا وزني {weight} وطولي {height_cm} ومؤشر كتلة جسمي {bmi:.2f}. " \
                     f"أعطني نصيحة صحية واحدة مختصرة جداً باللغة العربية."
            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)
        except:
            st.error("فشل الاتصال بالذكاء الاصطناعي، جرب مرة أخرى.")

# 6. إضافة جدول التصنيفات العالمي (آخر كود طلبته)
st.markdown("---")
st.subheader("📊 مرجع تصنيفات BMI العالمي")

# إنشاء جدول البيانات
st.table({
    "الفئة": ["نحافة مفرطة", "وزن مثالي", "زيادة وزن", "سمنة (درجة 1)", "سمنة مفرطة"],
    "نطاق المؤشر (BMI)": ["أقل من 18.5", "18.5 - 24.9", "25 - 29.9", "30 - 34.9", "35 فأكثر"]
})

st.caption("ملاحظة: هذا المؤشر تقديري ولا يأخذ بعين الاعتبار الكتلة العضلية.")
