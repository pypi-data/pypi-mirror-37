import json
import logging
import time
import random

# from requests.packages.urllib3.util.url import parse_url
# from ssl import SSLError

from elampclient.elamprequest import eLampRequest


class Server(object):

    def __init__(self, token, connect=True, proxies=None):
        """
            The Server object owns the websocket connection and all attached channel information.
        """

        # eLamp client configs
        self.token = token
        self.proxies = proxies
        self.api_requester = eLampRequest(proxies=proxies)

        # Workspace metadata
        self.username = None
        self.tenant = None
        self.login_data = None
        # self.users = SearchDict()
        # self.channels = SearchList()

    def api_call(self, api_method, http_method='post', timeout=None, **kwargs):
        """
        Call the eLamp Web API as documented here: https://api.elamp.fr/docs
        :Args:
            method (str): The API Method to call. See here for a list: https://api.elamp.fr/docs
        :Kwargs:
            (optional) timeout: stop waiting for a response after a given number of seconds
            (optional) kwargs: any arguments passed here will be bundled and sent to the api
            requester as post_data
                and will be passed along to the API.
        Example::
            sc.server.api_call(
                "channels.setPurpose",
                channel="CABC12345",
                purpose="Writing some code!"
            )
        Returns:
            str -- returns HTTP response text and headers as JSON.
            Examples::
                u'{"ok":true,"purpose":"Testing bots"}'
                or
                u'{"ok":false,"error":"channel_not_found"}'
            See here for more information on responses: https://api.elamp.fr/docs
        """
        response = self.api_requester.do(self.token, api_method, http_method, timeout=timeout, **kwargs)
        response_json = json.loads(response.text)
        response_json["headers"] = dict(response.headers)
        response_json['status_code'] = response.status_code

        return json.dumps(response_json)