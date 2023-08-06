from elampclient.api_methods import BaseAPIMethods


class SkillProfileAPIMethods(BaseAPIMethods):

    def __init__(self, client):
        super(SkillProfileAPIMethods, self).__init__(client)
        self.BASE_URL = 'v1/profiles'

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

    def match(self, identifier=None, include_reasons=False, **kwargs):
        include_reasons_query = 'false' if include_reasons is False else 'true'
        if identifier is not None:
            return self.client.api_call(
                '{}/matching?profile_id={}&include_reasons={}'.format(self.BASE_URL, identifier, include_reasons_query),
                'get',
                **kwargs
            )
        else:
            return self.client.api_call(
                '{}/matching?include_reasons={}'.format(self.BASE_URL, include_reasons_query),
                'get',
                **kwargs
            )
