# file: streamlit_test_app.py
import streamlit as st
import random
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
            random.shuffle(options)  # Javoblarni chalkashtirish
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
        if question["correct_answer"] == user_answers[i]:
            correct_count += 1
    return correct_count

# PDF hisobotni yaratish funksiyasi
def generate_pdf_report(questions, user_answers, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test Natijalari", ln=True, align='C')
    pdf.ln(10)

    for i, question in enumerate(questions):
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, txt=f"{i + 1}. {question['question']}", ln=True)
        pdf.cell(0, 10, txt=f"  To'g'ri javob: {question['correct_answer']}", ln=True)
        pdf.cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}", ln=True)
        pdf.ln(5)

    pdf.set_font("Arial", size=12)
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
    user_answers = []

    # Har bir savolni chiqarish
    for i, question in enumerate(selected_questions):
        st.subheader(f"{i + 1}. {question['question']}")
        user_answer = st.radio(
            "Javobingizni tanlang:",
            question["options"],
            key=f"q{selected_chunk_index}_{i}"  # Unique key for each question
        )
        user_answers.append(user_answer)

    # Javoblarni topshirish
    if st.button("Testni yakunlash"):
        score = calculate_score(selected_questions, user_answers)
        st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(selected_questions)}")
        st.write("Natijalar:")
        for i, question in enumerate(selected_questions):
            st.write(f"**{i + 1}. {question['question']}**")
            st.write(f"To'g'ri javob: {question['correct_answer']}")
            st.write(f"Sizning javobingiz: {user_answers[i]}")

        # PDF hisobotni yaratish
        pdf = generate_pdf_report(selected_questions, user_answers, score)
        pdf_file_path = "test_results.pdf"
        pdf.output(pdf_file_path)
        
        # PDF-ni yuklab olish havolasi
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
