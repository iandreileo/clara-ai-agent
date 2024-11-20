import streamlit as st
import uuid
import os

st.title("AI Agent for resume building")

# generate an unique user token
if "user_token" not in st.session_state:
    st.session_state.user_token = str(uuid.uuid4())

# conversation id should persist across reruns
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        import requests

        api_url = "http://localhost:8000/api/v1/chat"
        payload = {
            "message": prompt,
            "conversation_id": st.session_state.conversation_id,
        }
        headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            stream = response.json().get("response", "No response from assistant")

            os.write(1, f"{stream}\n".encode()) 
            os.write(1, f"{st.session_state.conversation_id}\n".encode()) 
        else:
            stream = "Error: Unable to get response from assistant"

        response = st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": stream})
