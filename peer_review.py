# peer_review.py

import streamlit as st
from employee_db import create_employee, get_employee, get_profile_summary

# Simulate creating an employee profile (you would typically retrieve this from a database)
create_employee(
    employee_id="12345",
    name="John Doe",
    role="Software Developer",
    department="Engineering",
    skills=["Python", "Machine Learning", "Data Analysis"],
    years_experience=5
)

# List of peer review questions for the employee
peer_review_questions = [
    {"question": "How would you rate {name}'s collaboration with peers?", "type": "text"},
    {"question": "How well does {name} communicate with teammates?", "type": "text"},
    {"question": "How would you rate {name}'s contribution to team goals?", "type": "text"},
    {"question": "What are {name}'s key strengths in a team setting?", "type": "text"},
    {"question": "In what areas could {name} improve when working with the team?", "type": "text"},
    {"question": "How does {name} handle feedback from teammates?", "type": "text"},
    {"question": "What are some examples of {name}'s contributions to the team's success?", "type": "text"}
]

# Initialize session state to keep track of the current question and responses
if 'peer_responses' not in st.session_state:
    st.session_state.peer_responses = {}

# Function to display the current question and collect text responses in chat-style input
def display_peer_question(index, employee_data):
    question = peer_review_questions[index]
    # Personalize the question by replacing {name} with the employee's name
    personalized_question = question["question"].format(name=employee_data["name"])
    
    if question["type"] == "text":
        # Create a chat-style input box with st.chat_input
        user_input = st.chat_input("Your response:", key=f"peer_input_{index}")
        if user_input:
            # Display the user input as part of the conversation
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.peer_responses[personalized_question] = user_input
            # Increment the question index immediately after the response is recorded
            st.session_state.peer_question_index += 1
            return True
    return False

# Main function to display the peer review chat flow
def peer_review_chat():
    st.title("💬 Peer Review Chat")
    
    # Ask for the employee ID to fetch their profile
    employee_id = st.text_input("Enter Employee ID for Peer Review", "")
    
    if employee_id:
        # Get the employee's data from the simulated database
        employee_data = get_employee(employee_id)
        
        if not employee_data:
            st.error("Employee not found!")
            return
        
        # Display employee profile summary
        st.markdown("### Employee Profile")
        profile_summary = f"""
        **Name**: {employee_data['name']}
        **Role**: {employee_data['role']}
        **Department**: {employee_data['department']}
        **Skills**: {', '.join(employee_data['skills'])}
        **Years of Experience**: {employee_data['years_experience']}
        """
        st.markdown(profile_summary)
    
        # Track the current question index
        if 'peer_question_index' not in st.session_state:
            st.session_state.peer_question_index = 0

        # Display the chat messages so far
        if st.session_state.peer_question_index < len(peer_review_questions):
            for i in range(st.session_state.peer_question_index):
                question = peer_review_questions[i]
                # Personalize the question by replacing {name} with the employee's name
                personalized_question = question["question"].format(name=employee_data["name"])
                response = st.session_state.peer_responses.get(personalized_question, "No response yet.")
                
                st.chat_message("assistant").markdown(f"**Q{str(i+1)}**: {personalized_question}")
                st.chat_message("user").markdown(f"**A**: {response}")

            # Check if we need to display the current question
            question = peer_review_questions[st.session_state.peer_question_index]
            # Personalize the question by replacing {name} with the employee's name
            personalized_question = question["question"].format(name=employee_data["name"])
            
            st.chat_message("assistant").markdown(f"**Q{str(st.session_state.peer_question_index+1)}**: {personalized_question}")
            
            # Wait for the user's response
            if display_peer_question(st.session_state.peer_question_index, employee_data):
                # Force a page rerun to show the next question
                st.experimental_rerun()
        else:
            # Once all questions are answered, show a thank you message and the Q/A summary
            st.success("Thank you for your response!")
            st.markdown("### 📄 Peer Review Summary:")

            # Collect all responses and format them in a string
            peer_review_summary = ""
            for q, a in st.session_state.peer_responses.items():
                peer_review_summary += f"**Q**: {q}\n**A**: {a}\n\n"

            # Display the review summary in a text area
            st.text_area("Full Responses (for HR or report generation)", peer_review_summary, height=300)

            # Button to restart the questionnaire
            if st.button("Restart Peer Review"):
                st.session_state.peer_responses = {}
                st.session_state.peer_question_index = 0
                st.experimental_rerun()

# Run the main app
if __name__ == '__main__':
    peer_review_chat()
