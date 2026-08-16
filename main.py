import requests


OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def show_welcome_message():
    print("\nShelf Glimpse")
    print("A small way to explore books through Open Library.")
    print("-" * 52)


def ask_for_search_type():
    print("\nHow would you like to search?")
    print("1. Title")
    print("2. Author")
    print("3. Subject")

    choice = input("Choose 1, 2, or 3: ").strip()

    if choice == "1":
        return "title"
    elif choice == "2":
        return "author"
    elif choice == "3":
        return "subject"
    else:
        return None


def ask_for_search_words(search_type):
    if search_type == "title":
        prompt = "Enter a book title: "
    elif search_type == "author":
        prompt = "Enter an author name: "
    else:
        prompt = "Enter a subject to explore: "

    search_words = input(prompt).strip()
    return search_words


def request_books(search_type, search_words):
    search_parameters = {}
    search_parameters[search_type] = search_words
    search_parameters["limit"] = 40

    try:
        response = requests.get(
            OPEN_LIBRARY_URL,
            params=search_parameters,
            timeout=10
        )

        response.raise_for_status()
        response_data = response.json()

        books = response_data.get("docs", [])

        if isinstance(books, list):
            return books
        else:
            print("The book data came back in an unexpected format.")
            return []

    except requests.exceptions.RequestException:
        print("\nI couldn't reach Open Library right now.")
        print("Check your internet connection and try again.")
        return None
    except ValueError:
        print("\nOpen Library returned data that could not be read.")
        return None


def ask_for_decade_filter():
    print("\nYou can narrow the results by decade.")
    decade_text = input(
        "Enter a decade like 1990, or press Enter to skip: "
    ).strip()

    if decade_text == "":
        return "skip"

    try:
        decade = int(decade_text)
    except ValueError:
        return None

    if decade < 1000 or decade > 2020:
        return None

    if decade % 10 != 0:
        return None

    return decade


def keep_books_from_decade(books, decade):
    matching_books = []
    decade_end = decade + 9

    for book in books:
        year = book.get("first_publish_year")

        if year is not None:
            if isinstance(year, int):
                if year >= decade:
                    if year <= decade_end:
                        matching_books.append(book)

    return matching_books


def make_author_text(book):
    author_names = book.get("author_name")

    if author_names is None:
        return "Unknown author"

    if len(author_names) == 0:
        return "Unknown author"

    author_text = ""

    for index in range(len(author_names)):
        author_text = author_text + author_names[index]

        if index < len(author_names) - 1:
            author_text = author_text + ", "

    return author_text


def show_book_results(books):
    if len(books) == 0:
        print("\nNo books matched that search and filter.")
        return

    print("\n" + "=" * 52)
    print("BOOKS TO EXPLORE")
    print("=" * 52)

    number_to_show = 10

    if len(books) < number_to_show:
        number_to_show = len(books)

    for index in range(number_to_show):
        book = books[index]

        title = book.get("title")
        if title is None:
            title = "Untitled"

        author_text = make_author_text(book)

        publish_year = book.get("first_publish_year")
        if publish_year is None:
            publish_year = "Unknown"

        edition_count = book.get("edition_count")
        if edition_count is None:
            edition_count = "Unknown"

        print("\n" + str(index + 1) + ". " + str(title))
        print("   Author: " + str(author_text))
        print("   First published: " + str(publish_year))
        print("   Editions listed: " + str(edition_count))

    if len(books) > number_to_show:
        print("\nShowing the first " + str(number_to_show) + " matching books.")


def run_program():
    show_welcome_message()

    search_type = ask_for_search_type()

    if search_type is None:
        print("\nThat wasn't a valid option. Run the program again and choose 1, 2, or 3.")
        return

    search_words = ask_for_search_words(search_type)

    if search_words == "":
        print("\nThe search cannot be empty. Run the program again and enter something to search for.")
        return

    books = request_books(search_type, search_words)

    if books is None:
        return

    if len(books) == 0:
        print("\nNo books were found for that search.")
        return

    decade = ask_for_decade_filter()

    if decade is None:
        print("\nThat decade wasn't valid.")
        print("Use a four-digit decade ending in 0, such as 1980 or 2000.")
        return

    if decade != "skip":
        books = keep_books_from_decade(books, decade)

    show_book_results(books)


if __name__ == "__main__":
    run_program()
