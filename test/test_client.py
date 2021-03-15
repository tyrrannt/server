import getpass
import unittest
from socket import *

from utils.utility import serialize_json, deserialize_json


class TestErrors(unittest.TestCase):

    def test_serialize_json(self):
        username = getpass.getuser()
        ip_address = gethostbyname(getfqdn())
        test_string = '{"action": "authenticate", "user": {"username": "' + username + '", "ip_address": "' \
                      + ip_address + '"}, "message": "123"}'
        self.assertEqual(serialize_json(0, "123"), test_string.encode('utf-8'))

    def test_deserialize_json(self):
        dicts = {'action': 'message', 'user': {'username': 'Admin', 'ip_address': '192.168.56.1'}, 'message': '123'}
        bytes = b'{"action": "message", "user": {"username": "Admin", "ip_address": "192.168.56.1"}, "message": "123"}'
        self.assertEqual(deserialize_json(bytes), dicts)


if __name__ == "__main__":
    unittest.main()
