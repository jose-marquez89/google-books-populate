import unittest
import requests

from populate import gb_url, request_and_execute


class TestPopulateFunctions(unittest.TestCase):

    def test_get_url(self):
        """Test for valid url creation"""
        publisher = "Houghton Mifflin"
        index_no = 40

        url = gb_url(publisher, index=index_no)
        res = requests.get(url)

        url_no_index = gb_url(publisher)
        res_no_index = requests.get(url_no_index)

        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_no_index.status_code, 200)
        self.assertIn('items', data.keys())

    def test_request_execute(self):
        """
        Test the function that gets data and executes queries
        (this is the function that will be used in multi-threading
        DATABASE_URL environment variable must exist to pass test
        """

        self.assertTrue(
            request_and_execute("Simon & Schuster", 40)
        )
