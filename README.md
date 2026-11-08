# Import Price Comparison
 web app that collects product listings from factories and suppliers so you can compare prices, descriptions, factory verification and factory age. Save the products you're interested in and get updates when prices change.

🚧 Work in progress. Currently learning web scraping with a practice site; supplier scraping comes next.

## Why I'm building this

I have experience finding products for clients and presenting them good prices. Most marketplaces let you filter by lowest price, but a low price doesn't guarantee you get what you see in the pictures. I want to compare the product description and the company behind it too.

## Current status

- Scrapes the title, price, currency and link of every book on [books.toscrape.com](https://books.toscrape.com/), following pagination across all 50 pages
- Saves the results to `books.csv`

## How to run

```bash
pip install -r requirements.txt
python scraper.py
```

## Planned

- [x] Save results to CSV
- [x] Reuse the scraper on a second practice site
- [ ] Scrape real supplier listings (price, MOQ, supplier name, years active, verified status)
- [ ] Handle dynamic (JavaScript) pages
- [ ] Save products and track price changes

## Dev log

I'm documenting the process in [DEVLOG.md](DEVLOG.md).
