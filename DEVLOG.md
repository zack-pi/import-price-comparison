# Day 1

I have been pondering for a long time about what to build as a project. With the rise of AI in the web dev space, it is more difficult to find motivation to do it on your own. But to truly learn, I must do it on my own. This is my day 1. I will try, I will break things, but I will continue.

## Why this project?

I decided that my first project will be some sort of price comparison of products, mainly ones that can be imported.

Eventually I want each result to show the price, MOQ, supplier name, how long the supplier has been active, and whether they're verified or not. This will be the base.

Why did I choose this? Well, I have experience in this type of business venture: finding products for clients and presenting them good prices.

I know most of those websites have a filter option to retrieve the lowest-priced products. But the way I want to compare is by looking at the product description and the company itself too, to help make the best decision, because low price doesn't mean you will get what you are seeing in the pictures.

Since I have never worked on a project like this, I will start by practicing on retrieving data from easy-to-scrape websites, then repurpose that same code for other websites, and then maybe see what I can do with more dynamic websites.

## Day 1 goal

Scrape the title, price and link of every book on books.toscrape.com and print them.

From what I read online, you use "Beautiful Soup" to scrape static pages. I hadn't tried working with it before, so I watched a video about it to see what I could learn about the library. I installed Beautiful Soup and the lxml parser. I didn't know what a parser did, so I read this: https://www.huntress.com/cybersecurity-101/topic/what-is-a-parser. Pretty interesting stuff. I also read a bit about XML.

I made a basic prototype. Since I was still figuring out the library, at first I used two loops to extract the info, but I fixed that problem. Since I had to work with URLs, I needed to use `urllib`. I wasn't sure what it did or how to use it, so I watched some videos and read about it a bit.

I saw that, basically, if you import `requests`, it is similar to `urllib.request`, just with different syntax. I used `urllib.parse` to join my root URL and the relative URL. I just finished learning how to use it, and I believe I learned enough about it.

I also learned that you should be careful if you use user input as a URL. If the program fetches whatever URL a user gives it, they can point it at places you didn't intend, such as internal pages on your own network. `urljoin` has a similar quirk: if the second part is a full URL, it ignores the first part completely, so a link can send your program to a different site.

So I have finally made the scraper. It takes in data from the books page, follows pagination, and retrieves the title, price and link of each book. It scraped 1000 books across 50 pages, and it wasn't that difficult. Currently I'm saving it to a txt file. My next step is saving to a CSV file and repurposing my code for a different webpage. I'm still trying to make sense of everything, like the response codes and all the stuff related to Beautiful Soup, and I want to organize my code into well-structured functions.

## What broke

At first, I didn't write the code using functions. I had to split it into functions after I finished writing it, and deciding which line goes where, what each function should return, and which parameters it needs was a pain. From now on, I will start with my functions so I don't have to do that again.

I also wanted to save each book in a dictionary using the title as the key, but some books might share the same title and overwrite each other. So I used a list of dictionaries instead.

The prices showed up as Â£ instead of £. `requests` guessed the wrong text encoding, so I set `response.encoding = "utf-8"` and later added `encoding="utf-8"` when opening files.

## GitHub setup

To post my code and dev log, I needed to make a GitHub account, and honestly I didn't know much about it. I took a quick look at how it works.

I learned a little about GitHub, and I still need to learn more. I uploaded my files manually, which is fine for now, but later I will use command lines. I'm trying to follow good habits by writing a README and a requirements file so anyone can install what's needed to run the program.
I also added a `.gitignore`, a file that tells git which files not to upload. I already knew that `.env` is usually where you store your API keys, so it should never be uploaded. I had seen `__pycache__` before, and now I know it's a folder Python creates automatically when you run your code. It stores compiled versions of your files so they load faster, so it's clutter that doesn't belong in the repo. I also learned that `.venv` is a virtual environment, which keeps each project's dependencies separate from the others and from my global Python.
