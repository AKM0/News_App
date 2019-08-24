from database import Database
import sqlite3
import unittest
import re

class TestDatabase(unittest.TestCase):

    def test_regex(self):
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(A, B, C)"))
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(A)"))
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(A, B)"))
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(A, B, C, D)"))
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(ABCDEF, B, C)"))
        self.assertTrue(re.match(r"\((\w+,\s)*(\w+)\)", "(A, B_B, C)"))

        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "(A, B, )"))
        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "()"))
        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "A, B, C"))
        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "(ABCDEF, )"))
        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "(A  ,  B,    C)"))
        self.assertFalse(re.match(r"\((\w+,\s)*(\w+)\)", "(A, \nB, C)"))



    def test_exists(self):
        db = Database("test_db.db")
        self.assertTrue(db.exists_in_table("Shopping", "Item", "Soda"))
        self.assertTrue(db.exists_in_table("Shopping", "Item", "Chips"))
        self.assertTrue(db.exists_in_table("Shopping", "Item", "Water"))
        self.assertTrue(db.exists_in_table("Shopping", "Price", "1"))
        self.assertTrue(db.exists_in_table("Shopping", "Price", "0.5"))
        self.assertTrue(db.exists_in_table("Shopping", "Price", "3"))

        self.assertFalse(db.exists_in_table("Shopping", "Item", "CocaCola"))
        self.assertFalse(db.exists_in_table("Shopping", "Item", "Coals"))
        self.assertFalse(db.exists_in_table("Shopping", "Price", "10"))
        self.assertFalse(db.exists_in_table("Shopping", "Price", "0"))
        self.assertFalse(db.exists_in_table("Shopping", "Price", "-1"))

        self.assertRaises(RuntimeError, lambda:db.exists_in_table("", "", "Test"));
        self.assertRaises(RuntimeError, lambda:db.exists_in_table("", "Item", ""));
        self.assertRaises(RuntimeError, lambda:db.exists_in_table("Shop", "", ""));

    def test_insert(self):
        db = Database("test_db.db")
        self.assertTrue(db.insert_row("Shipping", "(Country, State, County)", ("India", "Mumbia", "Borvali")))
        self.assertTrue(db.exists_in_table("Shipping", "Country", "India"))
        self.assertTrue(db.insert_row("Shipping", "(Country, State, County)", ("Japan", "Tokyo", "Spirited")))
        self.assertTrue(db.exists_in_table("Shipping", "State", "Tokyo"))
        self.assertTrue(db.insert_row("Shipping", "(Country, State, County)", ("Russia", "West", "Moscow")))
        self.assertTrue(db.exists_in_table("Shipping", "Country", "Russia"))
        self.assertTrue(db.exists_in_table("Shipping", "State", "West"))
        self.assertTrue(db.exists_in_table("Shipping", "County", "Moscow"))

        self.assertFalse(db.insert_row("Shipping", "(Country, State, County)", ("India", "Mumbia", "Borvali")))
        self.assertTrue(db.exists_in_table("Shipping", "Country", "India"))
        self.assertFalse(db.insert_row("Shipping", "(Country, State, County)", ("Japan", "Tokyo", "Spirited")))
        self.assertTrue(db.exists_in_table("Shipping", "State", "Tokyo"))
        self.assertFalse(db.insert_row("Shipping", "(Country, State, County)", ("Russia", "West", "Moscow")))
        self.assertTrue(db.exists_in_table("Shipping", "Country", "Russia"))
        self.assertTrue(db.exists_in_table("Shipping", "State", "West"))
        self.assertTrue(db.exists_in_table("Shipping", "County", "Moscow"))


unittest.main()
