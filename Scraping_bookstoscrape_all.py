import requests
from bs4 import BeautifulSoup
import csv
import shutil
import os.path

# fonction 1: request and soup() ; request et parse d'une url
def request_and_soup(x):
    reponse = requests.get(x)
    HTML = reponse.content
    soup  = BeautifulSoup(HTML, "html.parser")
    return soup

# fonction 2: url_list_category_all_pages(); creation d'une liste de toutes les pages d'une catgorie (pouvant être superieur à 7, ex:default)
def url_list_category_all_pages(z):
    url_list_category_x=[]
    for i in range(1,13):
        url_list_category_x.append(z.replace("index",  ("page-" + str(i))))
    a = url_list_category_x[0]
    b = a.replace("page-1", "index")
    url_list_category_x[0] = b
    return url_list_category_x

# fonction 3: extract_books_link ;creation de la liste de liens des livres par page de categorie
def extract_books_link(w):
    soup = request_and_soup(w)
    category_book_link_page_x =[]
    href_a_tag = soup.find_all('h3')
    for h3 in href_a_tag:
      category_book_link_page_x.append(h3.a['href'])
    category_book_link_page_x = [s.replace("../../..", "https://books.toscrape.com/catalogue") for s in category_book_link_page_x]
    return category_book_link_page_x

# fonction 4: extract_book_data; recuperation data pour chaque liens de la category 
def extract_book_data(y):
    soup = request_and_soup(y)
    book_title = soup.h1.string
    description  = soup.find("meta", attrs={"name": "description"}).get("content").lstrip()
    book_img_link = soup.find("img").get('src').replace("../..", "https://books.toscrape.com")
    informations = [y, book_title, description, book_img_link]
    for infos in soup.find_all('td'):
        informations.append(infos.string)
    a = informations[9]
    b = a.split()
    c = b[2]
    d = c.lstrip("(")
    informations[9]=d
    return informations

#fonction 5: category_book_data_csv_and_download_img ; creation du fichier csv , donwload ensemble des img de la category dans un dossier specific
def category_book_data_csv_and_download_img(v):
    properties = ["book_url", "book_title", "description" ,"img link", "upc", "product type", "price (excl. tax)", "price (incl. tax)", "tax", "availabilily", "numbers of review"]
    soup = request_and_soup(v)
    category_title = soup.h1.text
    a = f"{category_title}_dir"
    b = f"{category_title}_img"
    os.makedirs(str(a+"/"+b),exist_ok=True)   
    with open(os.path.join(a, f"{category_title}_data.csv"), "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(properties)
        for i in book_data:
            writer.writerow(i)
    for i in book_data:
        book_title = i[1]
        book_link_img = i[3]
        try:
            f = open(f"{category_title}.{book_title}.jpg", "wb")
            response = requests.get(book_link_img)
            f.write(response.content)
            f.close()
            shutil.move(f"{category_title}.{book_title}.jpg",str(a+"/"+b))
        except : 
            pass
    try:
        shutil.move(a,"Books to Scrape_Datas")
    except:
        pass

URL = "https://books.toscrape.com/index.html"

os.makedirs("Books to Scrape_Datas",exist_ok=True)
page_links =[]
soup = request_and_soup(URL)
for a in soup.find_all('a', href=True):
    page_links.append(a["href"])

category_links = page_links[3:53]
category_links = [s.replace("catalogue", "https://books.toscrape.com/catalogue") for s in category_links]


for category_url in category_links:
    url_list_category_x = url_list_category_all_pages(category_url)
    category_book_link_all_imbriquee= list(map(extract_books_link, url_list_category_x))
    category_book_link_all = sum(category_book_link_all_imbriquee,[])
    book_data =[]
    for l in category_book_link_all:
        extract_book_data(l)
        book_data.append(extract_book_data(l))
    category_book_data_csv_and_download_img(category_url)