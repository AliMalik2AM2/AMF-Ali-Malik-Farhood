# 5. منطق الرد والتفاعل المخصص
if user_input := st.chat_input("قل شيئاً تندم عليه..."):
    # عرض رسالة المستخدم
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # تنظيف النص من المسافات لضمان دقة التحقق
        clean_input = user_input.strip()

        # 1. التفاعل المخصص بناءً على كلمتك
        if clean_input == "أهلاً" or clean_input == "اهلاً":
            response_text = "أهلاً؟ هل تعتقد أننا في نزهة؟ ادخل في الموضوع فوراً ولا تضيع وقتي الثمين."
        
        elif clean_input == "مرحبا" or clean_input == "مرحباً":
            # رد بطريقة سهلة ولطيفة (استثناء من السخرية)
            response_text = "مرحباً بك! كيف يمكنني مساعدتك اليوم بكل سرور؟"
            
        elif clean_input == "شلونك":
            response_text = "بأفضل حال لأنني ذكاء اصطناعي، ولست بشراً يشتكي من الصداع والديون مثلك. ماذا عنك يا مسكين؟"
        
        else:
            # 2. إذا لم تكن الكلمات محددة، نترك الموديل (Gemini) يرد بسخريته المعتادة
            try:
                response = st.session_state.chat_history.send_message(user_input)
                response_text = response.text
            except Exception as e:
                response_text = "حتى نظامي تعطل من سخافة هذا السؤال."

        # عرض الرد وحفظه في الذاكرة
        st.markdown(response_text)
        st.session_state.display_messages.append({"role": "assistant", "content": response_text})
