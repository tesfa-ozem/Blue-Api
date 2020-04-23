import os
import unittest
import numpy as np
import pandas as pd
from blue import create_app, db
from blue.logic.logic import Logic
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(Config):
    TESTING = True


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_something(self):
        logic = Logic()
        print(logic.get_current_week_sales())


if __name__ == '__main__':
    unittest.main()
