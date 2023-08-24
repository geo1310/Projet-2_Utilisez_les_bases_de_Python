""" 
Récupère et renvoie la liste de toutes les url des catégories

"""
import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime

def categories(url):
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        categories_url_list = []

        # Vérification de la présence du dossier csv
        folder = "./csv"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Extraction des données
        categories_list_ul = soup.find("ul", class_="nav-list")
        categories_list_a = categories_list_ul.find_all("a")
        for category_a in categories_list_a:
            categories_url_list.append(
                "http://books.toscrape.com/" + category_a.get("href")
            )
        categories_url_list.pop(0)
    else:
        print("La requete a échouée avec le code : ", page.status_code)
        return False

    return categories_url_list


if __name__ == "__main__":
    os.system("cls")
    print("\nCréation d'un fichier CSV avec la liste des catégories.")
    url = "http://books.toscrape.com/index.html"
    categories_list = categories(url)
    if categories_list != False:
        # Enregistrement du fichier csv
        # Définition du nom du fichier csv
        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
        csv_file = f"liste_categories_{timestamp}.csv"
        # Ecriture du fichier csv
        full_path = os.path.join("./csv", csv_file)
        with open(full_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # les en-têtes
            headers = ["categories_urls"]
            writer.writerow(headers)
            # les données
            for category in categories_list:
                data = [category]
                writer.writerow(data)
        print("\nFichier CSV enregistré avec succès : " + csv_file + "\n")
