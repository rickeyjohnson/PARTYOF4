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

if __name__ == '__main__':
    main()
