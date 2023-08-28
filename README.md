## Installation et activation de l'environnement Virtuel
Ouvrez un nouveau terminal et taper  
```
python -m venv .venv-projet2
```
Selectionner l'environnement virtuel dans visual studio code ou l'activer en se plaçant dans le dossier **venv-projet2/scripts** et taper
```
./activate
```
Installer les dependances necessaires au projet
```
pip install -r requirements.txt
```

Le script principal est main.py permettant d'accéder au menu suivant :

Menu d'utilisation des differents scripts :

    1- Extraire les donnees d'un livre
    2- Extraire les donnees de tous les livres d'une catégorie
    3- Extraire les donnees de tous les livres et de toutes les categories
    4- Quitter

Les modules books_infos.py , categories_url.py, category_books.py et download_image.py sont utilisables independamment afin de realiser des tests.


