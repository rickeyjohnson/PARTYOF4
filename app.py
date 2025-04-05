import streamlit as st
from employee_db import create_employee, get_employee
from reviews.performance_review import performance_review_chat
from reviews.self_assessment import self_assessment_chat
from reviews.peer_review import peer_review_chat
from fake_ai_api import generate_employee_profile_summary

EMPLOYEE_ID = "12345"


def init_employee():
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


def show_sidebar():
    page = st.sidebar.radio("Go to", ["🏠 Home", "👨‍💼 Performance Review", "🧠 Self Assessment", "🤝 Peer Review"])
    page_map = {
        "🏠 Home": "home",
        "👨‍💼 Performance Review": "performance_review",
        "🧠 Self Assessment": "self_assessment",
        "🤝 Peer Review": "peer_review"
    }
    if st.session_state.get("current_page") != page_map[page]:
        st.session_state.current_page = page_map[page]
        st.rerun()


def home_page():
    st.title("Employee Evaluation")

    # "Go to Job Matches" button
    if st.button("Job Recommendations"):
        st.session_state.current_page = "page_2"
        st.rerun()

    # Create two columns
    left_col, right_col = st.columns(2)

    # Left side content
    with left_col:
        st.header("Employee Info")
        st.write("Performance/Project Evaluation | **Status:** " + 
                 ("✅ Complete" if st.session_state.get("performance_done") else "❌ Incomplete"))
        st.write("Peer Reviews | **Status:** " + 
                 ("✅ Complete" if st.session_state.get("peer_done") else "❌ Incomplete"))
        st.write("Self Assessment | **Status:** " + 
                 ("✅ Complete" if st.session_state.get("self_done") else "❌ Incomplete"))

    # Right side content
    with right_col:
        st.header("Job Openings")
        message = st.text_area("Write your message here. Include skills likely needed for the role:")
        st.button("Submit")  # You can later add a function to handle this

    # Centered button for evaluation generation
    left, center, right = st.columns([1, 2, 1])
    with center:
        if st.button("Generate Evaluation"):
            st.session_state.current_page = "page_2"
            st.rerun()

    # Final summary if all reviews are complete
    all_complete = st.session_state.get("performance_done", False) and \
                   st.session_state.get("self_done", False) and \
                   st.session_state.get("peer_done", False)

    if all_complete:
        st.success("✅ All reviews completed!")
        st.markdown("### 📄 Full Review Summary")

        combined_responses = {
            "performance_review": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("performance_responses", {}).items()]),
            "self_assessment": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("self_assessment_responses", {}).items()]),
            "peer_review": "\n".join([f"{q}: {a}" for q, a in st.session_state.get("peer_responses", {}).items()])
        }

        employee_profile = get_employee(EMPLOYEE_ID)

        employee_summary = generate_employee_profile_summary(
            employee_profile,
            combined_responses['performance_review'],
            combined_responses['self_assessment'],
            combined_responses['peer_review']
        )

        st.text_area("Employee Comprehensive Summary", employee_summary, height=400)
    else:
        st.info("Please complete all 3 reviews using the sidebar.")


def self_assessment_page():
    self_assessment_chat(EMPLOYEE_ID)


def peer_review_page():
    peer_review_chat(EMPLOYEE_ID)


def performance_review_page():
    performance_review_chat(EMPLOYEE_ID)


def main():
    init_employee()
    show_sidebar()

    page = st.session_state.get("current_page", "home")

    if page == "home":
        home_page()
    elif page == "performance_review":
        performance_review_page()
    elif page == "self_assessment":
        self_assessment_page()
    elif page == "peer_review":
        peer_review_page()


if __name__ == '__main__':
    main()