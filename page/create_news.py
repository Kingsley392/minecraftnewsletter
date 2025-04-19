import streamlit as st
def show(database):
   news = st.text_area('Enter what you did today.(Things that you do not want players to know will be refered as a "secert"')
   if st.button("Submit"):
      data = {
         "userData": {
            "news": news 
         }
      }
      user = st.session_state['user']
      database.collection("users").document(user['localId']).set(data)