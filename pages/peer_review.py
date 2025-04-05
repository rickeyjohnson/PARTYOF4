# peer_review.py
import streamlit as st
from employee_db import get_employee

# List of peer review questions for the employee
peer_review_questions = [
    {"question": "How would you rate {name}'s collaboration with peers?", "type": "text"},
    {"question": "How well does {name} communicate with teammates?", "type": "text"},
    # {"question": "How would you rate {name}'s contribution to team goals?", "type": "text"},
    # {"question": "What are {name}'s key strengths in a team setting?", "type": "text"},
    # {"question": "In what areas could {name} improve when working with the team?", "type": "text"},
    # {"question": "How does {name} handle feedback from teammates?", "type": "text"},
    # {"question": "What are some examples of {name}'s contributions to the team's success?", "type": "text"}
]

if 'peer_responses' not in st.session_state:
    st.session_state.peer_responses = {}

def display_peer_question(index, employee_data):
    question = peer_review_questions[index]
    personalized_question = question["question"].format(name=employee_data["name"])
    
    if question["type"] == "text":
        user_input = st.chat_input("Your response:", key=f"peer_input_{index}")
        if user_input:
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.peer_responses[personalized_question] = user_input
            st.session_state.peer_question_index += 1
            return True
    return False

def peer_review_chat(employee_id):
    st.title("💬 Peer Review Chat")

    employee_data = get_employee(employee_id)

    if "peer_responses" not in st.session_state:
        st.session_state.peer_responses = {}
    if "peer_question_index" not in st.session_state:
        st.session_state.peer_question_index = 0
    
    if "peer_done" not in st.session_state:
        st.session_state.peer_done = False

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

    if 'peer_question_index' not in st.session_state:
        st.session_state.peer_question_index = 0

    if st.session_state.peer_question_index < len(peer_review_questions):
        for i in range(st.session_state.peer_question_index):
            question = peer_review_questions[i]
            personalized_question = question["question"].format(name=employee_data["name"])
            response = st.session_state.peer_responses.get(personalized_question, "No response yet.")
            
            st.chat_message("assistant").markdown(f"**Q{str(i+1)}**: {personalized_question}")
            st.chat_message("user").markdown(f"**A**: {response}")

        current_question = peer_review_questions[st.session_state.peer_question_index]
        personalized_question = current_question["question"].format(name=employee_data["name"])
        st.chat_message("assistant").markdown(f"**Q{str(st.session_state.peer_question_index+1)}**: {personalized_question}")

        if display_peer_question(st.session_state.peer_question_index, employee_data):
            st.rerun()
    else:
        st.success("✅ Thank you for your response!")
        # Save responses into session state for display in app.py
        st.session_state.peer_responses = st.session_state.peer_responses

        # Signal completion
        st.session_state.peer_done = True
