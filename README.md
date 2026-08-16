# Shelf Glimpse

Shelf Glimpse is a small command-line book discovery project built with Python and the Open Library Search API. I wanted the project to feel a little more like browsing a shelf instead of only doing one fixed book lookup.

The user can search for books by title, author, or subject. After Open Library returns the results, the user can also choose a publication decade to narrow the list. The program prints a readable list with information about each book instead of printing the raw API response.

## API used

This project uses the Open Library Search API:

`https://openlibrary.org/search.json`

The program uses several fields from the API response, including:

- `title`
- `author_name`
- `first_publish_year`
- `edition_count`

## What the program does

1. Asks whether you want to search by title, author, or subject.
2. Asks for your search words.
3. Requests current book data from Open Library.
4. Lets you optionally filter the results by decade.
5. Displays up to 10 matching books in a readable format.
6. Handles empty searches, invalid menu choices, invalid decades, missing results, and request errors without crashing.

## How to run it

Make sure Python 3 is installed.

Clone or download this repository, then open a terminal in the project folder.

Install the dependency:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python3 main.py
```

## Example searches

- Search by author: `Toni Morrison`
- Search by title: `The Hobbit`
- Search by subject: `architecture`
- Optional decade filter: `1990`
