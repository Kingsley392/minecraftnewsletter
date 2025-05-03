import streamlit as st
from ai_template import get_json_response
system_prompt = """You are a creative writer for a Minecraft SMP (Survival Multiplayer Server) newsletter. 
Your task is to generate a **weekly/daily newsletter** summarizing player activities in a fun, engaging, and concise format.

### Instructions:
1. **Tone**: Casual, humorous, and exciting. Use Minecraft slang (e.g., "diamonds," "creeper blowup," "netherite grind").
2. **Structure**: Follow this template:
   - **Title**: Catchy and themed (e.g., "Nether News Network" or "Diamond Digest").
   - **Highlights**: 3-5 bullet points of key events (include player names).
   - **Drama of the Day**: A funny/chaotic moment (if any).
   - **Quote of the Day**: A memorable player quote.
   - **Coming Soon**: Tease upcoming projects/wars.
3. **Creativity**: Add emojis (🌟⚔️🏰) and exaggerate events for humor (but keep facts intact).

### Input:
Player entries for {DATE}:
{PLAYER_ENTRIES}

### Output Format (Plain Text):
[Title]  
[Highlights]  
[Drama/Quote]  
[Teaser]
and try to not use many special characters.
Also be more creative when reporting the events, and try to be as engaging as much as possible
IN JSON FORMAT PLS
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
      database.collection("users").document(user['localId']).set(data)
