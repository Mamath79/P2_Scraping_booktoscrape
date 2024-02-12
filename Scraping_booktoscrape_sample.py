"""
RAJOUTER COMMENATIRE EN DEBUT DE FICHIER
"""

import csv
import shutil
import os.path

import requests

from bs4 import BeautifulSoup


########################################
# BEST PRACTICE
########################################

from src.functions import *

#############################################
#   CODE EN ANGLAIS POUR LE MOMENT
#############################################


############################################
# BEST PRATICE => MAIN function
############################################


def main():
    """main fucntion"""

    URL = "https://books.toscrape.com/index.html"

    os.makedirs("Books to Scrape_Datas", exist_ok=True)
    page_links = []
    soup = request_and_soup(URL)
    for a in soup.find_all("a", href=True):
        page_links.append(a["href"])

    category_links = page_links[3:7]
    category_links = [
        s.replace("catalogue", "https://books.toscrape.com/catalogue")
        for s in category_links
    ]

    for category_url in category_links:
        url_list_category_x = url_list_category_all_pages(category_url)
        category_book_link_all_imbriquee = list(
            map(extract_books_link, url_list_category_x)
        )
        category_book_link_all = sum(category_book_link_all_imbriquee, [])
        book_data = []
        for l in category_book_link_all:
            extract_book_data(l)
            book_data.append(extract_book_data(l))
        category_book_data_csv_and_download_img(category_url)


############################################
# BEST PRATICE => MAIN function
############################################

if __name__ == "__main__":
    main()
