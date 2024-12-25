import streamlit as st
from fpdf import FPDF

# Function to load test from file
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
            correct_answer = options[0]  # Correct answer is always the first
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer
            })
    return questions

# Function to split questions into chunks
def split_questions(questions, chunk_size=25):
    return [questions[i:i + chunk_size] for i in range(0, len(questions), chunk_size)]

# Function to calculate the score
def calculate_score(questions, user_answers):
    correct_count = 0
    for i, question in enumerate(questions):
        if question["correct_answer"] == user_answers[i]:
            correct_count += 1
    return correct_count

# Function to generate a PDF report
def generate_pdf_report(questions, user_answers, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test Results", ln=True, align='C')
    pdf.ln(10)

    for i, question in enumerate(questions):
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, txt=f"{i + 1}. {question['question']}")
        pdf.multi_cell(0, 10, txt=f"  Correct Answer: {question['correct_answer']}")
        pdf.multi_cell(0, 10, txt=f"  Your Answer: {user_answers[i]}")
        pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Correct answers: {score}/{len(questions)}", ln=True)
    return pdf

# Streamlit interface
def main():
    st.title("📘 Streamlit Test Tizimi")
    st.markdown("""<style>
        .title {
            font-family: Arial, sans-serif;
            text-align: center;
            color: #4CAF50;
        }
        .question {
            background-color: #f9f9f9;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .selected {
            background-color: #cce5ff !important;
        }
    </style>""", unsafe_allow_html=True)
    st.markdown("<h3 class='title'>Quyidagi testga javob bering:</h3>", unsafe_allow_html=True)

    # Load test file
    test_file = "test_template.txt"
    questions = load_test_from_file(test_file)

    # Split questions into chunks
    chunks = split_questions(questions, chunk_size=25)
    chunk_titles = [f"Savollar {i * 25 + 1}-{(i + 1) * 25}" for i in range(len(chunks))]
    
    # Select chunk
    selected_chunk_index = st.selectbox("Savollar bo‘limini tanlang:", 
                                        options=range(len(chunks)), 
                                        format_func=lambda x: chunk_titles[x])
    selected_questions = chunks[selected_chunk_index]

    # Initialize session state for user answers
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [None] * len(questions)

    # Font size adjustment
    font_size = st.slider("Shrift o'lchamini tanlang:", min_value=10, max_value=20, value=14)
    st.markdown(f"<style>.question {{ font-size: {font_size}px !important; }}</style>", unsafe_allow_html=True)

    # Display questions
    for i, question in enumerate(selected_questions):
        question_index = selected_chunk_index * 25 + i
        st.markdown(f"<div class='question' id='question-{i}'><b>{i + 1}. {question['question']}</b></div>", unsafe_allow_html=True)
        user_answer = st.radio(
            "Javobingizni tanlang:",
            question["options"],
            key=f"q{selected_chunk_index}_{i}",
            index=question["options"].index(st.session_state.user_answers[question_index])
            if st.session_state.user_answers[question_index] in question["options"] else -1
        )
        if user_answer:
            st.session_state.user_answers[question_index] = user_answer
            st.markdown(f"<style>#question-{i} {{ background-color: #cce5ff; }}</style>", unsafe_allow_html=True)

    # Submit answers
    if st.button("Testni yakunlash"):
        selected_answers = st.session_state.user_answers[selected_chunk_index * 25:(selected_chunk_index + 1) * 25]
        score = calculate_score(selected_questions, selected_answers)
        st.success(f"✅ Test yakunlandi! To'g'ri javoblar soni: {score}/{len(selected_questions)}")
        st.write("Natijalar:")
        for i, question in enumerate(selected_questions):
            st.write(f"**{i + 1}. {question['question']}**")
            st.write(f"To'g'ri javob: {question['correct_answer']}")
            st.write(f"Sizning javobingiz: {selected_answers[i]}")

        # Generate PDF
        pdf = generate_pdf_report(selected_questions, selected_answers, score)
        pdf_file_path = "test_results.pdf"
        pdf.output(pdf_file_path)
        
        # Provide PDF download link
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button("📄 Natijalarni PDF shaklda yuklab olish", data=pdf_data, file_name="test_results.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
