import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def chat_with_bot(user_input):
    # Define the chatbot's role and instructions
    messages = [
        {"role": "system", "content": "You are a travel assistant. Help users book tickets and recommend travel experiences."},
        {"role": "user", "content": user_input}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the chatbot's reply
    bot_reply = response['choices'][0]['message']['content']
    return bot_reply

# Next

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
    
    
# Next

def chat_with_bot(user_input):
    messages = [
        {"role": "system", "content": "You are a travel assistant. Help users book tickets and recommend travel experiences."},
        {"role": "user", "content": user_input}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the chatbot's reply
    bot_reply = response['choices'][0]['message']['content']

    # Add ticket booking and experience recommendations
    if "book" in user_input.lower() or "ticket" in user_input.lower():
        bot_reply += "\n\nYou can book tickets on platforms like Expedia, Skyscanner, or Kayak."
    if "experience" in user_input.lower() or "visit" in user_input.lower():
        bot_reply += "\n\nHere are some popular experiences you might enjoy: [Local Tours], [Museums], [Adventure Activities]."

    return bot_reply