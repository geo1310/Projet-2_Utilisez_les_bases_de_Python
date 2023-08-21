""" 
 Récupération de tous les livres d'une catégorie 

"""
import requests
from bs4 import BeautifulSoup


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
    books_list = category_books(
        "http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
    )
    for url_book in books_list:
        print(url_book)
