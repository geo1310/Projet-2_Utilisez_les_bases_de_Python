""" 
 Récupération de tous les livres d'une catégorie 

"""
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def category_books(url, url_books_list=None):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")

        if url_books_list == None:
            url_books_list = []

        # Extraction des données de la premier page
        image_container = soup.find_all("div", class_="image_container")
        for container in image_container:
            book_href = container.find("a").get("href").replace("../../../", "")
            url_books_list.append(book_href)

        # Vérification de la pagination
        is_next = soup.find("li", class_="next")
        if is_next:
            # Construction de la nouvelle url
            index_url = is_next.find("a").get("href")
            new_url = url.rsplit("/", 1)[0] + '/' + index_url
    
            category_books(new_url, url_books_list)

    else:
        print("La requete a échouée avec le code : ", page.status_code)

    return url_books_list


if __name__ == "__main__":
    url = input('Entrez Url de la Catégorie : ')
    category_name = url.split("/")[-2]
    books_list = category_books(url)
    
    # Enregistrement du fichier csv
    # Définition du nom du fichier csv
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    csv_file = f"category_books_list_{category_name}_{timestamp}.csv"
    # Ecriture du fichier csv
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        # les en-têtes
        headers = [category_name]
        writer.writerow(headers)
        # les données
        for url_book in books_list:
            data = [url_book]
            writer.writerow(data)
    print("Fichier CSV enregistré avec succès : " + csv_file)
    
    
    
    
    
