# self_assessment.py
import streamlit as st
from data.employee_db import get_employee

# Self-assessment questions for the employee
self_assessment_questions = [
    {"question": "How would you rate your overall quality of work?", "type": "text"},
    {"question": "How would you rate your productivity and efficiency?", "type": "text"},
    # {"question": "How would you rate your communication skills?", "type": "text"},
    # {"question": "What are your key strengths?", "type": "text"},
    # {"question": "In what areas do you need improvement?", "type": "text"},
    # {"question": "What significant achievements or contributions have you made?", "type": "text"},
    # {"question": "What feedback do you have for your own growth and development?", "type": "text"}
]

# Initialize session state to keep track of the current question and responses
if 'self_assessment_responses' not in st.session_state:
    st.session_state.self_assessment_responses = {}

# Function to display a self-assessment question
def display_self_assessment_question(index, employee_data):
    question = self_assessment_questions[index]
    personalized_question = question["question"]

    if question["type"] == "text":
        user_input = st.chat_input("Your response:", key=f"self_input_{index}")
        if user_input:
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.self_assessment_responses[personalized_question] = user_input
            st.session_state.self_assessment_question_index += 1
            return True
    return False

# Main self-assessment chat flow
def self_assessment_chat(employee_id):
    st.title("💬 Self-Assessment Chat")

    employee_data = get_employee(employee_id)

    if "self_assessment_responses" not in st.session_state:
        st.session_state.self_assessment_responses = {}
    if "self_assessment_question_index" not in st.session_state:
        st.session_state.self_assessment_question_index = 0

    if "self_assessment_done" not in st.session_state:
        st.session_state.self_assessment_done = False


    if not employee_data:
        st.error("Employee not found!")
        return

    st.markdown("### Employee Profile")
    st.markdown(f"""
    **Name**: {employee_data['name']}
    **Role**: {employee_data['role']}
    **Department**: {employee_data['department']}
    **Skills**: {', '.join(employee_data['skills'])}
    **Years of Experience**: {employee_data['years_experience']}
    """)

    if 'self_assessment_question_index' not in st.session_state:
        st.session_state.self_assessment_question_index = 0

    if st.session_state.self_assessment_question_index < len(self_assessment_questions):
        for i in range(st.session_state.self_assessment_question_index):
            question = self_assessment_questions[i]
            response = st.session_state.self_assessment_responses.get(question["question"], "No response yet.")
            st.chat_message("assistant").markdown(f"**Q{str(i+1)}**: {question['question']}")
            st.chat_message("user").markdown(f"**A**: {response}")

        current_question = self_assessment_questions[st.session_state.self_assessment_question_index]
        st.chat_message("assistant").markdown(f"**Q{str(st.session_state.self_assessment_question_index+1)}**: {current_question['question']}")

        if display_self_assessment_question(st.session_state.self_assessment_question_index, employee_data):
            st.rerun()
    else:
        st.success("✅ Thank you for your response!")

        # Save responses into session state for display in app.py
        st.session_state.self_assessment_responses = st.session_state.self_assessment_responses

        # Signal completion
        st.session_state.self_done = True
