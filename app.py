import openai
import streamlit as st
import pyperclip

st.title("ChatGPT-like ChatBot")

# API key input with security and error handling
api_key = st.text_input("Enter your OpenAI API key:", type="password")
if api_key:
    try:
        openai.api_key = api_key
        openai.Completion.create(model="text-davinci-003", prompt="Hello world")  # Test API key
        st.success("API key is valid.")
    except openai.error.OpenAIError as e:
        st.error("Invalid API key:", e)
        openai.api_key = None  # Clear API key if invalid

if openai.api_key:  # Proceed only if API key is valid
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    tabs = st.tabs(["Chat", "Copy Responses"])

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

    with tabs["Copy Responses"]:
        all_response_messages = "\n\n".join(
            [m["content"] for m in st.session_state.messages if m["role"] == "assistant"]
        )
        if st.button("Copy All Responses"):
            pyperclip.copy(all_response_messages)
            st.success("Responses copied to clipboard!")
else:
    st.error("Please enter a valid OpenAI API key to use the chatbot.")
