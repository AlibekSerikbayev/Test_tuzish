import streamlit as st
import os

# Global variables
savollar = []
javoblar = []
variant_b = []
variant_c = []
variant_d = []

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

def display_question(selected_question_index):
    """
    Displays the question and its options using TextBox and RadioButton.
    """
    if selected_question_index < 0 or selected_question_index >= len(savollar):
        st.warning("Savollar qolmadi!")
        return
    
    # Show the current question
    st.text_area("Savol", savollar[selected_question_index], height=100, disabled=True)
    
    # Original options without shuffling
    options = [javoblar[selected_question_index], variant_b[selected_question_index], variant_c[selected_question_index], variant_d[selected_question_index]]
    
    # Panel-like layout for options
    selected_option = st.radio("Javob variantlarini tanlang:", options, key=f"question_{selected_question_index}")
    
    # Render options in TextBoxes
    cols = st.columns(4)
    for i, option in enumerate(options):
        with cols[i]:
            st.text_input(f"Variant {chr(65+i)}:", option, disabled=True)

    if st.button("Natijani Tekshirish", key=f"check_{selected_question_index}"):
        check_answer(selected_question_index, selected_option)

def check_answer(selected_question_index, selected_answer):
    """
    Checks if the selected answer is correct.
    """
    correct_answer = javoblar[selected_question_index]
    if selected_answer == correct_answer:
        st.success("To'g'ri javob!")
    else:
        st.error(f"Noto'g'ri javob! To'g'ri javob: {correct_answer}")

def main():
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
        
        # Load questions without shuffling
        load_questions(file_path)
        os.remove(file_path)  # Clean up temporary file
        
        # Reset test state
        st.session_state["current_question_index"] = 0
        st.success("Savollar yuklandi!")
    
    # Display the current question
    if savollar:
        question_labels = [f"Savol {i + 1}" for i in range(len(savollar))]
        selected_question_label = st.selectbox("Savolni tanlang:", question_labels)
        selected_question_index = question_labels.index(selected_question_label)
        
        display_question(selected_question_index)

if __name__ == "__main__":
    main()
