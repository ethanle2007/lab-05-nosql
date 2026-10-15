#!/usr/bin/env python3
"""Print a report of books linked to each author in the bookstore database."""

import logging
import os

import pymongo

# credentials from the environment
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

# author ids to report on
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

# logging configuration
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    """Connect to Atlas and print each listed author with their books."""
    # fail early with a clear message if any variable is missing
    if not (MONGODB_ATLAS_URL and MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD):
        logging.error(
            "Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD."
        )
        return

    client = None
    try:
        # open the client
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        # force a real round trip so a bad URL or password fails here
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas")

        # select the database and the two collections
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # count how many of the listed authors actually exist
        total = authors.count_documents({"_id": {"$in": AUTHOR_IDS}})
        print(f"Authors: {total}")

        # print each listed author with their books
        for author_id in AUTHOR_IDS:
            # find the author
            author = authors.find_one({"_id": author_id})
            # if the author is not found, log a warning and continue
            if author is None:
                logging.warning("No author found with _id %s", author_id)
                continue

            # print the author's name
            print(f"\n{author['name']}")

            # print each book by the author
            for book in books.find({"author_ids": author["_id"]}).sort(
                "published_year", 1
            ):
                print(f"  {book['title']} ({book['published_year']})")
    except pymongo.errors.PyMongoError as err:
        logging.error("MongoDB error: %s", err)
    finally:

        if client is not None:
            client.close()
            logging.info("Connection closed")


if __name__ == "__main__":
    main()
