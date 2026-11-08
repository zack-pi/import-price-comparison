from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time
import os
import csv

site_url = "https://webscraper.io"
base_url = "https://webscraper.io/test-sites/e-commerce/static"
file_name = "products.csv"
seen_links = set()
def reset_output_file():
    if os.path.exists(file_name):
        os.remove(file_name)
    
def fetch_page(url):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response
    except requests.exceptions.RequestException as err:
        print(f"HTTP error occurred: {err}")
        return None
    
def get_soup(url):
    response = fetch_page(url)
    if response:
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    return None

def side_bar_nav():
    first_links = []
    soup = get_soup(base_url)
    if not soup:
        return []
    div_tag = soup.find("div", role="navigation")
    if not div_tag:
        return []
    a_tags = div_tag.find_all("a", class_="nav-link")
    if not a_tags:
        return []
    for tag in a_tags:
        first_links.append(urljoin(site_url, tag["href"]))

    completed_links = []
    for link in first_links:
        soup = get_soup(link)
        if not soup:
            continue
        div_tag = soup.find("div", role="navigation")
        if not div_tag:
            continue
        a_tags = div_tag.find_all("a", class_="nav-link")
        if not a_tags:
            continue
        for tag in a_tags:
            new_tag =urljoin(site_url, tag["href"])
            if new_tag not in completed_links:
                completed_links.append(new_tag)

    return completed_links

def scraping(url):
    soup = get_soup(url)
    if not soup:
        return []
    products = []
    div_tag = soup.find_all("div", class_ = "thumbnail")
    
    for tag in div_tag:
        title_tag = tag.find("a", class_ = "title")
        product_name = title_tag["title"] if title_tag.has_attr("title") else title_tag.text.strip()
        product_link = urljoin(base_url, title_tag["href"]) if title_tag.has_attr("href") else "N/A"

        price_tag = tag.find("h4", class_ = "price")
        product_price = price_tag.text.strip() if price_tag else "N/A"

        review_tag = tag.find("p", class_ = "review-count")
        product_review = review_tag.text.strip() if review_tag else 0

        rating_tag = tag.find("p", attrs={"data-rating": True})
        product_rating = rating_tag["data-rating"] if rating_tag else 0


        products.append({"Product name": product_name, 
                         "Product price": product_price, 
                         "Product reviews": product_review,
                         "Product rating": product_rating,
                         "Product link": product_link})
    
    return products

def save_to_csv(products):
    if not products:
        return
    new_products = [p for p in products if p["Product link"] not in seen_links]
    if not new_products:
        return
    seen_links.update(p["Product link"] for p in new_products)
    field_names = ["Product name", "Product price", "Product reviews", "Product rating", "Product link"]
    file_exists = os.path.exists(file_name)
    with open(file_name, mode=  "a", newline = "", encoding = "utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_products) 
   
        
        
        
def main():
    reset_output_file()
    print("Scraping initialised!")

    side_bar_urls = side_bar_nav()

    for url in side_bar_urls:
        print(f"Currently scraping page: {url}")
        products = scraping(url)
        save_to_csv(products)
        current_url = url
        while current_url:
            soup = get_soup(current_url)
            if not soup:
                break
            div_tag = soup.find("div", id="static-pagination")
            if not div_tag:
                break
            a_tag = div_tag.find("a", rel="next")
            if not a_tag:
                break
            current_url = urljoin(site_url, a_tag["href"])
            print(f"Currently scraping page: {current_url}")
            products = scraping(current_url)
            save_to_csv(products)
            time.sleep(0.5)
        time.sleep(0.5)
        

    print("Scraping Done!")


if __name__ == "__main__":
    main()
    with open("products.csv", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    links = [r["Product link"] for r in rows]
    print(len(rows), len(set(links)))
