import json
import shlex
from tools import execute_command, get_file_content, modify_file_content, get_current_time

def get_tools ():
    return [
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
        {
            "type": "function",
            "function": {
                "name": "execute_shell_command",
                "description": "Exécute une commande shell et retourne la sortie.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "La commande à exécuter. Seules touch, ls et mkdir sont autorisées, avec au plus un chemin en argument."
                        }
                    },
                    "required": ["command"]
                }
            }
        }
    ]

def tool_call(reply):
    if not reply.tool_calls:
        raise ValueError("Le message ne contient aucun appel d'outil.")

    tool_call = reply.tool_calls[0]
    tool_name = tool_call.function.name
    arguments = tool_call.function.arguments

    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    print("Le modèle veut appeler :", tool_name)

    if tool_name == "get_current_time":
        result = get_current_time()
    elif tool_name == "get_file_content":
        file_path = arguments.get("file_path")
        result = get_file_content(file_path)
    elif tool_name == "modify_file_content":
        file_path = arguments.get("file_path")
        old_content = arguments.get("old_content")
        new_content = arguments.get("new_content")

        result = modify_file_content(file_path, old_content, new_content)
    elif tool_name == "execute_shell_command":
        command = arguments.get("command")
        if not isinstance(command, str):
            raise ValueError("La commande shell doit être une chaîne de caractères.")
        try:
            command_parts = shlex.split(command)
        except ValueError as error:
            raise ValueError(f"Commande shell invalide : {error}") from error

        if not command_parts or command_parts[0] not in {"touch", "ls", "mkdir"}:
            raise ValueError(f"Commande shell non autorisée : {command}")
        if len(command_parts) > 2:
            raise ValueError(f"Commande shell non autorisée : {command}")
        result = execute_command(command_parts[0], *command_parts[1:])
    else:
        raise ValueError(f"Outil inconnu : {tool_name}")

    return result