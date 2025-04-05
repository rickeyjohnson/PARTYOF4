import streamlit as st
from data.employee_db import create_employee, get_employee
from reviews.performance_review import performance_review_chat
from reviews.self_assessment import self_assessment_chat
from reviews.peer_review import peer_review_chat
from fake_ai_api import generate_employee_profile_summary, get_job_match_score
from data.job_listing import get_all_jobs

def page2():
    # Main layout with two columns
    main_col1, main_col2 = st.columns([1,1])

    # Left column: Employee Info Card
    EMPLOYEE_ID = "12345"

    if "employee_created" not in st.session_state:
        create_employee(
            employee_id=EMPLOYEE_ID,
            name="John Doe",
            role="Software Developer",
            department="Engineering",
            skills=["Python", "Machine Learning", "Data Analysis"],
            years_experience=5,
            pfp_url="https://www.shutterstock.com/image-vector/vector-flat-illustration-grayscale-avatar-600nw-2264922221.jpg"
        )
        st.session_state.employee_created = True
            
        employee = get_employee(EMPLOYEE_ID)

        if not employee:
            st.error("Employee not found.")
            return
    # Left column: Employee Info Card
    with main_col1:
        # Display employee info in a container
        with st.container(border=True):
            # Layout: Display profile picture and name side by side
            profile_col1, profile_col2 = st.columns([1, 3])
            
            # Left column: Profile picture
            with profile_col1:
                pfp_url = employee.get("pfp")
                st.image(pfp_url)
            
            # Right column: Name and other details
            with profile_col2:
                st.title(f"{employee['name']}")
                st.markdown(f"**Role**: {employee['role']}")
            
            # st.markdown("---")
            
            # Employee feedback summary
            # st.markdown("### Feedback Summary")
            # feedback_summary = get_profile_summary(employee_id)
            # st.text_area("Feedback Summary", feedback_summary, height=200, disabled=True)
        

            st.markdown("---")

            # Review status boxes
            col1, col2 = st.columns([1,1])
            with col1:
                st.write("**Strengths**")
                st.write("*Technical Skills*")
                st.write("*Soft Skills*")
            with col2:
                st.write("**Needs Improvement**")
                st.write("*Technical Skills*")
                st.write("*Soft Skills*")
            
    # Right column: Jobs and Submission
    with main_col2:
        with st.container():
            # Bottom Section: Job Matches
            num_jobs = 5
            job_percentages = [100, 84, 69, 54, 12]
            cols = st.columns(num_jobs)

            for i in range(num_jobs):
                with st.expander(f"Job #{i+1} | {job_percentages[i]}% Match"):
                    st.write("**Description:**")
                    st.markdown(f"THIs GUY FITS PERFECT")
    
    if st.button("Employee Evaluation"):
        st.session_state.current_page = "page_1"
        st.rerun()
    with st.container(border=True):
        st.write(f"Description here:")

if __name__ == '__main__':
    page2()
