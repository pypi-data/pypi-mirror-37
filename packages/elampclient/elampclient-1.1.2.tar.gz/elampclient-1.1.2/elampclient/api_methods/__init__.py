
class BaseAPIMethods(object):

    def __init__(self, client):
        if client is not None:
            self.client = client
        else:
            raise ValueError()
        self.BASE_URL = '/'

    def get(self, identifier, **kwargs):
        return self.client.api_call('{}/{}'.format(self.BASE_URL, identifier), 'get', **kwargs)

    def create(self, data, **kwargs):
        return self.client.api_call('{}'.format(self.BASE_URL), 'post', post_data=data, **kwargs)

    def update(self, identifier, data, **kwargs):
        return self.client.api_call('{}/{}'.format(self.BASE_URL, identifier), 'patch', post_data=data, **kwargs)

    def delete(self, identifier, **kwargs):
        return self.client.api_call('{}/{}'.format(self.BASE_URL, identifier), 'delete', **kwargs)