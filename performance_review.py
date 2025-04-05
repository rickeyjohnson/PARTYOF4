# performance_review.py

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

# List of structured and unstructured questions for the performance review
questions = [
    {"question": "How would you rate {name}'s overall quality of work?", "type": "text"},
    {"question": "How would you rate {name}'s productivity and efficiency?", "type": "text"},
    {"question": "How would you rate {name}'s communication skills?", "type": "text"},
    {"question": "What are {name}'s key strengths?", "type": "text"},
    {"question": "In what areas does {name} need improvement?", "type": "text"},
    {"question": "What significant achievements or contributions has {name} made?", "type": "text"},
    {"question": "What feedback do you have to help {name} grow and develop in their career?", "type": "text"}
]

# Initialize session state to keep track of the current question and responses
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Function to display the current question and collect text responses in chat-style input
def display_question(index, employee_data):
    question = questions[index]
    # Personalize the question by replacing {name} with the employee's name
    personalized_question = question["question"].format(name=employee_data["name"])
    
    if question["type"] == "text":
        # Create a chat-style input box with st.chat_input
        user_input = st.chat_input("Your response:", key=f"text_input_{index}")
        if user_input:
            # Display the user input as part of the conversation
            st.chat_message("user").markdown(f"**A**: {user_input}")
            st.session_state.responses[personalized_question] = user_input
            # Increment the question index immediately after the response is recorded
            st.session_state.question_index += 1
            return True
    return False

# Main function to display the review chat flow
def performance_review_chat():
    st.title("💬 Performance Review Chat")
    
    # Ask for the employee ID to fetch their profile
    employee_id = st.text_input("Enter Employee ID", "")
    
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
        if 'question_index' not in st.session_state:
            st.session_state.question_index = 0

        # Display the chat messages so far
        if st.session_state.question_index < len(questions):
            for i in range(st.session_state.question_index):
                question = questions[i]
                # Personalize the question by replacing {name} with the employee's name
                personalized_question = question["question"].format(name=employee_data["name"])
                response = st.session_state.responses.get(personalized_question, "No response yet.")
                
                st.chat_message("assistant").markdown(f"**Q{str(i+1)}**: {personalized_question}")
                st.chat_message("user").markdown(f"**A**: {response}")

            # Check if we need to display the current question
            question = questions[st.session_state.question_index]
            # Personalize the question by replacing {name} with the employee's name
            personalized_question = question["question"].format(name=employee_data["name"])
            
            st.chat_message("assistant").markdown(f"**Q{str(st.session_state.question_index+1)}**: {personalized_question}")
            
            # Wait for the user's response
            if display_question(st.session_state.question_index, employee_data):
                # Force a page rerun to show the next question
                st.rerun()
        else:
            # Once all questions are answered, show a thank you message and the Q/A summary
            st.success("Thank you for your response!")
            st.markdown("### 📄 Review Summary:")

            # Collect all responses and format them in a string
            review_summary = ""
            for q, a in st.session_state.responses.items():
                review_summary += f"**Q**: {q}\n**A**: {a}\n\n"

            # Display the review summary in a text area
            st.text_area("Full Responses (for HR or report generation)", review_summary, height=300)

            # Button to restart the questionnaire
            if st.button("Restart Review"):
                st.session_state.responses = {}
                st.session_state.question_index = 0
                st.experimental_rerun()
