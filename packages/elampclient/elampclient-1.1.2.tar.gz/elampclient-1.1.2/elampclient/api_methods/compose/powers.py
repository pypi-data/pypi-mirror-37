from elampclient.api_methods import BaseAPIMethods


class PowerAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(PowerAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/powers'

    def list(self, user=None, **kwargs):
        if user is not None:
            return self.client.api_call(
                '{}?user={}'.format(self.BASE_URL, user),
                'get',
                **kwargs
            )
        else:
            return self.client.api_call(
                '{}'.format(self.BASE_URL),
                'get',
                **kwargs
            )

    def create(self, user=None, skill=None, data=None, **kwargs):
        body = dict()
        if user is not None:
            body['resource'] = user
        if skill is not None:
            body['skill'] = skill
        # TODO: use data parameters
        return self.client.api_call(
            '{}'.format(self.BASE_URL),
            'post',
            post_data=body
        )

    def list_qualifiers(self, identifier, **kwargs):
        return self.client.api_call(
            '{}/{}/qualifiers'.format(self.BASE_URL, identifier),
            'get',
            **kwargs
        )

    def list_powers(self, identifier, **kwargs):
        return self.client.api_call(
            '{}/{}/powers'.format(self.BASE_URL, identifier),
            'get',
            **kwargs
        )