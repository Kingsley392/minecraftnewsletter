import streamlit as st
import pyrebase
import firebase_admin
import json
from firebase_admin import credentials, firestore
from firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    cred = credentials.Certificate("/workspaces/minecraftnewsletter/minecraft-newsletter-firebase-adminsdk-fbsvc-1960b1509e.json")
    firebase_admin.initialize_app(cred)
database = firestore.client()

st.title("Your local minecraft newsletter")
choice = st.sidebar.selectbox("Login/signup", ["Login", "Signup"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")
if choice == "Signup":
    username = st.text_input("username")
    members = st.text_input("members")
    serverIP = st.text_input("Server IP")
    servercode = st.text_input("Server Code")
    minecraftversion = st.text_input("Minecraft version")
    memberinfo = st.text_input("Give us some general info about the memebers in your server")
    if st.button("Create Account"):
      try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success("Account created successfully")
        database.collection("users").document(user['localId']).set({
          "email": email,
          "username": username,
          "members": members,
          "serverIP": serverIP,
          "servercode":servercode,
          "minecraftversion":minecraftversion,
          "memberinfo":memberinfo,
        })
      except Exception as e:
        st.error(f"Error: {e}")

elif choice == "Login":
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login Successful!")
            st.session_state['user'] = user
        except Exception as e:
            st.error(f"Error: {e}")
if "user" in st.session_state:
    st.subheader("Welcome!")
    user = st.session_state['user']
    user_info = database.collection("users").document(user['localId']).get().to_dict()
    st.write(f"Username: {user_info['username']}")
    st.write(f"Email: {user_info['email']}")
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.success("Logged out successfully.")
        st.rerun()



#username
#server ip
#server code
#members
#general info about members
#minecraft version