# Importation des librairies
import requests
from bs4 import BeautifulSoup
import csv

# Phase 1
url = "http://books.toscrape.com/catalogue/william-shakespeares-star-wars-verily-a-new-hope-william-shakespeares-star-wars-4_871/index.html"
response = requests.get(url)

# Réponse qui viens récupérer l'url si la requête ce passe bien
if response.ok:
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    # On récolte les données demander
    product_page_url = url

    datas_book = soup.find_all("td")
    universal_product_code = datas_book[0].text
    title = soup.find("h1").text
    price_including_tax = datas_book[3].text
    price_excluding_tax = datas_book[2].text
    number_available = datas_book[5].text
    product_description = soup.select_one("article > p").text
    category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
    review_rating = soup.find("p", class_="star-rating").get("class")[1]

    # Url de base du site Books to scrape
    base_url = "http://books.toscrape.com/"
    image_url = soup.find("div", class_="item active").find("img").get("src")
    image = (base_url + image_url).replace("../../", "")
    print(image)

    # Création d'une liste pour les en-têtes
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

    # Création d'un nouveau fichier csv pour écrire dans le fichier appelé "Book/datas.csv"
    with open('datas.csv', 'w') as fichier_csv:
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

