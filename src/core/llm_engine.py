from ollama import chat
from dotenv import load_dotenv
import os

load_dotenv()


def send_message(messages, tools):
    response = chat(
        model="gemma4:e4b",
        messages= messages,
        tools=tools
    )
    return response.message

