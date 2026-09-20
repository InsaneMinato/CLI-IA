import numpy as np


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


#best_doc = find_best_document(user_input, doc_embeddings)

#messages_with_context = messages + [{"role": "system", "content": "Voici un document qui peut t'aider : " + docs[best_doc]}]
