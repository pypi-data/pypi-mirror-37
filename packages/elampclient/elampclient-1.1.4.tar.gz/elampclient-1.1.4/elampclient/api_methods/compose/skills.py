from elampclient.api_methods import BaseAPIMethods


class SkillAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(SkillAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/skills'

    def list(self, skill=None, **kwargs):
        if skill:
            return self.client.api_call(
                '{}?parent={}'.format(self.BASE_URL, skill),
                'get',
                **kwargs
            )
        else:
            return self.client.api_call(
                '{}'.format(self.BASE_URL),
                'get',
                **kwargs
            )

    def list_recents(self, **kwargs):
        return self.client.api_call(
            '{}/recents'.format(self.BASE_URL),
            'get',
            **kwargs
        )

    def search(self, query, **kwargs):
        return self.client.api_call(
            '{}/search?q={}'.format(self.BASE_URL, query),
            'get',
            **kwargs
        )

    def list_qualifiers(self, identifier, **kwargs):
        return self.client.api_call(
            '{}/{}/qualifiers'.format(self.BASE_URL, identifier),
            'get',
            **kwargs
        )
