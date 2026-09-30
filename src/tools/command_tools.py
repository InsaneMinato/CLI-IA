from .file_tools import resolve_file_path
import subprocess

def execute_command(command , *args):
    if command == "touch":
        if len(args) != 1:
            return "Erreur : la commande 'touch' nécessite exactement un argument (le chemin du fichier)."
        file_path = args[0]
        file_path = resolve_file_path(file_path)
        result = run_shell_command("touch", file_path)
        return f"Fichier créé : {result}"
    elif command == "mkdir":
        if len(args) != 1:
            return "Erreur : la commande 'mkdir' nécessite exactement un argument (le chemin du répertoire)."
        dir_path = args[0]
        dir_path = resolve_file_path(dir_path)
        result = run_shell_command("mkdir", dir_path)
        return f"Répertoire créé : {result}"
    elif command == "ls":
        if len(args) > 1:
            return "Erreur : la commande 'ls' ne prend qu'un seul argument (le chemin du répertoire)."
        dir_path = args[0] if args else "."
        dir_path = resolve_file_path(dir_path)
        result = run_shell_command("ls", dir_path)
        return f"Contenu du répertoire : {result}"
    else:
        return f"Erreur : commande inconnue '{command}'."

def run_shell_command(command, *args):
    try:
        result = subprocess.run(
            [command, *map(str, args)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de la commande : {e.stderr}"