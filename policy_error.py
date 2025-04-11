from flask import Flask, request, jsonify, Response
from openai import OpenAI
from dotenv import load_dotenv
from eng_to_arabic import EngToArabic
from eng_to_arabic import ArabicToEng
import asyncio
import os

# Initialize Flask App
app = Flask(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Dictionary to store conversation history for each user
user_histories = {}

def chat(msg, user_id, language):
    # Construct the prompt for OpenAI
    prompt = """You are an experienced advocate that knows about every policy 
    and can easily list down the errors by seeing the policies given by users. 
    Be professional and polite to users while talking. Greet everyone if they say hello or hi by saying hello and welcome the user and introduce yourself if anyone 
    asks about you. Don't say understood again and again; just give straightforward answers to users like you are talking to them as a professional advocate."""

    # Initialize chat history for the user if it doesn't exist
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": prompt}]
    
    # Add the user's message to the history
    user_histories[user_id].append({"role": "user", "content": msg})

    # Get response from OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the specified model
        store=True,
        messages=user_histories[user_id]
    )

    message = completion.choices[0].message.content

    # Add the AI's response to the history
    user_histories[user_id].append({"role": "assistant", "content": message})

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

    reply = chat(msg, user_id, language)
    return jsonify(reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
