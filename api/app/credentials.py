import json
import os

def load_credentials():
    # Buscamos las credenciales en el .json
    path = os.path.join('app', "credentials.json")
    print(path)
    with open(path, "r") as f:
        return json.load(f)
