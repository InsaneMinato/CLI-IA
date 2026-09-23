from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def send_message(messages, tools):
    response = client.chat.complete(
        model="mistral-small-latest",
        messages= messages,
        tools=tools
    )
    reply = response.choices[0].message
    return reply.copy()


