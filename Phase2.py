# Importation des librairies
import requests
from bs4 import BeautifulSoup
import csv


# Phase 2
# Fonction pour récupérer les URLS de chaque page de la catégorie "Fiction".
def extract_url_page():
    url_fiction_page = []
    page_product = 1
    for i in range(4):
        i = f"http://books.toscrape.com/catalogue/category/books/fiction_10/page-{page_product}.html"
        page_product += 1
        url_fiction_page.append(i)
    extract_url_book(url_fiction_page)
    return url_fiction_page

# Fonction pour récupérer les URLS de chaque livre de la catégorie "Fiction".
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
    return url_book_fiction

# Fonction pour récupérer les données de chaque livre de la catégorie "Fiction".
def extract_datas_book(url_book_fiction):
    all_fiction_book = []
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
        all_fiction_book.append(fiction_book)
    print(len(all_fiction_book))

extract_url_page()

