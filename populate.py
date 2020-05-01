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
        googleId = None

    try:
        title = book['volumeInfo']['title']
    except KeyError:
        title = None

    try:
        authors = book['volumeInfo']['authors']
        authors = str(set(authors))
    except KeyError:
        authors = None

    try:
        pub = book['volumeInfo']['publisher']
    except KeyError:
        pub = None

    try:
        publishedDate = book['volumeInfo']['publishedDate']
    except KeyError:
        publishedDate = None

    try:
        description = book['volumeInfo']['description']
    except KeyError:
        description = None

    try:
        isbn = book['volumeInfo']['industryIdentifiers'][0]['identifier']
    except KeyError:
        isbn = None

    try:
        pageCount = book['volumeInfo']['pageCount']
    except KeyError:
        pageCount = None

    try:
        categories = book['volumeInfo']['categories']
        categories = str(set(categories))
    except KeyError:
        categories = None

    try:
        thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        thumbnail = None

    try:
        smallThumbnail = book['volumeInfo']['imageLinks']['smallThumbnail']
    except KeyError:
        smallThumbnail = None

    try:
        lang = book['volumeInfo']['language']
    except KeyError:
        lang = None

    try:
        webReaderLink = book['accessInfo']['webReaderLink']
    except KeyError:
        webReaderLink = None

    try:
        textSnippet = book['searchInfo']['textSnippet']
    except KeyError:
        textSnippet = None

    try:
        isEbook = book['saleInfo']['isEbook']
    except KeyError:
        isEbook = None

    try:
        averageRating = book['volumeInfo']['averageRating']
    except KeyError:
        averageRating = None

    try:
        maturityRating = book['volumeInfo']['maturityRating']
    except KeyError:
        maturityRating = None

    try:
        ratingsCount = book['volumeInfo']['ratingsCount']
    except KeyError:
        ratingsCount = None

    try:
        subtitle = book['volumeInfo']['subtitle']
    except KeyError:
        subtitle = None

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
        query = sql.SQL("INSERT INTO gb_test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        try:
            cursor.execute(query, entry)
        except Exception as err:
            logging.error(f"Error: {err}")
            connection.rollback()
        else:
            connection.commit()


    cursor.close()
    connection.close()

