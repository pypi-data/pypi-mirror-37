from elampclient.api_methods import BaseAPIMethods


class UserAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(UserAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/users'

    def list(self, **kwargs):
        return self.client.api_call(
            '{}'.format(self.BASE_URL),
            'get',
            **kwargs
        )

    def search(self, query, **kwargs):
        return self.client.api_call(
            '{}/search?q={}'.format(self.BASE_URL, query),
            'get',
            **kwargs
        )
