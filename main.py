import requests
from bs4 import BeautifulSoup

url = " http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
# Voir le code html source
print(page.content)
