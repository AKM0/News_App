# AK M
# December 17, 2018
from typing import *
from database import Database
from collect import Collect
import logging

database = Database("main.db")
collect = Collect("en", "us", database)

logging.basicConfig(filename = "backend.log", level = logging.INFO,
format = "%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s")
# LEVEL:TIME:FILE:FUNCTION:LINE:MESSAGE

# TODO loop on a regular basis
def insert_into_database(format: str, article: Tuple) -> None:
    # check to see if article is not already in database by checking article hash
    logging.debug("Inserting into database {}".format(article[6]))
    hash: str = article[0]
    try:
        if not database.exists_in_table("Articles", "Hash", hash):
            database.insert_row("Articles", format, article)
    except Exception as e:
        logging.error("Inserting into database failed: {} ".format(str(e)))


# collect articles using news api
summarized_articles = collect.get_summarized_articles()
logging.debug("Successfully summarized articles")

# loop through all fetched articles and insert into database
for article in summarized_articles:
    # construct tuple for insertion
    row_format: str = "(Hash, Url, DateAccess, Source, DatePublish, Authors, Title, Summary)"
    row: Tuple = (article["hash"], article["url"], article["accessedAt"], article["source"],
    article["publishedAt"], article["authors"], article["title"], article["summary"])

    insert_into_database(row_format, row)
