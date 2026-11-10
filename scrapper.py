from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import time
import os

file_name = "products.csv"
base_url = "https://webscraper.io/test-sites/e-commerce/static"

# Global generator instance to maintain state across pages
sidebar_generator = None

#-------------- the page scraper ----------------------

def scrape_page(url):
    global sidebar_generator
    
    response = requests.get(url, timeout=10)
    response.raise_for_status() 
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'lxml')

    # Fix 1: Correctly target product elements on this specific test site
    product_elements = soup.find_all("div", class_="thumbnail")
    products = []

    for product in product_elements:
        try:
            # Fix 2: Clean element selections with safeties
            title_tag = product.find("a", class_="title")
            product_name = title_tag["title"] if title_tag.has_attr("title") else title_tag.text.strip()
            product_link = urljoin(url, title_tag["href"])
            
            # The test site uses 'pull-right' or 'float-end' based on Bootstrap version
            price_tag = product.find(class_="price")
            product_price = price_tag.text.strip() if price_tag else "N/A"
            
            desc_tag = product.find("p", class_="description")
            product_description = desc_tag.text.strip() if desc_tag else "N/A"
            
            # Extract rating from the number of star elements or paragraph attribute
            rating_tag = product.find("p", attrs={"data-rating": True})
            product_rating = rating_tag["data-rating"] if rating_tag else "0"
            
            # Fix 3: Added missing parentheses () to .strip
            review_tag = product.find("p", class_="review-count")
            product_reviews = review_tag.text.strip() if review_tag else "0"
        
            products.append({
                "Product name": product_name, 
                "Product price": product_price, 
                "Product description": product_description, 
                "Product link": product_link,
                "Product rating": product_rating,
                "Product reviews": product_reviews
            })
        except (TypeError, KeyError) as e:
            continue # Skip individual corrupted product blocks gracefully

#-------------- next page navigation ----------------------

    nav_tag = soup.find("nav")
    next_button = nav_tag.find("a", class_="page-link next") if nav_tag else None
    
    if next_button and "href" in next_button.attrs:
        next_url = urljoin(url, next_button["href"])
    else:   
        # Fix 4: Instantiate the generator ONCE and advance it step-by-step
        if sidebar_generator is None:
            sidebar_generator = side_bar_nav(soup)
        
        next_sidebar_rel_url = next(sidebar_generator, False)
        if next_sidebar_rel_url:
            next_url = urljoin(base_url, next_sidebar_rel_url)
        else:
            next_url = None
        
    return products, next_url

#-------------- creation and insertion of the product data  ----------------------
def write_products(products):
    if not products:
        return
    field_names = ["Product name", "Product price", "Product description", "Product link", "Product rating", "Product reviews"]
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8-sig') as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerows(products)  
     
def fetch_products(start_url):
    if os.path.exists(file_name):
        os.remove(file_name)

    current_url = start_url
    while current_url:
        try:
            print(f"Scraping: {current_url}")
            products, current_url = scrape_page(current_url)
            write_products(products)
            time.sleep(1)
    
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.RequestException as err:
            print(f"A network error occurred: {err}")
            break
            
#-------------- side bar navigation  ----------------------

def side_bar_nav(soup):
    # Matches the test site's side navigation layout
    ul_tag = soup.find("ul", id="side-menu") or soup.find("ul", class_="nav")
    if not ul_tag:
        return
    
    a_tags = ul_tag.find_all("a")
    for tag in a_tags:
        if tag.text and "href" in tag.attrs:
            text_content = tag.text.strip()

            # Allows subcategory traversal like "Laptops" or "Tablets"
            if "Home" not in text_content:
                yield tag["href"]

def sub_cat_nav(link):
    link = next(side_bar_nav, False)
    if link:
        pass

if __name__ == "__main__":
    fetch_products(base_url)
