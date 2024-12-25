# file: streamlit_test_app.py
import streamlit as st
import random

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

# Streamlit interfeysi
def main():
    st.title("Streamlit Test Tizimi")
    st.write("Quyidagi testga javob bering:")

    # Test faylini yuklash
    test_file = "test_template.txt"  # Test fayli nomi
    questions = load_test_from_file(test_file)

    # Javoblarni saqlash
    user_answers = []

    # Har bir savolni chiqarish
    for i, question in enumerate(questions):
        st.subheader(f"{i + 1}. {question['question']}")
        user_answer = st.radio(
            "Javobingizni tanlang:",
            question["options"],
            key=f"q{i}"  # Har bir savol uchun unique key
        )
        user_answers.append(user_answer)
    
    # Javoblarni topshirish
    if st.button("Testni yakunlash"):
        score = calculate_score(questions, user_answers)
        st.success(f"Test yakunlandi! To'g'ri javoblar soni: {score}/{len(questions)}")
        st.write("Natijalar:")
        for i, question in enumerate(questions):
            st.write(f"**{i + 1}. {question['question']}**")
            st.write(f"To'g'ri javob: {question['correct_answer']}")
            st.write(f"Sizning javobingiz: {user_answers[i]}")

if __name__ == "__main__":
    main()


# import streamlit as st
# import os

# # Global variables
# savollar = []
# javoblar = []
# variant_b = []
# variant_c = []
# variant_d = []
# correct_answers = 0

# def load_questions(file_path):
#     """
#     Loads questions from a file and processes them into the global lists.
#     """
#     global savollar, javoblar, variant_b, variant_c, variant_d
#     savollar.clear()
#     javoblar.clear()
#     variant_b.clear()
#     variant_c.clear()
#     variant_d.clear()
    
#     with open(file_path, 'r', encoding='utf-8') as file:
#         text = file.read()
#         sections = text.split("****[1]")
#         for question_number, section in enumerate(sections, start=1):
#             first_index = section.find("++++")
#             if first_index != -1:
#                 question = section[:first_index].strip()
#                 parts = section[first_index + 4:].split("++++")
#                 answer = parts[0].strip() if len(parts) > 0 else "Variant yo'q"
#                 second_variant = parts[1].strip() if len(parts) > 1 else "Variant yo'q"
#                 third_variant = parts[2].strip() if len(parts) > 2 else "Variant yo'q"
#                 fourth_variant = parts[3].split("%%%%")[0].strip() if len(parts) > 3 else "Variant yo'q"
#                 savollar.append(f"Savol {question_number}: {question}")
#                 javoblar.append(answer)
#                 variant_b.append(second_variant)
#                 variant_c.append(third_variant)
#                 variant_d.append(fourth_variant)

# def display_question():
#     """
#     Displays the current question and its options.
#     """
#     current_question_index = st.session_state["current_question_index"]
#     if current_question_index < 0 or current_question_index >= len(savollar):
#         st.warning("Savollar qolmadi!")
#         return
    
#     st.write(f"### {savollar[current_question_index]}")
    
#     # Options in their original order
#     options = [
#         javoblar[current_question_index], 
#         variant_b[current_question_index], 
#         variant_c[current_question_index], 
#         variant_d[current_question_index]
#     ]
    
#     selected_option = st.radio(
#         "Javob variantlarini tanlang:", 
#         options, 
#         key=f"question_{current_question_index}"
#     )
    
#     if st.button("Javobni tekshirish", key=f"check_{current_question_index}"):
#         check_answer(selected_option)

# def check_answer(selected_answer):
#     """
#     Checks if the selected answer is correct and moves to the next question.
#     """
#     global correct_answers
#     current_question_index = st.session_state["current_question_index"]
#     correct_answer = javoblar[current_question_index]
#     if selected_answer == correct_answer:
#         st.success("To'g'ri javob!")
#         correct_answers += 1
#     else:
#         st.error(f"Noto'g'ri javob! To'g'ri javob: {correct_answer}")

# def main():
#     global correct_answers

#     # Initialize session state
#     if "current_question_index" not in st.session_state:
#         st.session_state["current_question_index"] = 0

#     st.title("Savollarni Yuklash Va Test")
    
#     # File upload
#     uploaded_file = st.file_uploader("Savollarni yuklash uchun fayl tanlang (.txt):", type="txt")
    
#     if uploaded_file:
#         # Save uploaded file temporarily
#         file_path = os.path.join("temp_questions.txt")
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         # Load questions
#         load_questions(file_path)
#         os.remove(file_path)  # Clean up temporary file
        
#         # Reset test state
#         st.session_state["current_question_index"] = 0
#         correct_answers = 0
#         st.success("Savollar yuklandi!")
    
#     # Display the current question
#     if savollar:
#         question_labels = [f"Savol {i + 1}" for i in range(len(savollar))]
        
#         # Save current selected question label in session state
#         if "selected_question_label" not in st.session_state:
#             st.session_state["selected_question_label"] = question_labels[0]
        
#         # Automatically update selected question based on current index
#         selected_question_label = st.selectbox(
#             "Savolni tanlang:", 
#             question_labels, 
#             index=st.session_state["current_question_index"]
#         )
#         st.session_state["current_question_index"] = question_labels.index(selected_question_label)
        
#         display_question()
        
#         # Navigation buttons
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Oldingi Savol"):
#                 if st.session_state["current_question_index"] > 0:
#                     st.session_state["current_question_index"] -= 1
#         with col2:
#             if st.button("Keyingi Savol"):
#                 if st.session_state["current_question_index"] < len(savollar) - 1:
#                     st.session_state["current_question_index"] += 1
    
#     # Show progress
#     st.write(f"To'g'ri javoblar: {correct_answers}/{len(savollar)}")

# if __name__ == "__main__":
#     main()
