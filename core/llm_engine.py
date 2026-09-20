from mistralai.client import Mistral

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

messages=[
    {"role": "system", "content": "Tu es un assistant personnel pour un developpeur junior. Réponds en texte brut, sans Markdown, sans astérisques ni tableaux."}
]

messages.append({"role": "user", "content": user_input})

response = client.chat.complete(
    model="mistral-small-latest",
    messages= messages,
    tools=tools
)


