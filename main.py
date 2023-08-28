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

# Menu
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

    menu_choice = input("Quel est votre choix :")
    match menu_choice:

        # Extraire les données d'un seul livre
        case "1":
            while True:
                url = input("\nEntrer Url du Livre ( vide pour retour au menu ): ")
                if url == "":
                    break
                try:
                    product_page, product_title_file = book_infos(url)
                except:
                    print("Veuillez entrer une Url Valide !!!")
                else:
                    if product_page != False:
                        # Enregistrement du fichier csv
                        # Définition du nom du fichier csv
                        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
                        csv_file = f"livre_{product_title_file}_{timestamp}.csv"
                        # Ecriture du fichier csv
                        full_path = os.path.join("./csv", csv_file)
                        with open(
                            full_path, mode="w", newline="", encoding="utf-8"
                        ) as file:
                            writer = csv.writer(file)
                            # les en-têtes
                            headers = product_page.keys()
                            writer.writerow(headers)
                            # les données
                            data = product_page.values()
                            writer.writerow(data)
                        print(
                            "\nFichier CSV enregistré avec succès : " + csv_file + "\n"
                        )
                        choix_1 = input(
                            "Entrer 1 pour une nouvelle requete ( vide ou autre pour retour au menu) :"
                        )
                        if choix_1 == "1":
                            continue
                        else:
                            break

        # Extraire les donnees de tous les livres d'une catégorie
        case "2":
            while True:
                url = input("\nEntrer Url de la Catégorie ( vide pour quitter): ")
                if url == "":
                    break
                try:
                    category_books(url)
                except:
                    print("\nVeuillez entrer une Url Valide !!!\n")
                choix_2 = input(
                    "Entrer 1 pour une nouvelle requete ( vide ou autre pour retour au menu ) :"
                )
                if choix_2 == "1":
                    continue
                else:
                    break

        # Extraire les donnees de tous les livres de toutes les categories
        
        case "3":
            print("\nRécupération de la liste de toutes les catégorie......", end=" ")
            categories_url = categories("http://books.toscrape.com/index.html")
            print(f"{len(categories_url)} catégories récupérées.")
            print("\nCréation des fichiers CSV pour toutes les catégories.\n")
            for category in categories_url:
                category_books(category)
            choix_3 = input("Appuyer sur une touche pour retourner au menu :")
            if choix_3:
                continue
        case "4":
            os.system("cls")
            break
        case _:
            print("Je ne connais pas ce choix !!!")
