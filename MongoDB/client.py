#!/usr/bin/env python3
import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flight.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("BOOKS_API_URL", "http://localhost:8000")



def print_book(book):
    for k in book.keys():
        print(f"{k}: {book[k]}")
    print("="*50)

def list_books(to_airpor, month):
    suffix = "/flight"
    endpoint = BOOKS_API_URL + suffix
    params = {
        "to_airport": to_airpor,
        "month": month
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for book in json_resp:
            print_book(book)
    else:
        print(f"Error: {response}")


def get_book_by_id(id):
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_book(json_resp)
    else:
        print(f"Error: {response}")




def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-i", "--id",
            help="Provide a book ID which related to the book action", default=None)
    parser.add_argument("-t", "--to_airport",
            help="Search parameter to look for books with average rating equal or above the param (0 to 5)", default=None)
    parser.add_argument("-m", "--month",
            help="Search parameter to look for books with average rating equal or above the param (0 to 5)", default=None)


    args = parser.parse_args()

    if args.id and not args.action in ["get", "update"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.to_airport and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        exit(1)

    if args.action == "search":
        list_books(args.to_airport, args.month)
    elif args.action == "get" and args.id:
        get_book_by_id(args.id)
   

if __name__ == "__main__":
    main()