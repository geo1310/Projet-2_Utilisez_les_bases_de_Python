"""
Extraction de données sur le site http://books.toscrape.com/index.html

Menu d'utilisation des differents scripts :
1- Extraire les donnees d'un livre
2- Extraire les donnees de tous les livres d'une catégorie
3- Extraire les donnees de tous les livres et de toutes les categories
4- Quitter

"""
import os
import csv
from datetime import datetime
from book_infos import book_infos
from category_books import category_books



menu = [1, 2, 3, 4]
menu_choice = ""
while menu_choice not in menu:
    os.system("cls")
    print(
        """
    Menu d'utilisation des differents scripts :

    1- Extraire les donnees d'un livre
    2- Extraire les donnees de tous les livres d'une catégorie
    3- Extraire les donnees de tous les livres et de toutes les categories
    4- Quitter

    """)

    menu_choice = input(" Quel est votre choix :")
    match menu_choice:
        # Extraire les données d'un seul livre
        case "1":
            while True:
                print()
                url = input("Entrer Url du Livre : ")
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
                        print()
                        print("Fichier CSV enregistré avec succès : " + csv_file)
                        print()
                        choix_1 = input('Entrer 1 pour une nouvelle requete ou une autre touche pour retourner au menu :')
                        if choix_1 == '1':
                            continue
                        else:
                            break
        # Extraire les donnees de tous les livres d'une catégorie
        case "2":
            while True:
                print()
                url = input("Entrez Url de la Catégorie : ")
                try:
                    books_list = category_books(url)
                except:
                    print("Veuillez entrer une Url Valide !!!")
                else:
                    if books_list != False:
                        # Enregistrement des données de tous les livres de la categorie
                        url_catalogue = "http://books.toscrape.com/catalogue/"

                        # Enregistrement du fichier csv des donnees de tous les livres d'une catégorie
                        # Définition du nom du fichier csv
                        category_name = url.split("/")[-2]
                        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
                        csv_file = f"category_books_data_{category_name}_{timestamp}.csv"

                        # Ecriture du fichier csv
                        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            # Parcours des url des livres de la catégorie
                            headers = None
                            for url_book in books_list:
                                product_page = book_infos(url_catalogue + url_book)
                                # les en-têtes
                                if headers == None:
                                    headers = product_page.keys()
                                    writer.writerow(headers)
                                # les données
                                data = product_page.values()
                                writer.writerow(data)
                        print()
                        print("Fichier CSV enregistré avec succès : " + csv_file)
                        print()
                        choix_2 = input('Entrer 1 pour une nouvelle requete ou une autre touche pour retourner au menu :')
                        if choix_2 == '1':
                            continue
                        else:
                            break
        case "3":
            print("choix 3")
        case "4":
            os.system("cls")
            break
        case _:
            print("Je ne connais pas ce choix !!!")
