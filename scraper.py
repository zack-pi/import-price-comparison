from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time


url = "https://books.toscrape.com/"

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

    next_button = soup.find("li", class_="next")
    if next_button:
        next_url = urljoin(url, next_button.a["href"])
    else:
        next_url = None

    return books, next_url

def write_books(books, counter):
    with open("books.txt", "a", encoding="utf-8") as file:     
        for book in books:
            counter +=1
            file.write(f"------------Book {counter}--------------\n")
            file.write("\n")
            file.write(f"Book Title: {book['title']}\n")
            file.write(f"Book Price: {book['currency'] + str(book['price'])}\n")
            file.write(f"Book Link: {book['link']}\n")
            file.write("\n")
    
    return counter  
     
def fetch_books(url):
    counter = 0
    with open("books.txt", "w", encoding= "utf-8") as file:
        pass

    while url:
        try:
            books, url = scrape_page(url)
            counter = write_books(books,counter)

            time.sleep(1)
    
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.RequestException as err:
            print(f"A network error occurred: {err}")
            break
            
    with open("books.txt", "a", encoding="utf-8") as file:
        file.write(f"Total amount of books: {counter}\n")
    

if __name__ == "__main__":
    fetch_books(url)
