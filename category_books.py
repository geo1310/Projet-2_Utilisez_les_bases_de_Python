""" 
 Récupére la liste des url de tous les livres d'une catégorie et crée un fichier CSV avec leurs données

"""
import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime
from book_infos import book_infos


def category_books(url, url_books_list=None):
    page = requests.get(url)
    if page.status_code == 200:
        category_name = url.split("/")[-2]
        soup = BeautifulSoup(page.content, "html.parser")
        if url_books_list == None:
            url_books_list = []

        # Extraction des données de la premiere page
        image_container = soup.find_all("div", class_="image_container")
        for container in image_container:
            book_href = container.find("a").get("href").replace("../../../", "")
            url_books_list.append(book_href)

        # Vérification de la pagination
        is_next = soup.find("li", class_="next")
        if is_next:
            # Construction de la nouvelle url
            index_url = is_next.find("a").get("href")
            new_url = url.rsplit("/", 1)[0] + "/" + index_url
            category_books(new_url, url_books_list)
        else:
            # Création du fichier CSV
            print(f"\nCréation du fichier CSV pour la catégorie : {category_name}\n")
            # Enregistrement des données de tous les livres de la categorie
            url_catalogue = "http://books.toscrape.com/catalogue/"
            # Enregistrement du fichier csv des donnees de tous les livres d'une catégorie
            # Définition du nom du fichier csv
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
            csv_file = f"liste_livres_{category_name}_{timestamp}.csv"

            # Ecriture du fichier csv
            full_path = os.path.join('./csv', csv_file)
            with open(full_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Parcours des url des livres de la catégorie et écrit les données sur le fichier csv
                headers = None
                index = 1
                for url_book in url_books_list:
                    product_page = book_infos(url_catalogue + url_book)
                    # les en-têtes
                    if headers == None:
                        headers = product_page.keys()
                        writer.writerow(headers)
                    # les données
                    data = product_page.values()
                    writer.writerow(data)
                    print(f'{index} - {product_page["title"]} - enregistré.')
                    index += 1
            print(
                f"\nFichier CSV enregistré avec succès :  {csv_file} avec {index-1} livre(s).\n"
            )
    else:
        print("\nLa requete a échouée avec le code : ", page.status_code, "\n")
        return False

    return True


if __name__ == "__main__":
    os.system("cls")
    while True:
        url = input("Entrer Url de la Catégorie ( vide pour quitter): ")
        if url == "":
            break
        try:
            category_books(url)
        except:
            print("\nVeuillez entrer une Url Valide !!!\n")
