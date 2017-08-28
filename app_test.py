import os
import app
import unittest
import tempfile


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_text_protocol(self):
        rv = self.app.get('/')
        assert b'JSON Posted' in rv.data

if __name__ == '__main__':
    unittest.main()