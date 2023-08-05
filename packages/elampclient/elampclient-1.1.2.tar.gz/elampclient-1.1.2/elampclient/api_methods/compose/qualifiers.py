from elampclient.api_methods import BaseAPIMethods


class QualiferAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(QualiferAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/qualifiers'

    def list(self, **kwargs):
        return self.client.api_call(
            '{}'.format(self.BASE_URL),
            'get',
            **kwargs
        )

    def list_skills(self, identifier, **kwargs):
        return self.client.api_call(
            '{}/{}/skills'.format(self.BASE_URL, identifier),
            'get',
            **kwargs
        )

    def list_powers(self, identifier, **kwargs):
        return self.client.api_call(
            '{}/{}/powers'.format(self.BASE_URL, identifier),
            'get',
            **kwargs
        )