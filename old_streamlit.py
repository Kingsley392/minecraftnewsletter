import streamlit as st
import pyrebase
import firebase_admin
import json
from firebase_admin import credentials, firestore
from firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "minecraft-newsletter-firebase-adminsdk-fbsvc-2c3ad50e90.json")
    firebase_admin.initialize_app(cred)
database = firestore.client()

st.title("Your local minecraft newsletter")
if "user" in st.session_state:

    page = st.sidebar.radio("G to", ["Home", "Server news", "Kill logs", "rules",
                            "server list", "members", "settings", "createnews"], key="main_nav_radio")
    if page == "Home":
        from page import Home
    elif page == "Server news":
        from page import servernews
        servernews.show
    elif page == "Kill logs":
        from page import killlogs
        killlogs.show()
    elif page == "members":
        from page import members
        members.show()
    elif page == "rules":
        from page import rules
        rules.show()
    elif page == "settings":
        from page import settings
        settings.show(database)
    elif page == "server list":
        from page import serverlist
        serverlist.show()
    elif page == "createnews":
        from page import create_news
        create_news.show(database)

else:
    choice = st.sidebar.selectbox("Login/signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if choice == "Signup":
        username = st.text_input("username")
        serverIP = st.text_input("Server IP")
        servercode = st.text_input("Server Code")
        minecraftversion = st.text_input("Minecraft version")
        memberinfo = st.text_input(
            "Give us some general info about the memebers in your server")
        if st.button("Create Account"):
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)
                st.success("Account created successfully")
                database.collection("users").document(user['localId']).set({
                    "email": email,
                    "username": username,
                    "serverIP": serverIP,
                    "servercode": servercode,
                    "minecraftversion": minecraftversion,
                    "memberinfo": memberinfo,
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

    # username
    # server ip
    # server code
    # members
    # general info about members
    # minecraft version
