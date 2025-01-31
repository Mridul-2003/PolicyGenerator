from flask import Flask, request, jsonify, Response
import ollama
ollama.pull('llama3.2:1b')
app = Flask(__name__)

# Dictionary to store conversation history for each user
user_histories = {}

def chat(msg,user_id):
    # System prompt for AI behavior
    system_prompt = """You are an experienced advocate that knows about every policy 
    and can easily list down the errors by seeing the policies given by users. 
    Be professional and polite to users while talking."""

    # Retrieve user's chat history or create a new one
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": system_prompt}]

    # Add user message to history
    user_histories[user_id].append({"role": "user", "content": msg})

    # Get response from AI model
    response = ollama.chat(model='llama3.2:1b', stream=True, messages=user_histories[user_id])
    
    # Process response
    message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        message += token
        print(message)

    # Add AI response to history
    user_histories[user_id].append({"role": "assistant", "content": message})
    return {"reply":message}
@app.route('/chat', methods=['POST'])
def policy_chat():
    data = request.get_json()
    user_id = data.get('user_id')  # Unique identifier for the user
    msg = data.get('msg')
    return Response(chat(user_id,msg),mimetype="text/event-stream")  # Streaming response

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)
