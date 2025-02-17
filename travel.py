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