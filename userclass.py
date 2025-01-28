# globals.py
import json

# Nom du fichier pour stocker la variable
STATE_FILE = "state.json"

# Charger la valeur de user_globale à partir du fichier
def load_user():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("user_globale", None)  # Retourne None si la clé n'existe pas
    except FileNotFoundError:
        return None  # Si le fichier n'existe pas encore

# Sauvegarder la valeur de user_globale dans le fichier
def save_user(value):
    with open(STATE_FILE, "w") as f:
        json.dump({"user_idg": value}, f)

# Initialisation de la variable globale
user_idg = load_user()
#session 
