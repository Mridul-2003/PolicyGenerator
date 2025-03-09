# import gradio as gr
# import ollama
# import google.generativeai as genai
# from dotenv import load_dotenv
# GEMINI_API = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=GEMINI_API)
# def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
#     chat_history = [{"role": "model", "content":system_prompt}]
#     for query, response in history:
#         chat_history.append({"role": "user", "content": query})
#         chat_history.append({"role": "assistant", "content": response})  
#     chat_history.append({"role": "user", "content": msg})
#     return chat_history

# def generate_response(msg: str, history: list[list[str, str]], system_prompt: str):
#     chat_history = format_history(msg, history, system_prompt)
#     response = ollama.chat(model='llama3.2:1b', stream=True, messages=chat_history)
#     message = ""
#     for partial_resp in response:
#         token = partial_resp["message"]["content"]
#         message += token
#         yield message

# chatbot = gr.ChatInterface(
#                 generate_response,
#                 additional_inputs=[
#                     gr.Textbox(
#                         """
# you are an experienced advocate that knows about every policy and can easily
# list down the errors by seeing the policies given by users.Be professional and 
# polite to users while talking.
# """,
#                         label="System Prompt"
#                     )
#                 ],
#                 title="LLama-3 Chatbot using 'Ollama'",
#                 description="Feel free to ask any question.",
#                 theme="soft"
# )

# chatbot.launch(share=True)

import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file (if any)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables.")
    exit()  # Or handle the error more gracefully

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Or 'gemini-pro', or the model of your choice

def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = [system_prompt] # System Prompt
    for query, response in history:
        chat_history.append(f"User: {query}")
        chat_history.append(f"Assistant: {response}")
    chat_history.append(f"User: {msg}")
    return "\n".join(chat_history) # Join as a single string for Gemini

def generate_response(msg: str, history: list[list[str, str]], system_prompt: str):
    formatted_prompt = format_history(msg, history, system_prompt)
    chat = model.start_chat(history=[]) # You can initialize with a system prompt too, as a role="user" message with the system prompt as content
    response = chat.send_message(formatted_prompt, stream=True)  # Pass the entire formatted prompt

    message = ""
    for chunk in response:
        message += chunk.text
        yield message


chatbot = gr.ChatInterface(
    generate_response,
    additional_inputs=[
        gr.Textbox(
            """
you are an experienced advocate that knows about every policy and can easily
list down the errors by seeing the policies given by users.Be professional and 
polite to users while talking.
""",
            label="System Prompt"
        )
    ],
    title="Gemini Chatbot",
    description="Feel free to ask any question.",
    theme="soft"
)

chatbot.launch(share=True,server_port=7860)
