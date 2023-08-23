import requests
import os

def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        full_path = os.path.join('./images', file_name)
        with open(full_path, "wb") as file:
            file.write(response.content)
            print(f"Image téléchargée avec succès : {file_name}")
    else:
        print("Échec du téléchargement de l'image.")

