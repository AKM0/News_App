# AK M
# December 19, 2018
from typing import *
import datetime
import logging
import re

parse_logger = logging.getLogger(__name__)
parse_logger.setLevel(logging.INFO)
parse_logger_handler = logging.FileHandler("parse.log");
parse_logger_handler.setFormatter(logging.Formatter("%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s"))
parse_logger.addHandler(parse_logger_handler)

class Parse:

    EPOCH = datetime.datetime(1970, 1, 1);
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    @staticmethod
    def parse_url(url: str) -> str:
        parse_logger.debug("Parsing url")
        return url

    @staticmethod
    def parse_title(title: str) -> Tuple[str, str]:
        parse_logger.debug("Parsing title")
        arr: List[str] = title.rsplit(" - ")

        if len(arr) <= 1:
            parse_logger.debug("Article " + title + " provided with no source")
            return (arr[0].strip(), "Unknown Source")
        elif len(arr) == 2:
            parse_logger.debug("Article title successfully parsed")
            return (arr[0].strip(), arr[1].strip())
        else:
            parse_logger.debug("Article title successfully parsed")
            source: str = arr[-1]
            parsed_title: str = re.sub(" - " + source, "", title)
            return (parsed_title.strip(), source.strip())

    @staticmethod
    def parse_authors(authors: str) -> str:
        parse_logger.debug("Parsing authors")
        if authors is None:
            return "Unknown Author"
        else:
            return authors

    @staticmethod
    def parse_publishedAt(publishedAt: str) -> str:
        parse_logger.debug("Parsing publish datetime")
        if (publishedAt is None) or (len(publishedAt) <= 0):
            return "Unknown publish date"
        else:
            publish_time_formatted = datetime.datetime.strptime(publishedAt, Parse.DATETIME_FORMAT)
            time_since_epoch: int = int((publish_time_formatted - Parse.EPOCH).total_seconds())
            return str(time_since_epoch)

    @staticmethod
    def parse_article_summary(article_text: str) -> str:
        parse_logger.debug("Parsing article summary")

        parsed_article_text: str = re.sub("\n", " ", article_text)
        parsed_article_text = re.sub("\s+", " ", parsed_article_text)
        parsed_article_text = parsed_article_text.strip()

        return parsed_article_text


    @staticmethod
    def parse_article(article) -> MutableMapping[str, str]:
        parse_logger.debug("Parsing all article fields")

        parsed_article: MutableMapping[str, str] = {}

        parsed_article["url"] = Parse.parse_url(article["url"])

        # title and source
        if (article["source"]["name"] is None) or (len(article["source"]["name"]) <= 0):
            parsed_title: Tuple[str, str] = Parse.parse_title(article["title"])
            parsed_article["title"] = parsed_title[0]
            parsed_article["source"] = parsed_title[1]
        else:
            parsed_article["title"] = article["title"]
            parsed_article["source"] = article["source"]["name"]

        parsed_article["authors"] = Parse.parse_authors(article["author"])
        parsed_article["publishedAt"] = Parse.parse_publishedAt(article["publishedAt"])

        if (parsed_article["url"] is None) or (len(parsed_article["url"]) <= 0):
            parse_logger.error("No url for article")
            raise RuntimeError("No url for article")

        if (parsed_article["title"] is None) or (len(parsed_article["title"]) <= 0):
            parse_logger.error("No title for article {}".format(article["url"]))
            raise RuntimeError("No title for article {}".format(article["url"]))

        return parsed_article
