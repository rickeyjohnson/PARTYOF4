import streamlit as st
from peer_review import peer_review_chat
from self_assessment import self_assessment_chat
from performance_review import performance_review_chat  # Import manager review

# Set up the Streamlit app layout
def main():
    st.set_page_config(page_title="Employee Reviews", layout="wide")

    # Add a title to the app
    st.title("Employee Review System")

    # Sidebar navigation with options for Peer Review, Self Assessment, and Manager Review
    with st.sidebar:
        st.header("Select Review Type")
        page = st.radio("Choose a review type:", ["Peer Review", "Self Assessment", "Manager Performance Review"])

    # Display the corresponding page based on the selection
    if page == "Peer Review":
        st.header("Peer Review")
        peer_review_chat()
    elif page == "Self Assessment":
        st.header("Self Assessment")
        self_assessment_chat()
    elif page == "Manager Performance Review":
        st.header("Manager Performance Review")
        performance_review_chat()

def page1():
    if st.button("Page 2"):
        st.session_state.current_page = "page_2"
        st.rerun()
    st.title("Page 1 Content")
    st.write("This is the content of the first page.")
    

def page2():
    if st.button("Page 1"):
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
        with cols[i]:
            st.markdown(f"<div style='text-align: center;'>Job #{i+1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>{job_percentages[i]}%</div>", unsafe_allow_html=True)
            

    

if "current_page" not in st.session_state:
    st.session_state.current_page = "page_1"

if st.session_state.current_page == "page_1":
    page1()
elif st.session_state.current_page == "page_2":
    page2()

if __name__ == '__main__':
    main()