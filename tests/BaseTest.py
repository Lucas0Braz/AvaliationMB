import unittest
#todo tests with unittest
from app import app
from db import Base


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = Base.get_db()


    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)