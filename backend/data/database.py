# AK M
# December 19, 2018

from typing import *
import sqlite3
import logging
import re

database_logger = logging.getLogger(__name__)
database_logger.setLevel(logging.INFO)
database_logger_handler = logging.FileHandler("database.log");
database_logger_handler.setFormatter(logging.Formatter("%(levelname)s:%(asctime)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s"))
database_logger.addHandler(database_logger_handler)

class Database:

    def __init__(self, database: str) -> None:
        database_logger.debug("Initialzing database with {}".format(database))

        if (database is None) or (len(database) <= 0):
            database_logger.error("Database name not provided")
            raise RuntimeError("Database name not provided")

        self.database: str = database
        self.conn: sqlite3.Connection = sqlite3.connect(self.database)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

        if (self.conn is None) or (self.cursor is None):
            database_logger.error("Failed to properly initialize database")
            raise RuntimeError("Failed to properly initialize database")

        database_logger.debug("Sucessfully initialized {}".format(self.database))

    def exists_in_table(self, table: str, column: str, element: Iterable[Any]) -> bool:
        database_logger.debug("Checking to see if {} exists in {} of {}".format(str(element), column, table))

        if (table is None) or (column is None) or (element is None) or (len(table) <= 0) or (len(column) <= 0):
            database_logger.error("Invalid argument passed to exists in table")
            raise RuntimeError("Invalid argument passed to exists in table")

        query: str = "SELECT EXISTS(SELECT 1 FROM {} WHERE {} = ?)".format(table, column)
        self.cursor.execute(query, (element,))

        response: List = self.cursor.fetchone()

        if (response is None):
            database_logger.error("Bad exists in table response")
            raise RuntimeError("Bad exists in table response")

        result: int = response[0]
        if (result is None):
            database_logger.error("Bad exists in table result")
            raise RuntimeError("Bad exists in table result")

        exists: bool = (result > 0)

        database_logger.debug("{}.{} in {} is {}".format(column, str(element), table, exists))
        return exists

    def get_column(self, table: str, column) -> List:
        database_logger.debug("Getting all all values of column {} in table {}".format(column, table))

        if (table is None) or (column is None) or (len(table) <= 0) or (len(column) <= 0):
            database_logger.error("Invalid argument passed to get column")
            raise RuntimeError("Invalid argument passed to get column")

        query: str = "SELECT {} FROM {}".format(column, table)
        self.cursor.execute(query)

        response: List = self.cursor.fetchall()

        if (response is None):
            database_logger.error("Bad get column response")
            raise RuntimeError("Bad get column response")

        result: List[str] = response[0]
        if (result is None):
            database_logger.error("Bad exists in table result")
            raise RuntimeError("Bad exists in table result")

        return result

    # TODO ensure column and row fields exists before insertion
    def insert_row(self, table: str, row_format: str, row: Iterable[Any]) -> bool:
        database_logger.debug("Inserting {} into {} of {}".format(str(row), row_format, table))

        if (table is None) or (row_format is None) or (row is None) or (len(table) <= 0) or (len(row_format) <= 0):
            database_logger.error("Invalid argument passed to insert in table")
            raise RuntimeError("Invalid argument passed to insert in table")

        if (not re.match(r"\((\w+,\s)*(\w+)\)", row_format)):
            database_logger.error("Invalid row_format")
            raise RuntimeError("Invalid row_format")

        values: str = re.sub("\w+", "?", row_format)

        try:
            query: str = "INSERT INTO {} {} VALUES {}".format(table, row_format, values)
            self.cursor.execute(query, row)
            self.conn.commit()
            database_logger.debug("Inserting {} into {} of {} was successful".format(str(row), row_format, table))
            return True
        except Exception as e:
            database_logger.error("Inserting {} into {} of {} failed with {}".format(str(row), row_format, table, str(e)))
            return False

    def __del__(self):
        self.conn.close()
