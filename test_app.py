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

def page1(employee_id):
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
                    bottom-padding: 20px;
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
                    font-size: 4em; /* Adjust font size as needed */
                    color: green; /* Set title color to red */
                    font-size: 8em; /* Adjust font size as needed */
                    color: green; /* Set title color to red */
                }
            </style>
            <div class="banner">
                <img src="https://techstartups.com/wp-content/uploads/2021/02/Chevron-Low-Carbon.jpg" alt="Banner Image">
                <h1>EMPLOYEE EVALUATION</h1>
                <h1>Employee Evaluation</h1>
            </div>
            """, unsafe_allow_html=True
        )


    # Main layout with two columns
    main_col1, main_col2 = st.columns([2, 1])

    # Left column: Employee Info Card
    with main_col1:
        st.title("👤 Employee(s)")
        employee = get_employee(employee_id)

        if not employee:
            st.error("Employee not found.")
            return
        
        # Display employee info in a container
        with st.container(border=True):
            # Layout: Display profile picture and name side by side
            profile_col1, profile_col2 = st.columns([1, 3])
            
            # Left column: Profile picture
            with profile_col1:
                pfp_url = employee.get("pfp")
                st.image(pfp_url, width=100)
            
            # Right column: Name and other details
            with profile_col2:
                st.title(f"{employee['name']}")

            st.markdown("---")

            st.markdown(f"**Role**: {employee['role']}")
            st.markdown(f"**Current Role**: {employee['role']}")  # Added Current Role
            st.markdown(f"**Department**: {employee['department']}")
            st.markdown(f"**Skills**: {', '.join(employee['skills'])}")
            st.markdown(f"**Years of Experience**: {employee['years_experience']}")
            
            # Employee feedback summary
            # st.subheader("💬 Feedback Summary")
            # feedback_summary = get_profile_summary(employee_id)
            # st.text_area("Feedback Summary", feedback_summary, height=200, disabled=True)
        

            st.markdown("---")

            # Review status boxes
            def review_status(label, key):
                status = "Requested"
                if st.session_state.get(key, False):
                    status = "Completed"
                return f"""
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{label}</strong>
                        <code>Status: {status}</code>
                    </div>
                """

            st.markdown(review_status("Performance/Project Review", "performance_done"), unsafe_allow_html=True)
            st.markdown(review_status("Peer Review", "peer_done"), unsafe_allow_html=True)
            st.markdown(review_status("Self Review", "self_done"), unsafe_allow_html=True)

            st.markdown("---")

            # Colored match bars (visualized as progress bars)
            st.write("### Match Percentages")
            st.progress(0.95)
            st.progress(0.75)
            st.progress(0.55)

            st.markdown("---")
            
            def review_status(label, key):
                status = "Requested"
                if st.session_state.get(key, False):
                    status = "Completed"
                return f"""
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{label}</strong>
                        <code>Status: {status}</code>
                    </div>
                """

            def review_status(employee, review_name, review_type):
                status_key = f"{review_type}_done"
                
                # Set default status to "Requested" (Red)
                status = "Requested"
                color = "red"
                
                # If session state for the review is set to True, update to Completed (Green)
                if st.session_state.get(status_key, False):
                    status = "Completed"
                    color = "green"
                # If the button was clicked but not yet marked as done, update to Pending (Yellow)
                elif st.session_state.get(f"{review_type}_requested", False):
                    status = "Pending"
                    color = "yellow"
                
                # Layout: One row with three columns
                col1, col2, col3 = st.columns([2, 4, 2])  # Adjusting column sizes for better layout
                
                # Left column: Review Type (Performance, Peer, Self)
                with col1:
                    st.markdown(f"## **{review_name}**")
                
                # Middle column: Status
                with col2:
                    if color == "red":
                        st.error(f"Status: `{status}`")
                    elif color == "yellow":
                        st.warning(f"Status: `{status}`")
                    elif color == "green":
                        st.success(f"Status: `{status}`")
                
                # Right column: Request Button
                with col3:
                    if not st.session_state.get(f"{review_type}_requested", False):
                        if st.button(f"Request {review_name}", key=f"{employee_id}_{review_type}_button"):
                            st.session_state[f"{review_type}_requested"] = True
                            st.session_state[status_key] = False
                            st.rerun()  # Rerun to update the status immediately

            review_types = [
                ("Performance Review", "performance"),
                ("Peer Review", "peer"),
                ("Self Assessment", "self")
            ]
        
            for review_name, review_type in review_types:
                review_status(employee, review_name, review_type)

            if st.button("View User Profile"):
                st.write('gonna kms')
                #page2()


    # Right column: Jobs and Submission
    with main_col2:
        with st.container():
            st.title("🧰 Jobs")

            # Text editor for entering jobs
            job_input = st.text_area("Enter Job Description", height=200)

            # Button to display job input (simulating adding job)
            if st.button("Submit Job(s)"):
                if job_input.strip():  # Only show if input is not empty
                    st.success(f"Job added: {job_input.strip()}")
                else:
                    st.error("Please enter a job description before submitting.")


if __name__ == '__main__':
    page1(EMPLOYEE_ID)