from flask import Flask, request, jsonify, Response
import ollama
import google.generativeai as genai
from dotenv import load_dotenv
from eng_to_arabic import EngToArabic
from eng_to_arabic import ArabicToEng
import asyncio
import os
# ollama.pull('llama3.2:1b')
app = Flask(__name__)
load_dotenv()
GEMINI_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API)
# Dictionary to store conversation history for each user
user_histories = {}

def chat(msg, user_id, language):
    
    # Construct the prompt for Gemini
    prompt = """You are an experienced advocate that knows about every policy 
     and can easily list down the errors by seeing the policies given by users. 
    Be professional and polite to users while talking. Greet everyone if they say hello or hi and introduce yourself if anyone 
    asks about you."""

    # Initialize chat history for the user if it doesn't exist
    if user_id not in user_histories:
        user_histories[user_id] = []

    # Add the user's message to the history
    user_histories[user_id].append({"role": "user", "parts": [msg]})  # Changed for Gemini API

    # Get response from Gemini
    model = genai.GenerativeModel('gemini-2.0-flash') # Choose your model, experiment with 1.5 pro too
    # For the Gemini API, you might want to create a new chat session for each call to chat()
    chat_session = model.start_chat(history=user_histories[user_id]) # Use current history

    response = chat_session.send_message(prompt)  # Send the prompt directly

    message = response.text  # Extract the text from the Gemini response

    # Add the AI's response to the history. Gemini expects a specific format
    user_histories[user_id].append({"role": "model", "parts": [message]}) # Changed for Gemini API

    if language == "arabic":
        async def main(policy):
            engtoarabic = EngToArabic()
            return await engtoarabic.translate(policy)
        translated_message = asyncio.run(main(message))
        print(translated_message)
        return {"reply": translated_message}

    return {"reply": message}

@app.route('/chat', methods=['POST'])
def policy_chat():
    data = request.get_json()
    user_id = data.get('user_id')  # Unique identifier for the user
    msg = data.get('msg')
    language = data.get('language')

    if language == "arabic":
            async def main(policy):
                arabictoenglish = ArabicToEng()
                return await arabictoenglish.translate(policy)
            msg = asyncio.run(main(msg))
    reply = chat(msg,user_id,language)
    return jsonify(reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)
