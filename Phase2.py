# Importation des librairies
import os
import requests
from bs4 import BeautifulSoup
import csv

# Phase 2
url_category_fiction = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"


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


# Fonction pour créer un dossier fiction_data si celui-ci n'est pas déjà créer:
def create_folder():
    if not os.path.isdir('product\\fiction_data'):
        os.system('mkdir product\\fiction_data')


# Fonction pour récupérer les URLS de chaque page de la catégorie "Fiction".
def get_url_page(url, heading):
    pages_url = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    current_page = soup.find("li", class_="current")
    if current_page:
        current_pages_number = current_page.text.split()
        number_of_pages = int(current_pages_number[3])
        for i in range(1, number_of_pages + 1):
            url_page = (url.replace("index.html", "page-") + str(i) + ".html")
            pages_url.append(url_page)
    if not current_page:
        pages_url.append(url)
    extract_url_book(pages_url, heading)


# Fonction pour récupérer les URLS de chaque livre de la catégorie "Fiction".
def extract_url_book(url_fiction_page, heading):
    url_book_fiction = []
    for page in url_fiction_page:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')
        item_list = soup.find_all("article", class_="product_pod")
        for item in item_list:
            fiction_url = item.find("h3").a.get("href").replace("../../../", "")
            base_url = "http://books.toscrape.com/catalogue/"
            full_url = (base_url + fiction_url)
            url_book_fiction.append(full_url)
    extract_datas_book(url_book_fiction, heading)
    return url_book_fiction


# Fonction pour récupérer les données de chaque livre de la catégorie "Fiction".
def extract_datas_book(url_book_fiction, heading):
    nbr = 0
    for datas in url_book_fiction:
        nbr = nbr + 1
        page = requests.get(datas)
        soup = BeautifulSoup(page.content, "html.parser")
        datas_book = soup.find_all("td")
        product_page_url = datas
        universal_product_code = datas_book[0].text
        title = soup.find("h1").text
        price_including_tax = datas_book[3].text
        price_excluding_tax = datas_book[2].text
        number_available = datas_book[5].text
        product_description = soup.select_one("article > p").text
        category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
        review_rating = soup.find("p", class_="star-rating").get("class")[1]
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
        create_csv_file(fiction_book, category, heading)
        extract_img_product(title, image)


# Fonction pour créer un fichier csv, et y enregistrer les données du livre.
def create_csv_file(fiction_book, category, heading):
    with open('product\\fiction_data\\' + category + '.csv', 'a') as fichier_csv:
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
def extract_img_product(title, url):
    if not os.path.isdir('product\\fiction_data\\fiction_img'):
        os.system('mkdir product\\fiction_data\\fiction_img')
    f = open('product\\fiction_data\\fiction_img\\' + title.replace(":", "").replace("/", " ").replace('"', '').replace(
        'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "") + ".jpg", 'wb')
    print(f)
    reponse_img = requests.get(url)
    f.write(reponse_img.content)
    f.close()


create_folder()
get_url_page(url_category_fiction, heading)
