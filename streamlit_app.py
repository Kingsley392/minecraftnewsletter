import streamlit as st
import auth
from firebase_utils import initialize_firebase

auth_instance, database_instance = initialize_firebase()

# --- Authentication Logic ---
if not auth.is_authenticated():
    st.title("Welcome to the minecraft newsletter!")
    st.info("Please login or sign up to continue.")
    auth.show_login_signup_form()
else:
    # --- Authenticated App Content ---
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Welcome, {st.session_state.get('username', 'User')}!")
    if st.sidebar.button("Logout"):
        auth.logout()

st.title("The SMP Newsletter App")
st.write("This app is supposed to help unite your server together through a serverwide newsletter. Users can input thier " \
"own shenanigans in the app, and it would create a newsletter with everyone's shennanigans. This app is supposed to be" \
"used for small servers with friends. Not meant for server giants. ")
