import unittest
from unittest import mock
from . import client
from .exceptions import ConfigError

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs.get('headers', {}).get('X-Config-Key') == 'good-config-key':
        return MockResponse({ 'someKey': 'someVal' }, 200)

    return MockResponse({ 'error': 'No config was found for the provided key' }, 404)

class MothershipClientTestCase(unittest.TestCase):
    
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_good_init(self, mock_get):
        config = client.init({ 'key': 'good-config-key' })
        
        self.assertEqual(config['someKey'], 'someVal')
        
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_bad_init(self, mock_get):
        self.assertRaises(ConfigError, client.init, { 'key': 'bad-config-key' })
        
if __name__ == '__main__':
    unittest.main()