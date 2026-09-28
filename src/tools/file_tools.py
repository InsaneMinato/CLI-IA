

import os
from pathlib import Path


def _resolve_file_path(file_path):
    if not isinstance(file_path, (str, os.PathLike)):
        raise TypeError("Le chemin du fichier doit être une chaîne de caractères.")

    raw_path = os.fspath(file_path).strip()
    if not raw_path:
        raise ValueError("Le chemin du fichier ne peut pas être vide.")

    if raw_path.startswith("~") and not raw_path.startswith("~/"):
        raw_path = f"~/{raw_path[1:]}"

    path = Path(os.path.expanduser(raw_path))
    if not path.is_absolute():
        parts = path.parts
        if parts and parts[0].casefold() in {
            "Desktop",
            "Documents",
            "Downloads",
            "Music",
            "Pictures",
            "Videos",
        }:
            path = Path.home() / path
        else:
            path = Path.cwd() / path

    if path.exists():
        return path

    current = Path(path.anchor)
    for part in path.parts[1:]:
        candidate = current / part
        if candidate.exists():
            current = candidate
            continue
        if not current.is_dir():
            return path
        matches = [entry for entry in current.iterdir() if entry.name.casefold() == part.casefold()]
        if len(matches) != 1:
            return path
        current = matches[0]
    return current


def get_file_content(file_path):
    try:
        resolved_path = _resolve_file_path(file_path)
        with open(resolved_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return f"Erreur : {str(e)}"

def modify_file_content(file_path, old_content, new_content):
    try:
        resolved_path = _resolve_file_path(file_path)
        if not isinstance(old_content, str) or not isinstance(new_content, str):
            raise TypeError("Les contenus à remplacer doivent être des chaînes de caractères.")

        with open(resolved_path, "r", encoding="utf-8") as f:
            content = f.read()

        if old_content == "":
            updated_content = new_content
        else:
            if old_content not in content:
                return f"Erreur : le texte à remplacer n'existe pas dans le fichier {file_path}."
            updated_content = content.replace(old_content, new_content)

        with open(resolved_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return f"Contenu du fichier {file_path} modifié avec succès."
    except FileNotFoundError:
        return f"Erreur : Le fichier {file_path} n'existe pas."
    except Exception as e:
        return f"Erreur : {str(e)}"
