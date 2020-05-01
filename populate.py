import requests
import logging
import os

import psycopg2
from psycopg2 import sql

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

api_url = "https://www.googleapis.com/books/v1/volumes?q="
publisher_param = "inpublisher:"
publisher = 'penguin'
sep = "&"
max_results = "maxResults=40"
res = requests.get(api_url + publisher_param +
                   publisher + sep + max_results)
book_data = res.json()
books = book_data['items']
values = []


def get_value(book):

    try:
        googleId = book['id']
    except KeyError:
        googleId = "NULL"

    try:
        title = book['volumeInfo']['title']
    except KeyError:
        title = "NULL"

    try:
        authors = f"ARRAY{book['volumeInfo']['authors']}"
    except KeyError:
        authors = "NULL"

    try:
        pub = book['volumeInfo']['publisher']
    except KeyError:
        pub = "NULL"

    try:
        publishedDate = book['volumeInfo']['publishedDate']
    except KeyError:
        publishedDate = "NULL"

    try:
        description = book['volumeInfo']['description']
    except KeyError:
        description = "NULL"

    try:
        isbn = book['volumeInfo']['industryIdentifiers'][0]['identifier']
    except KeyError:
        isbn = "NULL"

    try:
        pageCount = f"ARRAY{book['volumeInfo']['pageCount']}"
    except KeyError:
        pageCount = "NULL"

    try:
        categories = book['volumeInfo']['categories']
    except KeyError:
        categories = "NULL"

    try:
        thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        thumbnail = "NULL"

    try:
        smallThumbnail = book['volumeInfo']['imageLinks']['smallThumbnail']
    except KeyError:
        smallThumbnail = "NULL"

    try:
        lang = book['volumeInfo']['language']
    except KeyError:
        lang = "NULL"

    try:
        webReaderLink = book['accessInfo']['webReaderLink']
    except KeyError:
        webReaderLink = "NULL"

    try:
        textSnippet = book['searchInfo']['textSnippet']
    except KeyError:
        textSnippet = "NULL"

    try:
        isEbook = book['saleInfo']['isEbook']
    except KeyError:
        isEbook = "NULL"

    try:
        averageRating = book['volumeInfo']['averageRating']
    except KeyError:
        averageRating = "NULL"

    try:
        maturityRating = book['volumeInfo']['maturityRating']
    except KeyError:
        maturityRating = "NULL"

    try:
        ratingsCount = book['volumeInfo']['ratingsCount']
    except KeyError:
        ratingsCount = "NULL"

    try:
        subtitle = book['volumeInfo']['subtitle']
    except KeyError:
        subtitle = "NULL"

    value = [googleId, title, authors, publisher, publishedDate,
             description, isbn, pageCount, categories, thumbnail,
             smallThumbnail, lang, webReaderLink, textSnippet,
             isEbook, averageRating, maturityRating, ratingsCount,
             subtitle]

    return value

for book in books:
    value = get_value(book)
    values.append(value)


# TODO: make a call to the api for the maximum allowable results - 40
# TODO: iterate through pages, increasing index by 40 at time until less than 40 results are returned
# TODO: cache the api call or the index position of publishers so that they are not repeated
# TODO: account for missing/null values
# TODO: query the database; add book to database (rate limit)

DATABASE_URL = os.environ["DATABASE_URL"]

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

if __name__ == "__main__":
    for entry in values:
        query = sql.SQL(
"""
INSERT INTO gb_test
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""         .format(entry)
        )
        try:
            cursor.execute(query)
        except Exception as err:
            logging.error(f"Error: {err}")

    connection.commit()
    cursor.close()
    connection.close()

