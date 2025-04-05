import streamlit as st

st.title("Two-Column Layout Demo")

# Create two columns
left_col, right_col = st.columns(2)

# Left side content
with left_col:
    st.header("Left Side")
    st.write("This is the content on the left side.")
    st.button("Left Button")

# Right side content
with right_col:
    st.header("Right Side")
    st.write("This is the content on the right side.")
    st.button("Right Button")