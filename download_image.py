import requests
import os

def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        # Vérification de la présence du dossier images
        folder = './images'
        if not os.path.exists(folder):
            os.makedirs('./images')
            
        full_path = os.path.join(folder, file_name)
        with open(full_path, "wb") as file:
            file.write(response.content)
            print(f"\nImage téléchargée avec succès : {file_name}")
    else:
        print("\nÉchec du téléchargement de l'image.")

if __name__ == "__main__":
    os.system("cls")
    while True:
        url = input("Entrer Url de l'image à télécharger (vide pour quitter): ")
        if url == "":
            break
        try:
            product_page = download_image(url, 'test.jpg')
        except:
            print("\nVeuillez entrer une Url Valide ou echec de la requete !!!\n")
        

