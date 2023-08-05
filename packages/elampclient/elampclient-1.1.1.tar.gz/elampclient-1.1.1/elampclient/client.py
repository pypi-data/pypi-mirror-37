#!/usr/bin/python
# mostly a proxy object to abstract how some of this works

import json
import logging

from .server import Server
from .exceptions import ParseResponseError, eLampClientNotAuthedError, eLampClientUnsufficentScopesError

from elampclient.api_methods.compose import LibraryAPIMethods, SkillAPIMethods, QualiferAPIMethods, PowerAPIMethods, \
    SkillProfileAPIMethods

LOG = logging.getLogger(__name__)


class eLampClient(object):
    """
        The eLampClient makes API Calls to the `eLamp Web API <https://api.elamp.fr/docs>`_
    """

    def __init__(self, token, proxies=None):
        self.token = token
        self.server = Server(self.token, False, proxies)

    def libraries(self):
        return LibraryAPIMethods(self)

    def skills(self):
        return SkillAPIMethods(self)

    def qualifiers(self):
        return QualiferAPIMethods(self)

    def powers(self):
        return PowerAPIMethods(self)

    def skill_profiles(self):
        return SkillProfileAPIMethods(self)

    def api_call(self, method, http_method, timeout=None, **kwargs):
        """
        Call the eLamp Web API as documented here: https://api.elamp.fr/docs
        :Args:
            method (str): The API Method to call. See
            `the full list here <https://api.elamp.fr/docs>`_
        :Kwargs:
            (optional) kwargs: any arguments passed here will be bundled and sent to the api
            requester as post_data and will be passed along to the API.
            Example::
                sc.server.api_call(
                    "libraries",
                    identifier="LIB12345"
                )
        :Returns:
            str -- returns the text of the HTTP response.
            Examples::
                u'{"ok":true,"purpose":"Testing bots"}'
                or
                u'{"ok":false,"error":"channel_not_found"}'
            See here for more information on responses: https://api.elamp.fr/docs
        """
        response_body = self.server.api_call(method, http_method=http_method, timeout=timeout, **kwargs)
        try:
            result = json.loads(response_body)
        except ValueError as json_decode_error:
            raise ParseResponseError(response_body, json_decode_error)
        if 'ok' in result and result['ok'] is False:
            if 'error' in result and result['error'] == 'not_authed':
                if 'error_details' in result and result['error_details'] == 'unsufficent_scopes':
                    raise eLampClientUnsufficentScopesError(result)
                raise eLampClientNotAuthedError(result)
        return result
