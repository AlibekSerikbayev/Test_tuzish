import streamlit as st
import random
import os

# Global variables
savollar = []
javoblar = []
variant_b = []
variant_c = []
variant_d = []
shuffled_options = []
current_question_index = 0
correct_answers = 0
range_size = 25

def load_questions(file_path):
    """
    Loads questions from a file and processes them into the global lists.
    """
    global savollar, javoblar, variant_b, variant_c, variant_d
    savollar.clear()
    javoblar.clear()
    variant_b.clear()
    variant_c.clear()
    variant_d.clear()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sections = text.split("****[1]")
        for question_number, section in enumerate(sections, start=1):
            first_index = section.find("++++")
            if first_index != -1:
                question = section[:first_index].strip()
                parts = section[first_index + 4:].split("++++")
                answer = parts[0].strip() if len(parts) > 0 else "Variant yo'q"
                second_variant = parts[1].strip() if len(parts) > 1 else "Variant yo'q"
                third_variant = parts[2].strip() if len(parts) > 2 else "Variant yo'q"
                fourth_variant = parts[3].split("%%%%")[0].strip() if len(parts) > 3 else "Variant yo'q"
                savollar.append(f"Savol {question_number}: {question}")
                javoblar.append(answer)
                variant_b.append(second_variant)
                variant_c.append(third_variant)
                variant_d.append(fourth_variant)

def shuffle_all_options():
    """
    Shuffles the options for each question.
    """
    global shuffled_options
    shuffled_options = []
    for i in range(len(savollar)):
        options = [javoblar[i], variant_b[i], variant_c[i], variant_d[i]]
        random.shuffle(options)
        shuffled_options.append(options)

def display_question():
    """
    Displays the current question and its options.
    """
    global current_question_index, shuffled_options
    if current_question_index < 0 or current_question_index >= len(savollar):
        st.warning("Savollar qolmadi!")
        return
    
    st.write(f"### {savollar[current_question_index]}")
    options = shuffled_options[current_question_index]
    
    selected_option = st.radio("Javob variantlarini tanlang:", options, key=f"question_{current_question_index}")
    
    if st.button("Javobni tekshirish"):
        check_answer(selected_option)

def check_answer(selected_answer):
    """
    Checks if the selected answer is correct.
    """
    global current_question_index, correct_answers
    correct_answer = javoblar[current_question_index]
    if selected_answer == correct_answer:
        st.success("To'g'ri javob!")
        correct_answers += 1
    else:
        st.error(f"Noto'g'ri javob! To'g'ri javob: {correct_answer}")
    
    # Move to the next question
    if current_question_index + 1 < len(savollar):
        st.session_state["current_question_index"] += 1
    else:
        st.info("Barcha savollar tugadi!")

def main():
    global current_question_index, correct_answers

    # Initialize session state
    if "current_question_index" not in st.session_state:
        st.session_state["current_question_index"] = 0
    current_question_index = st.session_state["current_question_index"]

    st.title("Savollarni Yuklash Va Test")
    
    # File upload
    uploaded_file = st.file_uploader("Savollarni yuklash uchun fayl tanlang (.txt):", type="txt")
    
    if uploaded_file:
        # Save uploaded file temporarily
        file_path = os.path.join("temp_questions.txt")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load questions and shuffle
        load_questions(file_path)
        shuffle_all_options()
        os.remove(file_path)  # Clean up temporary file
        
        # Reset test state
        st.session_state["current_question_index"] = 0
        correct_answers = 0
        st.success("Savollar yuklandi!")
    
    # Display the current question
    if savollar:
        display_question()
    
    # Show progress
    st.write(f"To'g'ri javoblar: {correct_answers}/{len(savollar)}")

if __name__ == "__main__":
    main()





















