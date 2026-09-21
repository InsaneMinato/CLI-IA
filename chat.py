import os
import numpy as np
from dotenv import load_dotenv
from mistralai.client import Mistral
from datetime import datetime
import sqlite3
from sqlite3 import Error
import json

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

conn = sqlite3.connect("messages.db")

cursor = conn.cursor()

cursor.execute("""
			   CREATE TABLE IF NOT EXISTS messages (
													   id INTEGER PRIMARY KEY AUTOINCREMENT,
													   role TEXT NOT NULL,
													   content TEXT NOnpT NULL,
													   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			   )
			   """)
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables vues par Python :", cursor.fetchall())


tools = [
	{
		"type": "function",
		"function": {
			"name": "get_current_time",
			"description": "Retourne la date et l'heure actuelles",
			"parameters": {
				"type": "object",
				"properties": {},
				"required": []
			}
		}
	},
	{
		"type": "function",
		"function": {
			"name": "get_file_content",
			"description": "Retourne le contenu d'un fichier texte",
			"parameters": {
				"type": "object",
				"properties": {
					"file_path": {
						"type": "string",
						"description": "Le chemin du fichier texte à lire"
					}
				},
				"required": ["file_path"]
			}
		}
	},
	{
		"type": "function",
		"function": {
			"name": "modify_file_content",
			"description": "Modifie le contenu d'un fichier en remplaçant un texte par un autre",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Chemin du fichier à modifier."},
                    "old_content": {"type": "string", "description": "Contenu à remplacer (peut être vide)."},
                    "new_content": {"type": "string", "description": "Nouveau contenu à insérer."}
                },
                "required": ["file_path", "old_content", "new_content"],
            },
        },
    },
]

"""
def load_documents(folder):
	documents = {}
	for filename in os.listdir(folder):

		full_path = os.path.join(folder, filename)

		with open(full_path, "r", encoding="utf-8") as f:
			content = f.read()

		documents[filename] = content
	return documents

def get_embedding(text):
	response = client.embeddings.create(
		model="mistral-embed",
		inputs=[text]
	)
	return response.data[0].embedding

def embed_documents(documents):
	result = {}
	for filename, content in documents.items():
		result[filename] = get_embedding(content)
	return result

def cosine_similarity(vec1, vec2):
	vec1 = np.array(vec1)
	vec2 = np.array(vec2)
	return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_best_document(user_input, doc_embeddings):
	question_embedding = get_embedding(user_input)
	
	similarities = {}
	for filename, vector in doc_embeddings.items():
		similarities[filename] = cosine_similarity(question_embedding, vector)
	
	return max(similarities, key=similarities.get

)

docs = load_documents("docs")
doc_embeddings = embed_documents(docs)

"""


def get_current_time():
	return str(datetime.now())

def get_file_content(file_path):
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			return f.read()
	except Exception as e:
		print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
		return f"Erreur : {str(e)}"

def modify_file_content(file_path, old_content, new_content):
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()

		updated_content = content.replace(old_content, new_content)

		with open(file_path, "w", encoding="utf-8") as f:
			f.write(updated_content)

		return f"Contenu du fichier {file_path} modifié avec succès."
	except FileNotFoundError:
		return f"Erreur : Le fichier {file_path} n'existe pas."
	except Exception as e:
		return f"Erreur : {str(e)}"
		



def save_message(role, content):
	try:
		cursor.execute(
				"INSERT INTO messages (role, content) VALUES (?, ?)",
				(role, content)
			)
		conn.commit()
	except Error as e:
		return f"Erreur : {str(e)}" 
	




try:
	while True:
		user_input = input("> ")
		if user_input == "exit" or user_input == "quit":
			print("À la prochaine !")
			break

		#best_doc = find_best_document(user_input, doc_embeddings)

		messages.append({"role": "user", "content": user_input})
		save_message("user", user_input)

		#messages_with_context = messages + [{"role": "system", "content": "Voici un document qui peut t'aider : " + docs[best_doc]}]

		try:
			response = client.chat.complete(
				model="mistral-small-latest",
				messages= messages,
				tools=tools
			)

			reply = response.choices[0].message
			reply_content = reply.content

			if reply.tool_calls:
				tool_name = reply.tool_calls[0].function.name
				arguments = reply.tool_calls[0].function.arguments
				if isinstance(arguments, str):
					arguments = json.loads(arguments)
				print("Le modèle veut appeler :", tool_name)

				if tool_name == "get_current_time":
					result = get_current_time()

				if tool_name == "get_file_content":
					file_path = arguments.get("file_path")
					result = get_file_content(file_path)

				if tool_name == "modify_file_content":
					file_path = arguments.get("file_path")
					old_content = arguments.get("old_content")
					new_content = arguments.get("new_content")

					result = modify_file_content(file_path, old_content, new_content)


				messages.append(reply)
				save_message("assistant", f"[a demandé l'outil {tool_name}]")
				messages.append({
					"role": "tool",
					"name": tool_name,
					"content": result,
					"tool_call_id": reply.tool_calls[0].id
				})
				response2 = client.chat.complete(
					model="mistral-small-latest",
					messages=messages,
					tools=tools
				)
				final_reply = response2.choices[0].message.content
				messages.append({"role": "assistant", "content": final_reply})
				print("IA : ", final_reply)



			else:
				messages.append({"role": "assistant", "content": reply_content})
				save_message("assistant", reply_content)
				print("IA : ", reply_content)
		except Exception as e:
			print("Erreur, réessaie :", e)
			continue
finally:
	if conn:
		conn.close()
