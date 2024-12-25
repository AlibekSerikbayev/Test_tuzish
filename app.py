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


# Natijalarni hisoblash funksiyasi
def calculate_score(questions, user_answers):
    correct_count = 0
    for i, question in enumerate(questions):
        if question["correct_answer"] == user_answers[i]:
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
        pdf.multi_cell(0, 10, txt=f"  Sizning javobingiz: {user_answers[i]}")
        pdf.ln(5)

    pdf.set_font("ArialUnicode", size=12)
    pdf.cell(0, 10, txt=f"To'g'ri javoblar soni: {score}/{len(questions)}", ln=True)
    return pdf


# Streamlit interfeysi
def main():
    st.title("Streamlit Test Tizimi")
    st.write("Savollarni birma-bir ko'ring va javob bering:")

    # Test faylini yuklash
    test_file = "test_template.txt"  # Test fayli nomi
    questions = load_test_from_file(test_file)
    
    # Session state uchun indeks va javoblar
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [None] * len(questions)
    if "show_result" not in st.session_state:
        st.session_state.show_result = False

    # Hozirgi savolni olish
    current_index = st.session_state.current_index
    current_question = questions[current_index]

    # Savolni ko'rsatish
    st.subheader(f"Savol {current_index + 1}/{len(questions)}")
    st.write(current_question["question"])
    user_answer = st.radio(
        "Javobingizni tanlang:",
        current_question["options"],
        key=f"q{current_index}",
        index=current_question["options"].index(st.session_state.user_answers[current_index]) if st.session_state.user_answers[current_index] else None
    )
    st.session_state.user_answers[current_index] = user_answer

    # Tekshirish tugmasi
    if st.button("Tekshirish"):
        if user_answer == current_question["correct_answer"]:
            st.success("To'g'ri javob!")
        else:
            st.error("Noto'g'ri javob!")
        st.session_state.show_result = True

    # Natija ko'rsatilgandan keyin avtomatik keyingi savolga o'tish
    if st.session_state.show_result:
        if current_index < len(questions) - 1:
            st.session_state.current_index += 1
            st.session_state.show_result = False
        else:
            st.success("Barcha savollar tugadi!")
            st.session_state.show_result = False

    # Testni yakunlash
    if st.button("Testni yakunlash"):
        score = calculate_score(questions, st.session_state.user_answers)
        st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(questions)}")
        st.write("Natijalar:")
        for i, question in enumerate(questions):
            st.write(f"**{i + 1}. {question['question']}**")
            st.write(f"To'g'ri javob: {question['correct_answer']}")
            st.write(f"Sizning javobingiz: {st.session_state.user_answers[i]}")

        # PDF hisobotni yaratish
        pdf = generate_pdf_report(questions, st.session_state.user_answers, score)
        pdf_file_path = "test_results.pdf"
        pdf.output(pdf_file_path)
        
        # PDF-ni yuklab olish havolasi
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button("Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
