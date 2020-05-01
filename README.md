# Google Books API database builder

Ideally, this project will run from inside a docker container.
It will not be a web server environment. It will run for as long as needed
and may be on a cron job that runs every hour (TBA).
It will have these basic features:

- Will populate the database with unique values, skipping multiple entries
- Will save the index that it stops on so that it can continue from that
  index on the next time that it runs
- Will stop when it has exhausted significant publishers
- Will email recipients at regular intervals to report the progress
  probably publisher index.

Depending on the types of issues encountered, this program may:
- rotate IP addresses
- delay API get requests by a pre-determined time
- stop all processes at a certain time of day (peak hours)


### Table Creating SQL

```sql

CREATE TABLE gb_test (
	googleId varchar(20) UNIQUE,
	title varchar(300) UNIQUE,
	authors text[],
	publisher varchar(200),
	publishedDate varchar(40),
	description text,
	isbn varchar(20),
	pageCount integer,
	categories text[],
	thumbnail varchar(200),
	smallThumbnail varchar(200),
	lang varchar(10),
	webReaderLink varchar(150),
	textSnippet varchar(5000),
	isEbook boolean,
	averageRating float,
	maturityRating varchar(20),
	ratingsCount integer,
	subtitle varchar(400),
);
```
### Necessary Keys
```python
book['id']
book['volumeInfo']['title']
book['volumeInfo']['authors'] # format str(set(authors))
book['volumeInfo']['publisher']
book['volumeInfo']['publishedDate']
book['volumeInfo']['description']
book['volumeInfo']['industryIdentifiers'][0]['identifier']
book['volumeInfo']['pageCount']
book['volumeInfo']['categories']
book['volumeInfo']['imageLinks']['smallThumbnail']
book['volumeInfo']['imageLinks']['thumbnail']
book['volumeInfo']['language']
book['accessInfo']['webReaderLink']
book['searchInfo']['textSnippet']
book['saleInfo']['isEbook']
book['volumeInfo']['averageRating']
book['volumeInfo']['maturityRating']
book['volumeInfo']['ratingsCount']
book['volumeInfo']['subtitle']
```
