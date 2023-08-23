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
from categories_url import categories


menu_choice = ""
while True:
    os.system("cls")
    print(
        """
    Menu d'utilisation des differents scripts :

    1- Extraire les donnees d'un livre
    2- Extraire les donnees de tous les livres d'une catégorie
    3- Extraire les donnees de tous les livres et de toutes les categories
    4- Quitter

    """
    )

    menu_choice = input(" Quel est votre choix :")
    match menu_choice:
        # Extraire les données d'un seul livre
        case "1":
            while True:
                print()
                url = input("Entrer Url du Livre : ")
                if url == '':
                    break
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
                        choix_1 = input(
                            "Entrer 1 pour une nouvelle requete ou une autre touche pour retourner au menu :"
                        )
                        if choix_1 == "1":
                            continue
                        else:
                            break
        # Extraire les donnees de tous les livres d'une catégorie
        case "2":
            while True:
                print()
                url = input("Entrer Url de la Catégorie : ")
                if url =='':
                    break
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
                        csv_file = (
                            f"category_books_data_{category_name}_{timestamp}.csv"
                        )

                        # Ecriture du fichier csv
                        with open(
                            csv_file, mode="w", newline="", encoding="utf-8"
                        ) as file:
                            writer = csv.writer(file)
                            # Parcours des url des livres de la catégorie
                            headers = None
                            index = 1
                            for url_book in books_list:
                                product_page = book_infos(url_catalogue + url_book)
                                # les en-têtes
                                if headers == None:
                                    headers = product_page.keys()
                                    writer.writerow(headers)
                                # les données
                                data = product_page.values()
                                writer.writerow(data)
                                print(
                                    f'{index} - {product_page["title"]} - enregistré.'
                                )
                                index += 1
                        print()
                        print(
                            f"Fichier CSV enregistré avec succès :  {csv_file} avec {index-1} livre(s)."
                        )
                        print()
                        choix_2 = input(
                            "Entrer 1 pour une nouvelle requete ou une autre touche pour retourner au menu :"
                        )
                        if choix_2 == "1":
                            continue
                        else:
                            break
        # Extraire les donnees de tous les livres de toutes les categories
        case "3":
            print()
            print("Récupération de la liste de toutes les catégorie......", end=" ")
            categories_url = categories("http://books.toscrape.com/index.html")
            print(f"{len(categories_url)} catégories récupérées.")

            # Enregistrement du fichier csv des donnees de tous les livres de toutes les catégories
            url_catalogue = "http://books.toscrape.com/catalogue/"
            # Définition du nom du fichier csv
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
            csv_file = f"all_books_data_{timestamp}.csv"
            # Ecriture du fichier csv
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                headers = None
                index = 1
                for categorie in categories_url:
                    books_url = []
                    print()
                    print(
                        f'Récupération de la liste des livres de la catégorie {categorie.split("/")[6]}......',
                        end=" ",
                    )
                    books_url = category_books(categorie)
                    print(f"{len(books_url)} livres récupéré(s)")
                    for url_book in books_url:
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
            print()
            print(
                f"Fichier CSV enregistré avec succès :  {csv_file} avec {index-1} livre(s)."
            )
            print()
            choix_3 = input("Appuyer sur une touche pour retourner au menu :")
            if choix_3:
                continue
        case "4":
            os.system("cls")
            break
        case _:
            print("Je ne connais pas ce choix !!!")
