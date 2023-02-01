# Importation des librairies
import os
import requests
from bs4 import BeautifulSoup
import csv

# Phase 3
url_category = []
name_category = []

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

# Fonction pour créer un dossier category_data si celui-ci n'est pas déjà créer:
def create_folder(list):
    if not os.path.isdir('product\\category_data'):
        os.system('mkdir product\\category_data')
    for name in list:
        str(name)
        if not os.path.isdir('product\\category_data\\' + name):
            os.mkdir('product\\category_data\\' + name)

# Fonction qui vient extraire toutes les urls des catégories de livres disponibles.
def get_all_category():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    nav_list = soup.find_all("ul", class_="nav nav-list")
    for li in nav_list:
        category = li.find_all("li")
        for link in category:
            a = link.find("a")
            link_category = a["href"]
            name = a.text.strip()
            full_link_category = ("http://books.toscrape.com/" + link_category)
            name_category.append(name)
            url_category.append(full_link_category)

# Fonction qui vient extraire les pages des différentes catégories de livre.
def get_url_page(url):
    pages_url = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    current_page = soup.find("li", class_="current")
    numbers_of_pages = 1
    if current_page:
        current_pages_number = current_page.text.split()
        number_of_pages = int(current_pages_number[3])
        for i in range(1, number_of_pages + 1):
            url_page = (url.replace("index.html", "page-") + str(i) + ".html")
            pages_url.append(url_page)
    if not current_page:
        pages_url.append(url)
    extract_url_book(pages_url)


# Fonction qui viens extraire l'url de chaque livre, dans chaque catégorie de livre.
def extract_url_book(url_fiction_page):
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
    extract_datas_book(url_book_fiction)


# Fonction pour récupérer les données de chaque livre de chaque catégorie du site.
def extract_datas_book(url_book_fiction):
    all_book = []
    csv_init = 0
    for datas in url_book_fiction:
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
        all_book.append(fiction_book)
        title_folder = title.replace(":", "").replace("/", " ").replace('"', '').replace(" ", "").replace(
        'Ã©', 'é').replace(",", "").replace(".", "").replace("&", "").replace("*", "").replace("?", "").replace("#", "")

        if (csv_init == 0):
            with open('product\\category_data\\' + str(category) + '\\' + title_folder + '.csv', 'w', encoding="utf-8") as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=',')
                writer.writerow(heading)
                writer.writerow([
                    product_page_url,
                    universal_product_code,
                    title,
                    price_including_tax,
                    price_excluding_tax,
                    number_available,
                    product_description,
                    category,
                    review_rating,
                    image
                ])
            csv_init = 1
        else:
            with open('product\\category_data\\' + str(category) + '\\' + title_folder + '.csv', 'a', encoding="utf-8") as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=',')
                writer.writerow([
                    product_page_url,
                    universal_product_code,
                    title,
                    price_including_tax,
                    price_excluding_tax,
                    number_available,
                    product_description,
                    category,
                    review_rating,
                    image
                ])
        extract_img_product(category, title_folder, image)
def extract_img_product(category, title, url):
    if not os.path.isdir('product\\category_data\\' + str(category) + '\\' + str(category) + '_img'):
        os.mkdir('product\\category_data\\' + str(category) + '\\' + str(category) + '_img')
    f = open('product\\category_data\\' + str(category) + '\\' + str(category) + '_img\\' + title + ".jpg", 'wb')
    print(f)
    reponse_img = requests.get(url)
    f.write(reponse_img.content)
    f.close()

get_all_category()

del url_category[0]
del name_category[0]

create_folder(name_category)

for url in url_category:
    get_url_page(url)


