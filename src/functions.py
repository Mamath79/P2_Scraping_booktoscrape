import csv
import shutil
import os.path

import requests

from bs4 import BeautifulSoup


def request_and_soup(x):
    """# fonction 1: request and soup() ; request et parse d'une url"""
    # Ca s'appelle une docstring

    reponse = requests.get(x)
    HTML = reponse.content
    soup = BeautifulSoup(HTML, "html.parser")

    # separer return
    return soup


def url_list_category_all_pages(z):
    """# fonction 2: url_list_category_all_pages(); creation d'une liste de toutes les pages d'une catgorie (pouvant être superieur à 7, ex:default)"""

    ###############################################"
    # AERER LE CODE
    ###############################################""
    url_list_category_x = []

    for i in range(1, 10):
        url_list_category_x.append(z.replace("index", ("page-" + str(i))))

    a = url_list_category_x[0]
    b = a.replace("page-1", "index")

    url_list_category_x[0] = b

    return url_list_category_x


def extract_books_link(w):
    """# fonction 3: extract_books_link ;creation de la liste de liens des livres par page de categorie"""

    soup = request_and_soup(w)
    category_book_link_page_x = []
    href_a_tag = soup.find_all("h3")

    for h3 in href_a_tag:
        category_book_link_page_x.append(h3.a["href"])

    # BIEN LA COMPREHENSION DE LISTE 😃
    category_book_link_page_x = [
        s.replace("../../..", "https://books.toscrape.com/catalogue")
        for s in category_book_link_page_x
    ]
    return category_book_link_page_x


def extract_book_data(y):
    """# fonction 4: extract_book_data; recuperation data pour chaque liens de la category"""

    soup = request_and_soup(y)
    book_title = soup.h1.string

    ################################################
    # COMMENTER !!!!!
    ################################################

    ################################################
    # AERER
    ################################################
    description = (
        soup.find("meta", attrs={"name": "description"}).get("content").lstrip()
    )
    book_img_link = (
        soup.find("img").get("src").replace("../..", "https://books.toscrape.com")
    )

    star_rating_soup = soup.find_all("p", {"class": "star-rating"})
    star_rating_txt = star_rating_soup[0]["class"][1]
    dict = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    star_rating = dict[star_rating_txt]
    informations = [y, book_title, description, book_img_link, star_rating]

    for infos in soup.find_all("td"):
        informations.append(infos.string)

    ###########################################
    # ATTENTION AU NOM DES VARIABLES
    ###########################################

    informations[7:10] = [i.strip("£") for i in informations[7:10]]
    a = informations[10]
    b = a.split()
    c = b[2]
    d = c.lstrip("(")
    informations[10] = d
    return informations


def category_book_data_csv_and_download_img(v):
    """# fonction 5: category_book_data_csv_and_download_img ; creation du fichier csv , donwload ensemble des img de la category dans un dossier specific"""

    properties = [
        "book_url",
        "book_title",
        "description",
        "img link",
        "star rating",
        "upc",
        "product type",
        "price (excl. tax)",
        "price (incl. tax)",
        "tax",
        "availabilily",
        "numbers of review",
    ]

    #############################################
    # commenter
    #############################################

    #############################################
    # aerer
    #############################################

    soup = request_and_soup(v)
    category_title = soup.h1.text
    a = f"{category_title}_dir"
    b = f"{category_title}_img"

    os.makedirs(str(a + "/" + b), exist_ok=True)

    with open(os.path.join(a, f"{category_title}_data.csv"), "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(properties)
        for i in book_data:
            writer.writerow(i)
    for i in book_data:
        book_title = i[1]
        book_link_img = i[3]
        try:
            f = open(f"{category_title}_{book_title}.jpg", "xb")
            response = requests.get(book_link_img)
            f.write(response.content)
            f.close()

        #############################################"
        # JAMAIS de Except tout seul + jamais de pass
        #############################################""
        # except:
        #     pass

        ########################
        # PLUTOT CA
        ########################
        except Exception as e:
            print(e)

        try:
            shutil.move(
                f"{category_title}_{book_title}.jpg",
                str(a + "/" + b),
                copy_function=shutil.copy,
            )
        except:
            pass
    path = "Books to Scrape_Datas/" + a
    if os.path.isdir(path) == False:
        shutil.move(a, "Books to Scrape_Datas")
    else:
        shutil.rmtree(path)
        shutil.move(a, "Books to Scrape_Datas")
