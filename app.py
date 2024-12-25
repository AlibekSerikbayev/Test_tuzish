import streamlit as st
from fpdf import FPDF

# Test shablonini yuklash funksiyasi
def load_test_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    questions = []
    question_blocks = content.strip().split("%%%%")
    for block in question_blocks:
        if block.strip():
            parts = block.strip().split("++++")
            question_text = parts[0].replace("****[1]\n", "").strip()
            options = [part.strip() for part in parts[1:]]
            correct_answer = options[0]  # To'g'ri javob doim birinchi bo'ladi
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer
            })
    return questions

# Savollarni bo‘limlarga ajratish
def split_questions(questions, chunk_size=25):
    return [questions[i:i + chunk_size] for i in range(0, len(questions), chunk_size)]

# Natijalarni hisoblash funksiyasi
def calculate_score(questions, user_answers):
    correct_count = 0
    for i, question in enumerate(questions):
        if question["correct_answer"] == user_answers.get(i):
            correct_count += 1
    return correct_count

# Unicode shrift qo‘llab-quvvatlovchi PDF hisobotni yaratish funksiyasi
def generate_pdf_report(questions, user_answers, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("ArialUnicode", "", "ARIAL.TTF", uni=True)  # Unicode shrift
    pdf.set_font("ArialUnicode", size=12)
    pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
    pdf.ln(10)

    for i, question in enumerate(questions):
        pdf.set_font("ArialUnicode", size=10)
        pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
        pdf.multi_cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}")
        user_answer = user_answers.get(i, "Javob berilmagan")
        pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answer}")
        pdf.ln(5)

    pdf.set_font("ArialUnicode", size=12)
    pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
    return pdf

# Streamlit interfeysi
def main():
    st.title("Streamlit Test Tizimi")
    st.write("Quyidagi testga javob bering:")

    # Test faylini yuklash
    test_file = "test_template.txt"  # Test fayli nomi
    questions = load_test_from_file(test_file)
    
    # Savollarni bo‘limlarga ajratish
    chunks = split_questions(questions, chunk_size=25)
    chunk_titles = [f"Savollar {i * 25 + 1}-{(i + 1) * 25}" for i in range(len(chunks))]
    
    # Bo‘limni tanlash uchun selectbox
    selected_chunk_index = st.selectbox("Savollar bo‘limini tanlang:", options=range(len(chunks)), format_func=lambda x: chunk_titles[x])
    selected_questions = chunks[selected_chunk_index]

    # Javoblarni saqlash
    user_answers = {}

    # Radiobuttonlarni alohida panelda ko'rsatish
    with st.form("Test Form"):  # Form ichida radiobuttonlar
        for i, question in enumerate(selected_questions):
            st.subheader(f"{i + 1}. {question['question']}")
            user_answers[i] = st.radio(
                label=f"Savol {i + 1}",
                options=["Tanlanmagan"] + question["options"],
                index=0,  # Initially "Tanlanmagan" option is selected
                key=f"q{selected_chunk_index}_{i}"
            )
        submitted = st.form_submit_button("Testni yakunlash")

    # Javoblarni topshirish
    if submitted:
        final_answers = {i: ans for i, ans in user_answers.items() if ans != "Tanlanmagan"}
        score = calculate_score(selected_questions, final_answers)
        st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(selected_questions)}")
        st.write("Natijalar:")
        for i, question in enumerate(selected_questions):
            st.write(f"**{i + 1}. {question['question']}**")
            st.write(f"To'g'ri javob: {question['correct_answer']}")
            user_answer = final_answers.get(i, "Javob berilmagan")
            st.write(f"Sizning javobingiz: {user_answer}")

        # PDF hisobotni yaratish
        pdf = generate_pdf_report(selected_questions, final_answers, score)
        pdf_file_path = "test_results.pdf"
        pdf.output(pdf_file_path)
        
        # PDF-ni yuklab olish havolasi
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()



# import streamlit as st
# import random
# from fpdf import FPDF

# # Test shablonini yuklash funksiyasi
# def load_test_from_file(file_path):
#     with open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()
    
#     questions = []
#     question_blocks = content.strip().split("%%%%")
#     for block in question_blocks:
#         if block.strip():
#             parts = block.strip().split("++++")
#             question_text = parts[0].replace("****[1]\n", "").strip()
#             options = [part.strip() for part in parts[1:]]
#             correct_answer = options[0]  # To'g'ri javob doim birinchi bo'ladi
#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "correct_answer": correct_answer
#             })
#     return questions

# # Savollarni bo‘limlarga ajratish
# def split_questions(questions, chunk_size=25):
#     return [questions[i:i + chunk_size] for i in range(0, len(questions), chunk_size)]

# # Natijalarni hisoblash funksiyasi
# def calculate_score(questions, user_answers):
#     correct_count = 0
#     for i, question in enumerate(questions):
#         if question["correct_answer"] == user_answers[i]:
#             correct_count += 1
#     return correct_count

# # Unicode shrift qo‘llab-quvvatlovchi PDF hisobotni yaratish funksiyasi
# def generate_pdf_report(questions, user_answers, score):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.add_font("ArialUnicode", "", "ARIAL.TTF", uni=True)  # Unicode shrift
#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
#     pdf.ln(10)

#     for i, question in enumerate(questions):
#         pdf.set_font("ArialUnicode", size=10)
#         pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
#         pdf.multi_cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}")
#         pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}")
#         pdf.ln(5)

#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
#     return pdf

# # Streamlit interfeysi
# def main():
#     st.title("Streamlit Test Tizimi")
#     st.write("Quyidagi testga javob bering:")

#     # Test faylini yuklash
#     test_file = "test_template.txt"  # Test fayli nomi
#     questions = load_test_from_file(test_file)
    
#     # Savollarni bo‘limlarga ajratish
#     chunks = split_questions(questions, chunk_size=25)
#     chunk_titles = [f"Savollar {i * 25 + 1}-{(i + 1) * 25}" for i in range(len(chunks))]
    
#     # Bo‘limni tanlash uchun selectbox
#     selected_chunk_index = st.selectbox("Savollar bo‘limini tanlang:", options=range(len(chunks)), format_func=lambda x: chunk_titles[x])
#     selected_questions = chunks[selected_chunk_index]

#     # Javoblarni saqlash
#     user_answers = []

#     # Har bir savolni chiqarish
#     for i, question in enumerate(selected_questions):
#         st.subheader(f"{i + 1}. {question['question']}")
#         user_answer = st.radio(
#             "Javobingizni tanlang:",
#             question["options"],
#             key=f"q{selected_chunk_index}_{i}"  # Unique key for each question
#         )
#         user_answers.append(user_answer)

#     # Javoblarni topshirish
#     if st.button("Testni yakunlash"):
#         score = calculate_score(selected_questions, user_answers)
#         st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(selected_questions)}")
#         st.write("Natijalar:")
#         for i, question in enumerate(selected_questions):
#             st.write(f"**{i + 1}. {question['question']}**")
#             st.write(f"To'g'ri javob: {question['correct_answer']}")
#             st.write(f"Sizning javobingiz: {user_answers[i]}")

#         # PDF hisobotni yaratish
#         pdf = generate_pdf_report(selected_questions, user_answers, score)
#         pdf_file_path = "test_results.pdf"
#         pdf.output(pdf_file_path)
        
#         # PDF-ni yuklab olish havolasi
#         with open(pdf_file_path, "rb") as pdf_file:
#             pdf_data = pdf_file.read()
#         st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")

# if __name__ == "__main__":
#     main()




# # file: streamlit_test_app.py
# import streamlit as st
# import random
# from fpdf import FPDF

# # Test shablonini yuklash funksiyasi
# def load_test_from_file(file_path):
#     with open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()
    
#     questions = []
#     question_blocks = content.strip().split("%%%%")
#     for block in question_blocks:
#         if block.strip():
#             parts = block.strip().split("++++")
#             question_text = parts[0].replace("****[1]\n", "").strip()
#             options = [part.strip() for part in parts[1:]]
#             correct_answer = options[0]  # To'g'ri javob doim birinchi bo'ladi
#             random.shuffle(options)  # Javoblarni chalkashtirish
#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "correct_answer": correct_answer
#             })
#     return questions

# # Natijalarni hisoblash funksiyasi
# def calculate_score(questions, user_answers):
#     correct_count = 0
#     for i, question in enumerate(questions):
#         if question["correct_answer"] == user_answers[i]:
#             correct_count += 1
#     return correct_count

# # Unicode shrift qo‘llab-quvvatlovchi PDF hisobotni yaratish funksiyasi
# def generate_pdf_report(questions, user_answers, score):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.add_font("ArialUnicode", "", "ARIAL.TTF", uni=True)  # Unicode shrift
#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
#     pdf.ln(10)

#     for i, question in enumerate(questions):
#         pdf.set_font("ArialUnicode", size=10)
#         pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
#         pdf.multi_cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}")
#         pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}")
#         pdf.ln(5)

#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
#     return pdf

# # Streamlit interfeysi
# def main():
#     st.title("Streamlit Test Tizimi")
#     st.write("Savollarni birma-bir ko'ring va javob bering:")

#     # Test faylini yuklash
#     test_file = "test_template.txt"  # Test fayli nomi

#     # Aralashtirilgan savollarni session_state'da saqlash
#     if "shuffled_questions" not in st.session_state:
#         questions = load_test_from_file(test_file)
#         random.shuffle(questions)  # Savollarni aralashtirish
#         st.session_state.shuffled_questions = questions
#     else:
#         questions = st.session_state.shuffled_questions

#     # Session state uchun indeks va javoblar
#     if "current_index" not in st.session_state:
#         st.session_state.current_index = 0
#     if "user_answers" not in st.session_state:
#         st.session_state.user_answers = [None] * len(questions)

#     # Hozirgi savolni olish
#     current_index = st.session_state.current_index
#     current_question = questions[current_index]

#     # Savolni ko'rsatish
#     st.subheader(f"Savol {current_index + 1}/{len(questions)}")
#     st.write(current_question["question"])
#     user_answer = st.radio(
#         "Javobingizni tanlang:",
#         current_question["options"],
#         key=f"q{current_index}",
#         index=current_question["options"].index(st.session_state.user_answers[current_index]) if st.session_state.user_answers[current_index] else None
#     )
#     st.session_state.user_answers[current_index] = user_answer

#     # Oldinga va orqaga tugmalar
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         if st.button("⬅️ Oldingi savol", disabled=current_index == 0):
#             st.session_state.current_index -= 1
#     with col3:
#         if st.button("Keyingi savol ➡️", disabled=current_index == len(questions) - 1):
#             st.session_state.current_index += 1

#     # Testni yakunlash
#     if st.button("Testni yakunlash"):
#         score = calculate_score(questions, st.session_state.user_answers)
#         st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(questions)}")
#         st.write("Natijalar:")
#         for i, question in enumerate(questions):
#             st.write(f"**{i + 1}. {question['question']}**")
#             st.write(f"To'g'ri javob: {question['correct_answer']}")
#             st.write(f"Sizning javobingiz: {st.session_state.user_answers[i]}")

#         # PDF hisobotni yaratish
#         pdf = generate_pdf_report(questions, st.session_state.user_answers, score)
#         pdf_file_path = "test_results.pdf"
#         pdf.output(pdf_file_path)
        
#         # PDF-ni yuklab olish havolasi
#         with open(pdf_file_path, "rb") as pdf_file:
#             pdf_data = pdf_file.read()
#         st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")

# if __name__ == "__main__":
#     main()




# # file: streamlit_test_app.py
# import streamlit as st
# import random
# from fpdf import FPDF

# # Test shablonini yuklash funksiyasi
# def load_test_from_file(file_path):
#     with open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()
    
#     questions = []
#     question_blocks = content.strip().split("%%%%")
#     for block in question_blocks:
#         if block.strip():
#             parts = block.strip().split("++++")
#             question_text = parts[0].replace("****[1]\n", "").strip()
#             options = [part.strip() for part in parts[1:]]
#             correct_answer = options[0]  # To'g'ri javob doim birinchi bo'ladi
#             random.shuffle(options)  # Javoblarni chalkashtirish
#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "correct_answer": correct_answer
#             })
#     return questions


# # Natijalarni hisoblash funksiyasi
# def calculate_score(questions, user_answers):
#     correct_count = 0
#     for i, question in enumerate(questions):
#         if question["correct_answer"] == user_answers[i]:
#             correct_count += 1
#     return correct_count


# # Unicode shrift qo‘llab-quvvatlovchi PDF hisobotni yaratish funksiyasi
# def generate_pdf_report(questions, user_answers, score):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.add_font("ArialUnicode", "", "ARIAL.TTF", uni=True)  # Unicode shrift
#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
#     pdf.ln(10)

#     for i, question in enumerate(questions):
#         pdf.set_font("ArialUnicode", size=10)
#         pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
#         pdf.multi_cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}")
#         pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}")
#         pdf.ln(5)

#     pdf.set_font("ArialUnicode", size=12)
#     pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
#     return pdf


# # Streamlit interfeysi
# def main():
#     st.title("Streamlit Test Tizimi")
#     st.write("Savollarni birma-bir ko'ring va javob bering:")

#     # Test faylini yuklash
#     test_file = "test_template.txt"  # Test fayli nomi
#     questions = load_test_from_file(test_file)
    
#     # Session state uchun indeks va javoblar
#     if "current_index" not in st.session_state:
#         st.session_state.current_index = 0
#     if "user_answers" not in st.session_state:
#         st.session_state.user_answers = [None] * len(questions)

#     # Hozirgi savolni olish
#     current_index = st.session_state.current_index
#     current_question = questions[current_index]

#     # Savolni ko'rsatish
#     st.subheader(f"Savol {current_index + 1}/{len(questions)}")
#     st.write(current_question["question"])
#     user_answer = st.radio(
#         "Javobingizni tanlang:",
#         current_question["options"],
#         key=f"q{current_index}",
#         index=current_question["options"].index(st.session_state.user_answers[current_index]) if st.session_state.user_answers[current_index] else None
#     )
#     st.session_state.user_answers[current_index] = user_answer

#     # Oldinga va orqaga tugmalar
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         if st.button("⬅️ Oldingi savol", disabled=current_index == 0):
#             st.session_state.current_index -= 1
#     with col3:
#         if st.button("Keyingi savol ➡️", disabled=current_index == len(questions) - 1):
#             st.session_state.current_index += 1

#     # Testni yakunlash
#     if st.button("Testni yakunlash"):
#         score = calculate_score(questions, st.session_state.user_answers)
#         st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(questions)}")
#         st.write("Natijalar:")
#         for i, question in enumerate(questions):
#             st.write(f"**{i + 1}. {question['question']}**")
#             st.write(f"To'g'ri javob: {question['correct_answer']}")
#             st.write(f"Sizning javobingiz: {st.session_state.user_answers[i]}")

#         # PDF hisobotni yaratish
#         pdf = generate_pdf_report(questions, st.session_state.user_answers, score)
#         pdf_file_path = "test_results.pdf"
#         pdf.output(pdf_file_path)
        
#         # PDF-ni yuklab olish havolasi
#         with open(pdf_file_path, "rb") as pdf_file:
#             pdf_data = pdf_file.read()
#         st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")


# if __name__ == "__main__":
#     main()


# # # # file: streamlit_test_app.py
# # import streamlit as st
# # import random
# # from fpdf import FPDF


# # # Test shablonini yuklash funksiyasi
# # def load_test_from_file(file_path):
# #     with open(file_path, "r", encoding="utf-8") as file:
# #         content = file.read()
    
# #     questions = []
# #     question_blocks = content.strip().split("%%%%")
# #     for block in question_blocks:
# #         if block.strip():
# #             parts = block.strip().split("++++")
# #             question_text = parts[0].replace("****[1]\n", "").strip()
# #             options = [part.strip() for part in parts[1:]]
# #             correct_answer = options[0]  # To'g'ri javob doim birinchi bo'ladi
# #             random.shuffle(options)  # Javoblarni chalkashtirish
# #             questions.append({
# #                 "question": question_text,
# #                 "options": options,
# #                 "correct_answer": correct_answer
# #             })
# #     return questions


# # # Savollarni bo‘limlarga ajratish
# # def split_questions(questions, chunk_size=25):
# #     return [questions[i:i + chunk_size] for i in range(0, len(questions), chunk_size)]


# # # Natijalarni hisoblash funksiyasi
# # def calculate_score(questions, user_answers):
# #     correct_count = 0
# #     for i, question in enumerate(questions):
# #         if question["correct_answer"] == user_answers[i]:
# #             correct_count += 1
# #     return correct_count


# # # Unicode shrift qo‘llab-quvvatlovchi PDF hisobotni yaratish funksiyasi
# # def generate_pdf_report(questions, user_answers, score):
# #     pdf = FPDF()
# #     pdf.add_page()
# #     pdf.add_font("ArialUnicode", "", "ARIAL.TTF", uni=True)  # Unicode shrift
# #     pdf.set_font("ArialUnicode", size=12)
# #     pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
# #     pdf.ln(10)

# #     for i, question in enumerate(questions):
# #         pdf.set_font("ArialUnicode", size=10)
# #         pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
# #         pdf.multi_cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}")
# #         pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}")
# #         pdf.ln(5)

# #     pdf.set_font("ArialUnicode", size=12)
# #     pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
# #     return pdf


# # # Streamlit interfeysi
# # def main():
# #     st.title("Streamlit Test Tizimi")
# #     st.write("Quyidagi testga javob bering:")

# #     # Test faylini yuklash
# #     test_file = "test_template.txt"  # Test fayli nomi
# #     questions = load_test_from_file(test_file)
    
# #     # Savollarni bo‘limlarga ajratish
# #     chunks = split_questions(questions, chunk_size=25)
# #     chunk_titles = [f"Savollar {i * 25 + 1}-{(i + 1) * 25}" for i in range(len(chunks))]
    
# #     # Bo‘limni tanlash uchun selectbox
# #     selected_chunk_index = st.selectbox("Savollar bo‘limini tanlang:", options=range(len(chunks)), format_func=lambda x: chunk_titles[x])
# #     selected_questions = chunks[selected_chunk_index]

# #     # Javoblarni saqlash
# #     user_answers = []

# #     # Har bir savolni chiqarish
# #     for i, question in enumerate(selected_questions):
# #         st.subheader(f"{i + 1}. {question['question']}")
# #         user_answer = st.radio(
# #             "Javobingizni tanlang:",
# #             question["options"],
# #             key=f"q{selected_chunk_index}_{i}"  # Unique key for each question
# #         )
# #         user_answers.append(user_answer)

# #     # Javoblarni topshirish
# #     if st.button("Testni yakunlash"):
# #         score = calculate_score(selected_questions, user_answers)
# #         st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(selected_questions)}")
# #         st.write("Natijalar:")
# #         for i, question in enumerate(selected_questions):
# #             st.write(f"**{i + 1}. {question['question']}**")
# #             st.write(f"To'g'ri javob: {question['correct_answer']}")
# #             st.write(f"Sizning javobingiz: {user_answers[i]}")

# #         # PDF hisobotni yaratish
# #         pdf = generate_pdf_report(selected_questions, user_answers, score)
# #         pdf_file_path = "test_results.pdf"
# #         pdf.output(pdf_file_path)
        
# #         # PDF-ni yuklab olish havolasi
# #         with open(pdf_file_path, "rb") as pdf_file:
# #             pdf_data = pdf_file.read()
# #         st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")


# # if __name__ == "__main__":
# #     main()
