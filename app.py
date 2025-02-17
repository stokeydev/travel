from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datasets import load_dataset
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)

# Load the DialoGPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Load the Bitext Travel Dataset
try:
    dataset = load_dataset("bitext/Bitext-travel-llm-chatbot-training-dataset")
    print("Bitext dataset loaded successfully.")
except Exception as e:
    print(f"Error loading Bitext dataset: {str(e)}")
    dataset = None

# Load a pre-trained sentence transformer model for semantic similarity
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')


def find_closest_response(user_input):
    if dataset is None:
        return "I'm sorry, but I couldn't load the travel dataset. Please try again later."

    try:
        # Precompute embeddings for all instructions in the dataset
        instructions = [example['instruction'] for example in dataset['train']]
        instruction_embeddings = sentence_model.encode(instructions)

        # Encode the user input
        user_embedding = sentence_model.encode([user_input])

        # Compute cosine similarity between the user input and all instructions
        similarities = cosine_similarity(
            user_embedding, instruction_embeddings)
        closest_index = similarities.argmax()

        # Return the closest response
        return dataset['train'][closest_index]['response']
    except Exception as e:
        print(f"Error finding closest response: {str(e)}")
        return "I'm sorry, but I couldn't find a suitable response. Please try again."


def chat_with_bot(user_input, chat_history_ids=None):
    try:
        # Find the closest response from the Bitext dataset
        closest_response = find_closest_response(user_input)
        print(f"Closest response: {closest_response}")  # Debugging statement

        # Generate a response using DialoGPT
        new_user_input_ids = tokenizer.encode(
            user_input + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids],
                                  dim=-1) if chat_history_ids is not None else new_user_input_ids
        chat_history_ids = model.generate(
            bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        bot_reply = tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"DialoGPT response: {bot_reply}")  # Debugging statement

        # Combine the Bitext response and DialoGPT response
        combined_response = f"{closest_response}\n\n{bot_reply}"

        return combined_response, chat_history_ids
    except Exception as e:
        print(f"Exception: {str(e)}")  # Print the full exception
        return "Sorry, an unexpected error occurred. Please try again.", None

# Serve the HTML file


@app.route("/")
def serve_html():
    return send_from_directory(".", "index.html")

# Chat route


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get the chat history from the session (if any)
    chat_history_ids = request.json.get("chat_history_ids")
    if chat_history_ids:
        chat_history_ids = torch.tensor(
            chat_history_ids)  # Convert back to a tensor

    # Get the bot's response
    bot_response, chat_history_ids = chat_with_bot(
        user_input, chat_history_ids)

    # Convert chat_history_ids to a list for JSON serialization
    chat_history_ids_list = chat_history_ids.tolist(
    ) if chat_history_ids is not None else None

    return jsonify({
        "response": bot_response,
        "chat_history_ids": chat_history_ids_list
    })


if __name__ == "__main__":
    app.run(debug=True)
