from datetime import datetime
import streamlit as st
from ai_template import get_json_response
system_prompt = """
You are an AI content generator for a Minecraft SMP newsletter.

Generate a JSON response in this format:
{{
  "week_start": "will put later",
  "headline": "Fun headline",
  "subheadline": "Week of...",
  "sections": [
    {{
      "title": "...",
      "body": "...",
      "screenshot_category": "optional"
    }},
    ...
  ]
}}

Requirements:
- Casual, funny, and immersive tone.
- Markdown body formatting.
- Include at least 5 sections.
- Add 'screenshot_category' to 2–3 sections from: survival, building, redstone, pvp, farming, mining, exploration, community.

"""
def show(database):
   news = st.text_area('Enter what you did today.(Things that you do not want players to know will be refered as a "secert"')
   if st.button("Submit"):
      user_prompt = ",".join(news)
        
      output = get_json_response(system_prompt, user_prompt)
      st.write(output)
      data = {
         "userData": {
            "news": news 
         }
      }
      user = st.session_state['user']
      entry_ref = database.collection("entries").document()
      entry_ref.set({
        "user_id":user['localId'],
        "email": user['email'],
        "date": datetime.now(),
        "content": news,
        "server_code": user[servercode]
      })
      database.collection("users").document(user['localId']).set(data)
