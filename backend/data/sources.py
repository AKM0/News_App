# AK M
# December 27th, 2018

from newsapi import NewsApiClient # type: ignore
from database import Database
from collect import Collect
from typing import *
import logging

source_logger = logging.getLogger(__name__)
source_logger.setLevel(logging.INFO)
source_logger_handler = logging.FileHandler("source.log");
source_logger_handler.setFormatter(logging.Formatter("%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s"))
source_logger.addHandler(source_logger_handler)

source_logger.info("Requested sources")
database = Database("main.db")

news_api = NewsApiClient(api_key = "") # TODO removed API key
ROW_FORMAT: str = "(Id, Name, Url, Category, Language, Country)"

def insert_into_database(format: str, source: Tuple) -> None:
    source_logger.debug("Inserting into database {}".format(source[0]))
    id: str = source[0]

    try:
        if not database.exists_in_table("Sources", "Id", id):
            database.insert_row("Sources", format, source)
    except Exception as e:
        logging.error("Inserting into database failed: {} ".format(str(e)))

def get_all_sources():
    source_logger.info("Getting all sources")

    response = news_api.get_sources()

    if (response["status"] == "ok"):
        source_logger.info("Sources successfully returned")
        return response["sources"]
    else:
        source_logger.error(response["code"] + " " + response["message"])

filtered_sources: List = []
all_sources: List = get_all_sources()
for source in all_sources:
    if (source["language"] == "en" and source["country"] == "us"):
        filtered_sources.append(source["id"])

    row: Tuple = (source["id"], source["name"], source["url"], source["category"], source["language"], source["country"])
    insert_into_database(ROW_FORMAT, row)

#print(filtered_sources)
