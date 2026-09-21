

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

