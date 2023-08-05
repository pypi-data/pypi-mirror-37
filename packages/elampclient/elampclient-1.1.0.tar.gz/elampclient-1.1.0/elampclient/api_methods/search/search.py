from elampclient.api_methods import BaseAPIMethods


class SearchAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(SearchAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/search'

    def list(self, skill=None, **kwargs):
        if skill:
            return self.client.api_call('{}?parent={}'.format(self.BASE_URL, skill), 'get', **kwargs)
        else:
            return self.client.api_call('{}'.format(self.BASE_URL), 'get', **kwargs)
