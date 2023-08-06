import json
import jwt
import datetime
import uuid
import requests

from elampclient.exceptions import eLampClientInvalidCredentialsError

AUTH_ENDPOINT = 'https://www.elamp.fr/oauth/token'


class JWTAuth(object):
    """
        jwt, expiration = JWTAuth(
            'APK15124',
            'BOT13539',
            '/path/to/my/private_key.pem'
        ).authenticate()
    """

    def __init__(self, client_id, subject_id, path_to_private_key, auth_endpoint=AUTH_ENDPOINT):
        self.client_id = client_id
        self.subject_id = subject_id
        self.private_key = self.get_private_key(path_to_private_key)
        self.assertion = None
        self.auth_endpoint = auth_endpoint

    def get_private_key(self, path):
        key = None
        with open(path, 'rb') as key_file:
            key = key_file.read()
        if key:
            return key

    def make_assertion(self):
        expire_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        payload = {
            'iss': self.client_id,
            'sub': self.subject_id,
            'aud': 'https://elamp.fr/oauth/token',
            'jti': str(uuid.uuid1()),
            'exp': expire_at,
            'iat': datetime.datetime.utcnow()
        }
        self.assertion = jwt.encode(payload, self.private_key, algorithm='RS256')

    def authenticate(self):
        if self.assertion is None:
            self.make_assertion()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'client_id': self.client_id,
            'assertion': self.assertion
        }
        response = requests.request(
            'post',
            self.auth_endpoint,
            headers=headers,
            data=post_data,
            timeout=60
        )
        response_json = json.loads(response.text)
        response_json["headers"] = dict(response.headers)
        if response.status_code == 200 and 'access_token' in response_json:
            return response_json['access_token'], response_json['expires_in']
        else:
            raise eLampClientInvalidCredentialsError(response_json)
