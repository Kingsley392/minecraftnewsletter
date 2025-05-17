import streamlit as st
import auth


def show():
    if auth.is_authenticated():
        st.title("🏠 Home")
        st.write(f"Hello, {st.session_state.get('username', 'User')}!")
        st.write("Welcome to your SMP newsletter.")

    else:
        st.warning("Please login to view the Home page.")
        auth.show_login_signup_form()


show()
