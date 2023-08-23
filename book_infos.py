""" 
Récupération des données sur une page produit

"""
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime


def book_infos(url):

    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        product_page = {}

        # Extraction des données

        # Titre
        product_title = soup.h1.string

        # Description
        product_description_prev = soup.find(id="product_description")
        if product_description_prev != None:
            product_description = product_description_prev.find_next_sibling().string
        else:
            product_description = ""

        # Image_Url
        image_div = soup.find(class_="item active")
        image_url = image_div.find("img").get("src")

        # Catégorie
        category_ul = soup.find("ul", class_="breadcrumb")
        category_li = category_ul.find_all("li")
        category = category_li[2].find("a").string

        # Enregistrement du tableau information produit
        product_infos = {}
        product_table = soup.find("table", class_="table-striped")
        rows = product_table.find_all("tr")
        for row in rows:
            table_th = row.find("th")
            table_td = row.find("td")
            if table_th and table_td:
                product_infos[table_th.string] = table_td.string

        # Enregistrement des donnees du produit
        product_page["product_page_url"] = page.url
        product_page["universal_product-code"] = product_infos["UPC"]
        product_page["title"] = product_title
        product_page["price_including_tax"] = product_infos["Price (incl. tax)"]
        product_page["price_excluding_tax"] = product_infos["Price (excl. tax)"]
        product_page["number_available"] = product_infos["Availability"]
        product_page["product_description"] = product_description
        product_page["category"] = category
        product_page["review_rating"] = product_infos["Number of reviews"]
        product_page["image_url"] = image_url

    else:
        print("La requete a échouée avec le code : ", page.status_code)
        return False

    return product_page


if __name__ == "__main__":
    url = input("Entrez Url du Livre : ")
    try:
        product_page = book_infos(url)
    except:
        print("Veuillez entrer une Url Valide !!!")
    else:
        if product_page != False:
            # Enregistrement du fichier csv
            # Définition du nom du fichier csv
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
            csv_file = f"book_infos_{product_page['title'].replace(':', '_').replace(' ', '_').replace(',', '_')}_{timestamp}.csv"
            # Ecriture du fichier csv
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                # les en-têtes
                headers = product_page.keys()
                writer.writerow(headers)
                # les données
                data = product_page.values()
                writer.writerow(data)
            print("Fichier CSV enregistré avec succès : " + csv_file)
