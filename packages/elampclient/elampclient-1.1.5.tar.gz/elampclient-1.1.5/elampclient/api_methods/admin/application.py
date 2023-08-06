from elampclient.api_methods import BaseAPIMethods


class ApplicationAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(ApplicationAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/applications'

    def info(self, **kwargs):
        return self.client.api_call('{}/infos'.format(self.BASE_URL), 'get', **kwargs)