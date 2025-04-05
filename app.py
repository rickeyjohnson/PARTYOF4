import streamlit as st
from data.employee_db import create_employee, get_employee
from reviews.performance_review import performance_review_chat
from reviews.self_assessment import self_assessment_chat
from reviews.peer_review import peer_review_chat
from fake_ai_api import generate_employee_profile_summary, get_job_match_score  # Import AI summary function
from data.job_listing import get_all_jobs

EMPLOYEE_ID = "12345"

def rickey_page(employee_id):
    # Initialize
    if "employee_created" not in st.session_state:
        create_employee(
            employee_id=employee_id,
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
            employee_profile = get_employee(employee_id)

            # Generate the employee summary using the LLM (simulated API call)
            employee_summary = generate_employee_profile_summary(
                employee_profile,
                combined_responses['performance_review'],
                combined_responses['self_assessment'],
                combined_responses['peer_review']
            )

            # Display the comprehensive summary
            st.text_area("Employee Comprehensive Summary", employee_summary, height=400)

            result = []
            for job in get_all_jobs():
                result.append(get_job_match_score(employee_summary, job))

            st.title('JOB MATCHING')
            st.write(result)

    elif page == "👨‍💼 Performance Review":
        performance_review_chat("12345")

    elif page == "🧠 Self Assessment":
        self_assessment_chat("12345")

    elif page == "🤝 Peer Review":
        peer_review_chat("12345")


def page1():
    if st.button("Job Recommendations"):
        st.session_state.current_page = "page_2"
        st.rerun()
    st.title("Employee Evaluation")

    # Create two columns
    left_col, right_col = st.columns(2)

    # Left side content
    with left_col:
        st.header("Employee Info")
        performance_status = "Requested"
        if st.session_state.get("performance_done", False):
            performance_status = "Completed"
        st.write(f"Performance/Project Review | **Status: {performance_status}**")

        peer_status = "Requested"
        if st.session_state.get("peer_done", False):
            performance_status = "Completed"
        st.write(f"Peer Reviews | **Status: {peer_status}**")

        self_status = "Requested"
        if st.session_state.get("self_done", False):
            performance_status = "Completed"
        st.write(f"Peer Reviews | **Status: {self_status}**")

    # Right side content
    with right_col:
        st.header("Job Openings")
        message = st.text_area("Write your message here. Be sure to include technical"+ 
        " and soft skills that will likely be needed for the role:")
        st.button("Submit")
    
    # Submit data for employee profile
    left, center, right = st.columns([1, 2, 1])
    with center:
        if st.button("Generate Evaluation"):
            st.session_state.current_page = "page_2"
            st.rerun()

def page2():
    if st.button("Employee Evaluation"):
        st.session_state.current_page = "page_1"
        st.rerun()
    st.title("Jawn Dough")

    # Top Section: Strengths and Needs Work
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.subheader("Strengths")
        st.write("**Tech**")
        st.markdown("- Python")
        st.markdown("- Java")
        st.write("**Soft**")
        st.markdown("- Teamwork")
        st.markdown("- Communication")

    with col2:
        st.markdown("<div style='font-size: 4em; text-align: center;'>😊</div>", unsafe_allow_html=True)

    with col3:
        st.subheader("Needs work")
        st.write("**Tech**")
        st.markdown("- No C++")
        st.markdown("- No SQL")
        st.write("**Soft**")
        st.markdown("- No Leadership")

    
    st.subheader("Jawn Matches")

    # Bottom Section: Job Matches
    num_jobs = 5
    job_percentages = [100, 84, 69, 54, 12]
    cols = st.columns(num_jobs)

    for i in range(num_jobs):
        #with cols[i]:
            #st.markdown(f"<div style='text-align: center;'>Job #{i+1}</div>", unsafe_allow_html=True)
            #st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>{job_percentages[i]}%</div>", unsafe_allow_html=True)
        with st.expander(f"Job #{i+1} | {job_percentages[i]}% Match"):
            st.write("**Description:**")
            st.markdown(f"THIs GUY FITS PERFECT")

if __name__ == '__main__':
    if "current_page" not in st.session_state:
        st.session_state.current_page = "page_1"

    if st.session_state.current_page == "page_1":
        page1()
    elif st.session_state.current_page == "page_2":
        page2()

    rickey_page(EMPLOYEE_ID)
