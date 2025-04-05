import streamlit as st
from employee_db import create_employee, get_employee
from pages.performance_review import performance_review_chat
from pages.self_assessment import self_assessment_chat
from pages.peer_review import peer_review_chat
from fake_ai_api import generate_employee_profile_summary  # Import AI summary function

EMPLOYEE_ID = "12345"
# Initialize
if "employee_created" not in st.session_state:
    create_employee(
        employee_id=EMPLOYEE_ID,
        name="John Doe",
        role="Software Developer",
        department="Engineering",
        skills=["Python", "Machine Learning", "Data Analysis"],
        years_experience=5
    )
    st.session_state.employee_created = True

# App UI
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "👨‍💼 Performance Review", "🧠 Self Assessment", "🤝 Peer Review"])

st.title("💼 Internal Talent Review Portal")

if page == "🏠 Home":
    st.subheader("Welcome to your dashboard")
    
    # Check if all responses exist
    all_complete = st.session_state.get("performance_done", False) and \
                    st.session_state.get("self_done", False) and \
                    st.session_state.get("peer_done", False)
    
    if not all_complete:
        st.info("Please complete all 3 reviews using the sidebar.")
    else:
        st.success("✅ All reviews completed!")
        st.markdown("### 📄 Full Review Summary")

        # Combine all responses into a single string
        combined_responses = {
            "performance_review": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("performance_responses", {}).items()]),
            "self_assessment": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("self_assessment_responses", {}).items()]),
            "peer_review": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("peer_responses", {}).items()])
        }

        # Get the employee profile
        employee_profile = get_employee(EMPLOYEE_ID)

        # Generate the employee summary using the LLM (simulated API call)
        employee_summary = generate_employee_profile_summary(
            employee_profile,
            combined_responses['performance_review'],
            combined_responses['self_assessment'],
            combined_responses['peer_review']
        )

        # Display the comprehensive summary
        st.text_area("Employee Comprehensive Summary", employee_summary, height=400)

elif page == "👨‍💼 Performance Review":
    performance_review_chat("12345")

elif page == "🧠 Self Assessment":
    self_assessment_chat("12345")

elif page == "🤝 Peer Review":
    peer_review_chat("12345")

###### RICKEY AI TESTING #######
# Fake AI Summary Generator Function
# def generate_fake_ai_summary(employee_data):
#     # Build a comprehensive "AI" summary of the employee using their profile and responses
#     performance_feedback = st.session_state.performance_responses if 'performance_responses' in st.session_state else {}
#     self_assessment_feedback = st.session_state.self_assessment_responses if 'self_assessment_responses' in st.session_state else {}
#     peer_review_feedback = st.session_state.peer_responses if 'peer_responses' in st.session_state else {}
    
#     summary = f"""
#     **Employee Profile:**
#     - Name: {employee_data['name']}
#     - Role: {employee_data['role']}
#     - Department: {employee_data['department']}
#     - Skills: {', '.join(employee_data['skills'])}
#     - Years of Experience: {employee_data['years_experience']}

#     **AI Summary of Reviews:**

#     Based on the reviews and assessments provided, the following insights can be made about {employee_data['name']}:

#     **Performance Review Insights:**
#     - {', '.join([f"{q}: {a}" for q, a in performance_feedback.items()])}

#     **Self-Assessment Insights:**
#     - {', '.join([f"{q}: {a}" for q, a in self_assessment_feedback.items()])}

#     **Peer Review Insights:**
#     - {', '.join([f"{q}: {a}" for q, a in peer_review_feedback.items()])}

#     **Overall Summary:**
#     - {employee_data['name']} is a highly skilled employee with expertise in {', '.join(employee_data['skills'])}. They have a strong foundation in {employee_data['role']} and have contributed significantly to the {employee_data['department']} department. Based on feedback, {employee_data['name']} is commended for their {', '.join([feedback for feedback in performance_feedback.values() if feedback])}. Areas for improvement include {', '.join([feedback for feedback in performance_feedback.values() if 'improve' in feedback])}.
#     """

#     return summary


######## EVAN AND ANTHONY #############

# def page1():
#     if st.button("Page 2"):
#         st.session_state.current_page = "page_2"
#         st.rerun()
#     st.title("Page 1 Content")
#     st.write("This is the content of the first page.")
    

# def page2():
#     if st.button("Page 1"):
#         st.session_state.current_page = "page_1"
#         st.rerun()
#     st.title("Jawn Dough")

#     # Top Section: Strengths and Needs Work
#     col1, col2, col3 = st.columns([2, 1, 2])

#     with col1:
#         st.subheader("Strengths")
#         st.write("**Tech**")
#         st.markdown("- Python")
#         st.markdown("- Java")
#         st.write("**Soft**")
#         st.markdown("- Teamwork")
#         st.markdown("- Communication")

#     with col2:
#         st.markdown("<div style='font-size: 4em; text-align: center;'>😊</div>", unsafe_allow_html=True)

#     with col3:
#         st.subheader("Needs work")
#         st.write("**Tech**")
#         st.markdown("- No C++")
#         st.markdown("- No SQL")
#         st.write("**Soft**")
#         st.markdown("- No Leadership")

    
#     st.subheader("Jawn Matches")

#     # Bottom Section: Job Matches
#     num_jobs = 5
#     job_percentages = [100, 84, 69, 54, 12]
#     cols = st.columns(num_jobs)

#     for i in range(num_jobs):
#         with cols[i]:
#             st.markdown(f"<div style='text-align: center;'>Job #{i+1}</div>", unsafe_allow_html=True)
#             st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>{job_percentages[i]}%</div>", unsafe_allow_html=True)
            

    

# if "current_page" not in st.session_state:
#     st.session_state.current_page = "page_1"

# if st.session_state.current_page == "page_1":
#     page1()
# elif st.session_state.current_page == "page_2":
#     page2()