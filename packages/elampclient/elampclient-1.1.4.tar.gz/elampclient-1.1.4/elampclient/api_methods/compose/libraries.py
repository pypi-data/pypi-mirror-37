from elampclient.api_methods import BaseAPIMethods


class LibraryAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(LibraryAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/libraries'

    def list(self, skill=None, **kwargs):
        if skill:
            return self.client.api_call('{}?parent={}'.format(self.BASE_URL, skill), 'get', **kwargs)
        else:
            return self.client.api_call('{}'.format(self.BASE_URL), 'get', **kwargs)

    def subscribe(self, identifier, **kwargs):
        return self.client.api_call('{}/{}/subscribe'.format(self.BASE_URL, identifier), 'post', **kwargs)

    def unsubscribe(self, identifier, **kwargs):
        return self.client.api_call('{}/{}/unsubscribe'.format(self.BASE_URL, identifier), 'post', **kwargs)