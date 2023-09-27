pip install --upgrade pip
import streamlit as st
from streamlit_chat import message
from embedchain import OpenSourceApp

# Create a Streamlit app title and description
st.title("Online Resources ChatBot:books:")
st.write("Enter multiple URL links and ask questions to the embedded data.")

#initialize the opensourceApp instance
zuck_bot = OpenSourceApp()

#get user input for URLs
num_links = st.number_input("Enter the number of URLs:",min_value=1,value=1,step=1)

url_inputs = []
for i in range(num_links):
    url = st.text_input(f"Enter URL {i+1}:",key=f'url_{i}')
    url_inputs.append(url)

#add urls to the opensourceApp instance
for url in url_inputs:
    if url:
        zuck_bot.add("web_page",url)

#conversation chat functions:
def conversation_chat(query):
    result = zuck_bot.query(query)
    st.session_state['history'].append((query,result))
    return result

def intialize_session_state():
    if "history" not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about"]
    if "past" not in st.session_state:
        st.session_state['past'] = ['Hey!']

def display_chat_histroy():
    reply_container = st.container()
    container =st.container()
    
    with container:
        with st.form(key='my_form',clear_on_submit=True):
            user_input = st.text_input("Question:",placeholder="Ask me about resources",key='input')
            submit_button = st.form_submit_button(label='send')
        
        if submit_button and user_input:
            output = conversation_chat(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
    
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state["generated"])):
                message(st.session_state['past'][i],is_user=True,key=str(i)+"_user",avatar_style="thumbs")
                message(st.session_state['generated'][i],key=str(i),avatar_style="fun-emoji")
#initialize the session_state
intialize_session_state()

#Display the chat history
display_chat_histroy()

