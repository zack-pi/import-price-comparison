from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import time
import os

file_name = "books.csv"
url = "https://books.toscrape.com/"


#-------------- the page scraper ----------------------

def scrape_page(url):

    response = requests.get(url, timeout=10)
    response.raise_for_status() 
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.find_all("article", class_= "product_pod")

    books = []
    for article in articles:
        book_name = article.h3.a["title"]
        book_link = urljoin(url, article.h3.a["href"])
        div_tag = article.find("div", class_ = "product_price")
        p_tag = div_tag.find("p", class_ = "price_color")
        book_price = float(p_tag.text[1:])
        price_currency = p_tag.text[0]
    
        books.append({"title": book_name, "price": book_price, "currency": price_currency, "link": book_link})


#-------------- next page navigation ----------------------

    next_button = soup.find("li", class_="next")
    if next_button:
        next_url = urljoin(url, next_button.a["href"])
    else:
        next_url = None

    return books, next_url

#-------------- creation and insertion of the book data  ----------------------
def write_books(books):
    field_names = ["title", "price" ,"currency" , "link"]
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8-sig') as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        if not file_exists:
            writer.writeheader()

        writer.writerows(books)  
     
def fetch_books(url):
#-------------- main loop to execute the functions on each books page  ----------------------
    if os.path.exists(file_name):
        os.remove(file_name)

    while url:
        try:
            books, url = scrape_page(url)
            write_books(books)

            time.sleep(1)
    
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.RequestException as err:
            print(f"A network error occurred: {err}")
            break
            
    

if __name__ == "__main__":
    fetch_books(url)
