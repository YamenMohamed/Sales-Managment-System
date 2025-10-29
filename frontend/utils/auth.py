import streamlit as st

def save_login(user_data, token):
    """Save user and token to session state."""
    st.session_state.user = user_data
    st.session_state.token = token

def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None

def is_admin():
    user = st.session_state.get("user")
    return user and user.get("role") == "admin"

def logout():
    """Clear session and refresh."""
    for key in ["user", "token"]:
        st.session_state.pop(key, None)
    st.success("Logged out successfully!")
    st.rerun()
