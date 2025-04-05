import streamlit as st
from data.employee_db import create_employee, get_employee
from reviews.performance_review import performance_review_chat
from reviews.self_assessment import self_assessment_chat
from reviews.peer_review import peer_review_chat
from fake_ai_api import generate_employee_profile_summary, get_job_match_score
from data.job_listing import get_all_jobs

st.set_page_config(
    page_title="Employee Evaluation",
    layout="wide",  # Use "wide" layout for full width
    initial_sidebar_state="collapsed"  # Optional: start sidebar collapsed
)

def page1():
    if st.button("Job Recommendations"):
        st.session_state.current_page = "page_2"
        st.rerun()

    # Top bar with title
    with st.container():
        st.markdown(
            """
            <style>
                .banner {
                    position: relative;
                    text-align: center;
                    color: red; /* Set title color to red */
                    height: 400px; /* Set the height of the banner in pixels */
                    overflow: hidden;
                }
                .banner img {
                    width: 100%;
                    height: 100%; /* Set image to cover the banner height */
                    object-fit: cover; /* Ensure the image covers the container without distortion */
                    object-position: top; /* Focus on the top of the image */
                }
                .banner h1 {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 2.5em; /* Adjust font size as needed */
                    color: red; /* Set title color to red */
                }
            </style>
            <div class="banner">
                <img src="https://techstartups.com/wp-content/uploads/2021/02/Chevron-Low-Carbon.jpg" alt="Banner Image">
                <h1>TITLE</h1>
            </div>
            """, unsafe_allow_html=True
        )



    # Main layout with two columns
    main_col1, main_col2 = st.columns([2, 1])

    # Left column: Employee Info Card
    with main_col1:
        with st.container():
            st.markdown("### 👤 Employee Info")

            st.markdown("---")

            # Placeholder for profile + basic info
            st.image("https://via.placeholder.com/80", width=80)
            st.write("Name: Jawn Dough")
            st.write("Role: Software Engineer")

            st.markdown("---")

            # Review status boxes
            def review_status(label, key):
                status = "Requested"
                if st.session_state.get(key, False):
                    status = "Completed"
                return f"**{label}** | Status: `{status}`"

            st.write(review_status("Performance/Project Review", "performance_done"))
            st.write(review_status("Peer Review", "peer_done"))
            st.write(review_status("Self Review", "self_done"))

            st.markdown("---")

            # Colored match bars (visualized as progress bars)
            st.write("### Match Percentages")
            st.progress(0.95)
            st.progress(0.75)
            st.progress(0.55)

    # Right column: Jobs and Submission
    with main_col2:
        with st.container():
            st.markdown("### 🧰 Jobs")

            # Text editor for entering jobs
            job_input = st.text_area("Enter Job Description", height=200)

            # Button to display job input (simulating adding job)
            if st.button("Submit Job"):
                if job_input.strip():  # Only show if input is not empty
                    st.success(f"Job added: {job_input.strip()}")
                else:
                    st.error("Please enter a job description before submitting.")

    # Centered submission button
    left, center, right = st.columns([1, 2, 1])
    with center:
        if st.button("Generate Evaluation"):
            st.session_state.current_page = "page_2"
            st.rerun()


if __name__ == '__main__':
    if "current_page" not in st.session_state:
        st.session_state.current_page = "page_1"

    if st.session_state.current_page == "page_1":
        page1()
    elif st.session_state.current_page == "page_2":
        page2()