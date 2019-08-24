# AK M
# December 20, 2018

from newspaper import Article # type: ignore
from newsapi import NewsApiClient # type: ignore
from database import Database
from parse import Parse
from typing import *

import hashlib # for hashing
import datetime
import logging

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

collect_logger = logging.getLogger(__name__)
collect_logger.setLevel(logging.INFO)
collect_logger_handler = logging.FileHandler("collect.log");
collect_logger_handler.setFormatter(logging.Formatter("%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s"))
collect_logger.addHandler(collect_logger_handler)

class Collect:

    SUMMARY_MIN_SENTENCES: int = 3 # do not summarize articles smaller than 3 sentences
    SUMMARY_RATIO: int = 4 # ~1/4 the size of main article
    LANGUAGE_LONG: str = "english"
    ARTICLES_SOFT_LIMIT: int = 100 # fetch 100 articles per update
    DAYS_OLD: int = 1
    SOURCES: List[str] = ["abc-news", "associated-press", "axios", "bloomberg", "business-insider", "cbs-news", "cnbc", "cnn", "espn", "fox-news",
    "mtv-news", "nbc-news", "politico", "reuters", "the-hill", "the-new-york-times", "the-wall-street-journal", "the-washington-post", "time", "usa-today"]
    PAGE_SIZE: int = 100
    SENTENCES_PERCENTAGE: int = 20 # 20 percent
    SENTENCES_NUM: int = 5; # target 5 sentence length summaries
    news_api = NewsApiClient(api_key = "") # TODO removed API key

    def __init__(self, language: str, country: str, database: Database) -> None:
        collect_logger.debug("Initialzing Collect() for {} and {}".format(language, country))
        self.language: str = language
        self.country: str = country
        self.articles: MutableMapping = {}
        self.summarized_articles: List = []
        self.database: Database = database

        self.stemmer = Stemmer(Collect.LANGUAGE_LONG)
        self.summarizer = Summarizer(self.stemmer)
        self.tokenizer = Tokenizer(Collect.LANGUAGE_LONG)
        self.summarizer.stop_words = get_stop_words(Collect.LANGUAGE_LONG)


    # get articles using News API based on defined filters (on sources, langauge, time, etc)
    def get_filtered_articles(self) -> None:
        collect_logger.info("Requesting top articles with {} and {} source criteria".format(self.language, self.country))

        yesterday = (datetime.datetime.now() - datetime.timedelta(days = Collect.DAYS_OLD))
        yesterday_date: str = str(yesterday.strftime("%Y-%m-%d"))

        response = Collect.news_api.get_everything(language = self.language, sources = ",".join(Collect.SOURCES), from_param = yesterday_date, page_size = Collect.PAGE_SIZE)

        if (response["status"] == "ok"):
            collect_logger.info("Articles with souce criteria successfully returned")
            self.articles = response["articles"]

            if (len(self.articles) > Collect.ARTICLES_SOFT_LIMIT):
                collect_logger.warning("Truncating articles due to soft limit of {} reached from {}".format(str(Collect.ARTICLES_SOFT_LIMIT), str(len(self.articles))))
                self.articles = self.articles[0:Collect.ARTICLES_SOFT_LIMIT]

        else:
            collect_logger.error(response["code"] + " " + response["message"])

    # get articles based on popularity/trending
    def get_top_headlines(self) -> None:
        # make request for trending articles
        collect_logger.info("Requesting top articles with {} and {}".format(self.language, self.country))

        response = Collect.news_api.get_top_headlines(language = self.language, country = self.country, page_size = Collect.PAGE_SIZE)

        if (response["status"] == "ok"):
            collect_logger.info("Articles successfully returned")
            self.articles = response["articles"]

            if (len(self.articles) > Collect.ARTICLES_SOFT_LIMIT):
                collect_logger.warning("Truncating articles due to soft limit of {} reached from {}".format(str(Collect.ARTICLES_SOFT_LIMIT), str(len(self.articles))))
                self.articles = self.articles[0:Collect.ARTICLES_SOFT_LIMIT]

        else:
            collect_logger.error(response["code"] + " " + response["message"])


    # summarize single article
    def summarize(self, article):
        collect_logger.debug("Summarizing article {}".format(article["title"]))

        n3k_article = Article(article["url"])
        n3k_article.download()
        n3k_article.parse()

        article["text"]: str = n3k_article.text
        parser = PlaintextParser.from_string(article["text"], self.tokenizer)

        # calculate length of article summary based on existing length
        # summarize longer articles more than shorter articles
        sentences_num: int = int((article["text"].count(". ") ** 0.5)/Collect.SUMMARY_RATIO) + Collect.SUMMARY_MIN_SENTENCES

        text: List[str] = []
        for sentence in self.summarizer(parser.document, sentences_num):
            text.append(str(sentence).strip())

        summary: str = " ".join(text)

        article["summary"]: str = Parse.parse_article_summary(summary)
        article["accessedAt"]: str = str(int(datetime.datetime.now().timestamp()))

        if (article["summary"] is None) or (len(article["summary"]) <= 0):
            collect_logger.error("Summary for {} failed".format(article["title"]))
            raise RuntimeError("Summary for {} failed".format(article["title"]))

        return article

    # summarize all articles fetched
    def summarize_articles(self) -> None:
        collect_logger.info("Summarizing all {} articles".format(str(len(self.articles))))

        for article in self.articles:
            try:
                parsed_article: MutableMapping[str, str] = Parse.parse_article(article)

                input: str = parsed_article["source"] + parsed_article["title"] + parsed_article["publishedAt"]
                output = hashlib.sha256(input.encode())
                sha256: str = output.hexdigest()

                # only summarize articles not in database
                if not self.database.exists_in_table("Articles", "Hash", sha256):
                    collect_logger.debug("Article {} not already in database".format(parsed_article["title"]))
                    parsed_article["hash"] = sha256

                    try:
                        summarized_articles = self.summarize(parsed_article)
                        self.summarized_articles.append(summarized_articles)
                    except Exception as e:
                        collect_logger.error("Failed to summarize article {} with error {}".format(parsed_article["title"], str(e)))

            except Exception as e:
                collect_logger.error("Failed to summarize article")


        collect_logger.info("Summarized {} new articles".format(str(len(self.summarized_articles))))

    # entry
    def get_summarized_articles(self):
        collect_logger.debug("Retrieving summarized articles")
        self.get_filtered_articles()
        self.summarize_articles()
        return self.summarized_articles
