# Importation des librairies
import os
import requests
from bs4 import BeautifulSoup
import csv

# Phase 1
url_fiction_book = "http://books.toscrape.com/catalogue/william-shakespeares-star-wars-verily-a-new-hope-william-shakespeares-star-wars-4_871/index.html"

# Création d'une liste pour les en-têtes:
heading = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]
# Création du dossier book_data si celui-ci n'est pas déjà créer:
if not os.path.isdir('product\\book_data'):
    os.system('mkdir product\\book_data')

# Fonction pour récupérer les données d'un livre.
def extract_datas_book(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    datas_book = soup.find_all("td")
    product_page_url = url
    universal_product_code = datas_book[0].text
    title = soup.find("h1").text
    price_including_tax = datas_book[3].text
    price_excluding_tax = datas_book[2].text
    number_available = datas_book[5].text
    product_description = soup.select_one("article > p").text
    category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
    review_rating = soup.find("p", class_="star-rating").get("class")[1] + " in five"
    base_url = "http://books.toscrape.com/"
    image_url = soup.find("div", class_="item active").find("img").get("src")
    image = (base_url + image_url).replace("../../", "")

    # On créer un dictionnaire pour chaque livre:
    fiction_book = {
        "product_page_url": product_page_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image
    }
    print(fiction_book)

    # On appelle les fonctions create_csv_file et extract_img_product:
    create_csv_file(fiction_book, heading)
    extract_img_product(category, image)

# Fonction pour créer un fichier csv, et y enregistrer les données du livre.
def create_csv_file(fiction_book, heading):
    with open('product\\book_data\\' + fiction_book["category"] + '.csv', 'w')as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(heading)
        writer.writerow([
            fiction_book["product_page_url"],
            fiction_book["universal_product_code"],
            fiction_book["title"],
            fiction_book["price_including_tax"],
            fiction_book["price_excluding_tax"],
            fiction_book["number_available"],
            fiction_book["product_description"],
            fiction_book["category"],
            fiction_book["review_rating"],
            fiction_book["image_url"]
        ])

# Fonction pour télécharger les images à partir de leurs URLS:
def extract_img_product(category, url):
    f = open('product\\book_data\\' + category + '.jpg', 'wb')
    reponse_img = requests.get(url)
    f.write(reponse_img.content)
    f.close()

# On apelle la fonction extract_datas_book pour lancer le script:
extract_datas_book(url_fiction_book)

