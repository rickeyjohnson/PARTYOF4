# performance_review.py
import streamlit as st
from data.employee_db import get_employee

questions = [
    {"question": "How would you rate {name}'s overall quality of work?", "type": "text"},
    {"question": "How would you rate {name}'s productivity and efficiency?", "type": "text"},
    # {"question": "How would you rate {name}'s communication skills?", "type": "text"},
    # {"question": "What are {name}'s key strengths?", "type": "text"},
    # {"question": "In what areas does {name} need improvement?", "type": "text"},
    # {"question": "What significant achievements or contributions has {name} made?", "type": "text"},
    # {"question": "What feedback do you have to help {name} grow and develop in their career?", "type": "text"}
]

def display_question(index, employee_data):
    question = questions[index]
    personalized_question = question["question"].format(name=employee_data["name"])

    if question["type"] == "text":
        user_input = st.chat_input("Your response:", key=f"text_input_{index}")
        if user_input:
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.responses[personalized_question] = user_input
            st.session_state.question_index += 1
            return True
    return False

def performance_review_chat(employee_id):
    st.title("💬 Performance Review Chat")

    employee_data = get_employee(employee_id)

    if "performance_responses" not in st.session_state:
        st.session_state.performance_responses = {}
    if "performance_question_index" not in st.session_state:
        st.session_state.performance_question_index = 0

    if "performance_done" not in st.session_state:
        st.session_state.performance_done = False

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

    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    if st.session_state.question_index < len(questions):
        for i in range(st.session_state.question_index):
            q = questions[i]
            personalized = q["question"].format(name=employee_data["name"])
            a = st.session_state.responses.get(personalized, "No response yet.")
            st.chat_message("assistant").markdown(f"**Q{i+1}**: {personalized}")
            st.chat_message("user").markdown(f"**A**: {a}")

        current_q = questions[st.session_state.question_index]
        personalized = current_q["question"].format(name=employee_data["name"])
        st.chat_message("assistant").markdown(f"**Q{st.session_state.question_index+1}**: {personalized}")
        
        if display_question(st.session_state.question_index, employee_data):
            st.rerun()
    else:
        st.success("✅ Thank you for your response!")
        
        # Save responses into session state for display in app.py
        st.session_state.performance_responses = st.session_state.responses

        # Signal completion
        st.session_state.performance_done = True
