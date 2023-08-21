import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

url = " http://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"
page = requests.get(url)
product_page = {}

if page.status_code == 200:
    soup = BeautifulSoup(page.content, "html.parser")
    # Extraction des données

    # Titre
    product_title = soup.h1.string

    # Description
    product_description_prev = soup.find(id="product_description")
    product_description = product_description_prev.find_next_sibling().string

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

    # Enregistrement du fichier csv

    # Définition du nom de fichier csv
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file = (
        "product_page_" + product_title.replace(":", " ") + "_" + timestamp + ".csv"
    )
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        # les en-têtes
        headers = product_page.keys()
        writer.writerow(headers)
        # les données
        data = product_page.values()
        writer.writerow(data)

    print("Fichier CSV enregistré avec succès : " + csv_file)

else:
    print("La requete a échouée avec le code : ", page.status_code)
