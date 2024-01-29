import json
import logging

from model import Author, Quote
from parse_authors import load_authors
from parse_quotes import load_quotes


URI = 'http://quotes.toscrape.com'
path_authors = 'authors.json'
path_quotes = 'quotes.json'


def load_authors_data():
    # зчитуємо файл authors.json
    with open("authors.json", "r", encoding="utf-8") as f:
        authors_data = json.load(f)

        for author_data in authors_data:
            fullname = author_data["author"]

            # якщо автор вже існує то не добавляти його в бд
            author_existing = Author.objects(fullname=fullname)
            if author_existing:
                logging.error(f"this author '{fullname}' already exists.")
                continue

            born_location = author_data.get("borns_location", "")
            born_date = author_data["borns"]
            description = author_data["descriptions"]

            author = Author(
                fullname=fullname,
                born_date=born_date,
                born_location=born_location,
                description=description,
            )
            author.save()


def load_quotes_data():
    # зчитуємо файл quotes.json
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes_data = json.load(f)

        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data["author"]).first()
            tags = quote_data.get("tags", [])

            # # якщо цитата існує то не добавляти її в бд
            quotes_existing = Quote.objects(
                tags=quote_data['tags'], quote=quote_data["quote"], author=author
            )
            if quotes_existing:
                logging.error(f"This quote already exists!")
                continue
            # якщо цитата не існує то добавляти її в бд
            quotes = Quote(tags=tags, quote=quote_data["quote"], author=author)
            quotes.save()



if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    try:
        load_quotes(URI, path_quotes)
        load_authors(URI, path_authors)

    except Exception as err:
        logging.error('Error: {%s}' % err)

    try:
        load_authors_data()
        load_quotes_data()

    except FileNotFoundError as e:
        logging.error(f"Error: this file not exist {e}")

    logging.info("Data loaded successfully.")
