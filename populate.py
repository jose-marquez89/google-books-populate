import requests
import logging

import psycopg2

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# TODO: make a call to the api for the maximum allowable results - 40
# TODO: iterate through pages, increasing index by 40 at time until less than 40 results are returned
# TODO: cache the api call or the index position of publishers so that they are not repeated
# TODO: account for missing/null values
# TODO: query the database; add book to database (rate limit)

DATABASE_URL = os.environ["DATABASE_URL"]

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

query =
"""
INSERT INTO gb_test
VALUES ('MkHJ91AwS8MC', 'A Long Way Gone', '{"Ishmael Beah"}', 'Macmillan', '2007-02-13', 'In a heart-wrenching, candid autobiography, a human rights activist offers a firsthand account of war from the perspective of a former child soldier, detailing the violent civil war that wracked his native Sierra Leone and the government forces that transformed a gentle young boy into a killer as a member of the army. 75,000 first printing.', '9780374105235', 229.0, '{"Biography & Autobiography"}', 'http://books.google.com/books/content?id=MkHJ91AwS8MC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api', 'http://books.google.com/books/content?id=MkHJ91AwS8MC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'en', 'http://play.google.com/books/reader?id=MkHJ91AwS8MC&hl=&printsec=frontcover&source=gbs_api', NULL, true, 4.0, 'NOT_MATURE', NULL, 'Memoirs of a Boy Soldier');
"""

if __name__ == "__main__":
    try:
        cursor.execute(query)
    except Exception as err:
        logging.error(f"Error: {err}")
        
