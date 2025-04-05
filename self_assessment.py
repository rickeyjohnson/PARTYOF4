# self_assessment.py

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

# List of self-assessment questions for the employee
self_assessment_questions = [
    {"question": "How would you rate your overall quality of work?", "type": "text"},
    {"question": "How would you rate your productivity and efficiency?", "type": "text"},
    {"question": "How would you rate your communication skills?", "type": "text"},
    {"question": "What are your key strengths?", "type": "text"},
    {"question": "In what areas do you need improvement?", "type": "text"},
    {"question": "What significant achievements or contributions have you made?", "type": "text"},
    {"question": "What feedback do you have for your own growth and development?", "type": "text"}
]

# Initialize session state to keep track of the current question and responses
if 'self_assessment_responses' not in st.session_state:
    st.session_state.self_assessment_responses = {}

# Function to display the current question and collect text responses in chat-style input
def display_self_assessment_question(index, employee_data):
    question = self_assessment_questions[index]
    # Personalize the question by replacing {name} with the employee's name
    personalized_question = question["question"]
    
    if question["type"] == "text":
        # Create a chat-style input box with st.chat_input
        user_input = st.chat_input("Your response:", key=f"self_input_{index}")
        if user_input:
            # Display the user input as part of the conversation
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.self_assessment_responses[personalized_question] = user_input
            # Increment the question index immediately after the response is recorded
            st.session_state.self_assessment_question_index += 1
            return True
    return False

# Main function to display the self-assessment chat flow
def self_assessment_chat():
    st.title("💬 Self-Assessment Chat")
    
    # Ask for the employee ID to fetch their profile
    employee_id = st.text_input("Enter Employee ID for Self-Assessment", "")
    
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
        if 'self_assessment_question_index' not in st.session_state:
            st.session_state.self_assessment_question_index = 0

        # Display the chat messages so far
        if st.session_state.self_assessment_question_index < len(self_assessment_questions):
            for i in range(st.session_state.self_assessment_question_index):
                question = self_assessment_questions[i]
                response = st.session_state.self_assessment_responses.get(question["question"], "No response yet.")
                
                st.chat_message("assistant").markdown(f"**Q{str(i+1)}**: {question['question']}")
                st.chat_message("user").markdown(f"**A**: {response}")

            # Check if we need to display the current question
            question = self_assessment_questions[st.session_state.self_assessment_question_index]
            st.chat_message("assistant").markdown(f"**Q{str(st.session_state.self_assessment_question_index+1)}**: {question['question']}")
            
            # Wait for the user's response
            if display_self_assessment_question(st.session_state.self_assessment_question_index, employee_data):
                # Force a page rerun to show the next question
                st.experimental_rerun()
        else:
            # Once all questions are answered, show a thank you message and the Q/A summary
            st.success("Thank you for your response!")
            st.markdown("### 📄 Self-Assessment Summary:")

            # Collect all responses and format them in a string
            self_assessment_summary = ""
            for q, a in st.session_state.self_assessment_responses.items():
                self_assessment_summary += f"**Q**: {q}\n**A**: {a}\n\n"

            # Display the review summary in a text area
            st.text_area("Full Responses (for HR or report generation)", self_assessment_summary, height=300)

            # Button to restart the questionnaire
            if st.button("Restart Self-Assessment"):
                st.session_state.self_assessment_responses = {}
                st.session_state.self_assessment_question_index = 0
                st.experimental_rerun()

# Run the main app
if __name__ == '__main__':
    self_assessment_chat()