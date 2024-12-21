import unittest
from src.utilities.swen610_db_utils import exec_sql_file

class NutrikitSetupDB(unittest.TestCase) :
    # setup test date from sql file and also sample rows
    def test_0_setup_tables(self) :
        print("Setting up test data...")
        result = exec_sql_file("data/setup_tables.sql")
