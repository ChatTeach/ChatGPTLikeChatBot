import openai
import streamlit as st
import pyperclip  # Import pyperclip

st.title("ChatGPT-like ChatBot")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

tabs = st.tabs(["Chat", "Copy Responses"])  # Create tabs

with tabs["Chat"]:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Prompt and generate response
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tabs["Copy Responses"]:  # Code for copying responses
    all_response_messages = "\n\n".join(
        [m["content"] for m in st.session_state.messages if m["role"] == "assistant"]
    )  # Collect only assistant responses
    if st.button("Copy All Responses"):
        pyperclip.copy(all_response_messages)
        st.success("Responses copied to clipboard!")
