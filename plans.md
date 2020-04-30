# Google Books API database builder

Ideally, this project will run from inside a docker container.
It will pretend to be a flask application, but it will really just be a 
constantly running script. It will run for as many hours a day as 
needed. It will have these basic features:

- Will populate the database with unique values, skipping multiple entries
- Will save the index that it stops on so that it can continue from that 
  index on the next time that it runs
- Will stop when it has exhausted publishers
- Will email recipients at regular intervals to report the progress

Depending on the types of issues encountered, this program may:
- rotate IP addresses
- delay API get requests by a pre-determined time

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
);```

