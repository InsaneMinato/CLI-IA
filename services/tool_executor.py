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