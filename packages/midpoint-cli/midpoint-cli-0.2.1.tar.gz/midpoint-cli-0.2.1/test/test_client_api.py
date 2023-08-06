import unittest

from midpoint_cli.mpclient import RestApiClient


class ClientApiTest(unittest.TestCase):
    def test_url_sanitization(self):
        client = RestApiClient('http://localhost:8080/dumbo', '', '')
        self.assertEqual(client.url, 'http://localhost:8080/midpoint/')

    def test_rest_types(self):
        client = RestApiClient('http://localhost:8080/dumbo', '', '')
        self.assertEqual(client.resolve_rest_type('task'), 'tasks')

        try:
            client.resolve_rest_type('bogus')
            self.fail()
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
