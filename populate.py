import requests
import logging
import os
import threading
from urllib.parse import urljoin, quote

import psycopg2
from psycopg2 import sql

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# books = book_data['items']
# values = []


def gb_url(search_term, index=None):
    """
    Creates a valid url for request

    search_term: the terms to search for via the specified parameter

    index: defaults to None, can be used to paginate results
    """
    base_url = "https://www.googleapis.com/books/v1/"
    volumes = "volumes?q="
    parameter = "inpublisher:"
    max_results = "&maxResults=40"

    if index:
        tail = (volumes +
                parameter +
                quote(search_term) +
                max_results +
                f"&startIndex={index}")
    else:
        tail = (volumes +
                parameter +
                quote(search_term) +
                max_results)

    url = urljoin(base_url, tail)

    return url


def get_value(book):
    """
    Compiles book data from json response into an iterable
    for use in SQL command

    book: one individual item in googleAPIresponse['items']
    """
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

    value = [googleId, title, authors, pub, publishedDate,
             description, isbn, pageCount, categories, thumbnail,
             smallThumbnail, lang, webReaderLink, textSnippet,
             isEbook, averageRating, maturityRating, ratingsCount,
             subtitle]

    return value


def request_and_execute(search_term, starting_index):
    """
    Creates a GET request to google books API, collects data, then uses
    this data to execute a SQL query with connection to database
    """

    # create connection
    DATABASE_URL = os.environ["DATABASE_URL"]

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # GET request
    url = gb_url(search_term, index=starting_index)
    response = requests.get(url)

    try:
        response.raise_for_status()
    except Exception as err:
        logging.error(err)

        return None

    data = response.json()

    if 'items' not in data.keys():
        logging.info(
            f"No items for {search_term} at index {starting_index}"
        )

        return None

    books = data['items']
    values = []

    for book in books:
        values.append(get_value(book))

    for entry in values:
        query = sql.SQL(
            "INSERT INTO gb_test VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        try:
            cursor.execute(query, entry)
        except Exception as err:
            logging.error(f"Error: {err}")
            connection.rollback()
        else:
            connection.commit()

    cursor.close()
    connection.close()

    return True


def get_publisher_books():

    """Gets books data from index 0 of API request pages, starts
    necessary threads to collect other pages
    """
    pass

# for book in books:
    # value = get_value(book)
    # values.append(value)


# TODO: make a call to the api for the maximum allowable results - 40

# TODO: iterate through pages, increasing index by 40
#       at a time until less than 40 results are returned

# TODO: cache the api call or the index position of
#       publishers so that they are not repeated

# TODO: query the database; add book to database (rate limit)

# DATABASE_URL = os.environ["DATABASE_URL"]

# connection = psycopg2.connect(DATABASE_URL)
# cursor = connection.cursor()

if __name__ == "__main__":
    for entry in values:
        query = sql.SQL(
            "INSERT INTO gb_test VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        try:
            cursor.execute(query, entry)
        except Exception as err:
            logging.error(f"Error: {err}")
            connection.rollback()
        else:
            connection.commit()

    cursor.close()
    connection.close()
