import streamlit as st

# Set up the Streamlit app
st.title("AI Travel Assistant")
st.write("Welcome to the AI Travel Assistant! Chat with me to book tickets and get travel recommendations.")

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    st.write(f"{message['role']}: {message['content']}")

# User input
user_input = st.text_input("Type your message here:")

if user_input:
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "You", "content": user_input})

    # Get chatbot response
    bot_response = chat_with_bot(user_input)

    # Add chatbot response to chat history
    st.session_state.chat_history.append({"role": "Travel Assistant", "content": bot_response})

    # Clear the input box
    st.experimental_rerun()