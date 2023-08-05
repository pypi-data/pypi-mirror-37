import unittest
import operator

from elampclient import eLampClient
from elampclient.auth import jwt_auth


class eLampClientAuthTest(unittest.TestCase):

    def test_jwt_auth(self):
        jwt , expiration = jwt_auth.JWTAuth(
            'APK1b',
            'BOT1f',
            '/path/to/my/private_key.pem'
        ).authenticate()
        print(jwt, expiration)
        # self.assertEqual(response, False)