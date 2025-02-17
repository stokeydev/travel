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