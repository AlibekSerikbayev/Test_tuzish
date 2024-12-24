import streamlit as st
import os

# Global variables
savollar = []
javoblar = []
variant_b = []
variant_c = []
variant_d = []
correct_answers = 0

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

def display_question():
    """
    Displays the current question and its options.
    """
    current_question_index = st.session_state["current_question_index"]
    if current_question_index < 0 or current_question_index >= len(savollar):
        st.warning("Savollar qolmadi!")
        return
    
    st.write(f"### {savollar[current_question_index]}")
    
    # Options in their original order
    options = [
        javoblar[current_question_index], 
        variant_b[current_question_index], 
        variant_c[current_question_index], 
        variant_d[current_question_index]
    ]
    
    selected_option = st.radio(
        "Javob variantlarini tanlang:", 
        options, 
        key=f"question_{current_question_index}"
    )
    
    if st.button("Javobni tekshirish", key=f"check_{current_question_index}"):
        check_answer(selected_option)

def check_answer(selected_answer):
    """
    Checks if the selected answer is correct and moves to the next question.
    """
    global correct_answers
    current_question_index = st.session_state["current_question_index"]
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
    global correct_answers

    # Initialize session state
    if "current_question_index" not in st.session_state:
        st.session_state["current_question_index"] = 0

    st.title("Savollarni Yuklash Va Test")
    
    # File upload
    uploaded_file = st.file_uploader("Savollarni yuklash uchun fayl tanlang (.txt):", type="txt")
    
    if uploaded_file:
        # Save uploaded file temporarily
        file_path = os.path.join("temp_questions.txt")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load questions
        load_questions(file_path)
        os.remove(file_path)  # Clean up temporary file
        
        # Reset test state
        st.session_state["current_question_index"] = 0
        correct_answers = 0
        st.success("Savollar yuklandi!")
    
    # Display the current question
    if savollar:
        question_labels = [f"Savol {i + 1}" for i in range(len(savollar))]
        selected_question_label = st.selectbox(
            "Savolni tanlang:", 
            question_labels, 
            index=st.session_state["current_question_index"],
            on_change=lambda: st.session_state.update(current_question_index=question_labels.index(st.session_state["Savolni tanlang"]))
        )
        
        display_question()
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Oldingi Savol"):
                if st.session_state["current_question_index"] > 0:
                    st.session_state["current_question_index"] -= 1
        with col2:
            if st.button("Keyingi Savol"):
                if st.session_state["current_question_index"] < len(savollar) - 1:
                    st.session_state["current_question_index"] += 1
    
    # Show progress
    st.write(f"To'g'ri javoblar: {correct_answers}/{len(savollar)}")

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
#     Displays the current question and its options using TextBox and RadioButton.
#     """
#     current_question_index = st.session_state.get("current_question_index", 0)
#     if current_question_index < 0 or current_question_index >= len(savollar):
#         st.warning("Boshqa savollar qolmadi!")
#         return

#     # Show the current question
#     st.text_area("Savol", savollar[current_question_index], height=100, disabled=True)
    
#     # Options without shuffling
#     options = [javoblar[current_question_index], variant_b[current_question_index], variant_c[current_question_index], variant_d[current_question_index]]
    
#     # Panel-like layout for options
#     selected_option = st.radio("Javob variantlarini tanlang:", options, key=f"question_{current_question_index}")
    
#     if st.button("Natijani Tekshirish"):
#         check_answer(current_question_index, selected_option)
    
#     # Navigation buttons
#     cols = st.columns(2)
#     with cols[0]:
#         if st.button("⬅️ Oldinga", key="prev"):
#             st.session_state.current_question_index = max(0, current_question_index - 1)
#     with cols[1]:
#         if st.button("➡️ Keyingi", key="next"):
#             st.session_state.current_question_index = min(len(savollar) - 1, current_question_index + 1)

# def check_answer(current_question_index, selected_answer):
#     """
#     Checks if the selected answer is correct and proceeds to the next question.
#     """
#     correct_answer = javoblar[current_question_index]
#     if selected_answer == correct_answer:
#         st.success("To'g'ri javob!")
#     else:
#         st.error(f"Noto'g'ri javob! To'g'ri javob: {correct_answer}")
    
#     # Automatically move to the next question
#     if current_question_index + 1 < len(savollar):
#         st.session_state.current_question_index += 1
#     else:
#         st.warning("Savollar tugadi!")

# def main():
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
#         st.success("Savollar yuklandi!")
    
#     # Display the current question
#     if savollar:
#         display_question()

# if __name__ == "__main__":
#     main()
