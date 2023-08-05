import requests
import json
import six
import sys
import platform
from .version import __version__


class eLampRequest(object):
    def __init__(self, proxies=None):

        client_name = __name__.split('.')[0]
        client_version = __version__  # Version is returned from version.py

        # Construct the user-agent header with the package info, Python version and OS version.
        self.default_user_agent = {
            "client": "{0}/{1}".format(client_name, client_version),
            "python": "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info),
            "system": "{0}/{1}".format(platform.system(), platform.release())
        }

        self.custom_user_agent = None
        self.proxies = proxies

    def get_user_agent(self):
        # Check for custom user-agent and append if found
        if self.custom_user_agent:
            custom_ua_list = ["/".join(client_info) for client_info in self.custom_user_agent]
            custom_ua_string = " ".join(custom_ua_list)
            self.default_user_agent['custom'] = custom_ua_string

        # Concatenate and format the user-agent string to be passed into request headers
        ua_string = []
        for key, val in self.default_user_agent.items():
            ua_string.append(val)

        user_agent_string = " ".join(ua_string)
        return user_agent_string

    def append_user_agent(self, name, version):
        if self.custom_user_agent:
            self.custom_user_agent.append([name.replace("/", ":"), version.replace("/", ":")])
        else:
            self.custom_user_agent = [[name, version]]

    def do(self, token, request="?", http_method='post', post_data=None, domain="api.elamp.fr", timeout=None):
        """
        Perform a POST request to the eLamp Web API
        Args:
            token (str): your authentication token
            request (str): the method to call from the eLamp API.
            timeout (float): stop waiting for a response after a given number of seconds
            post_data (dict): key/value arguments to pass for the request.
            domain (str): if for some reason you want to send your request to something other
                than api.elamp.fr
        """

        url = 'https://{0}/{1}'.format(domain, request)

        # Override token header if `token` is passed in post_data
        if post_data is not None and "token" in post_data:
            token = post_data['token']

        # Set user-agent and auth headers
        headers = {
            'user-agent': self.get_user_agent(),
            'Authorization': 'Bearer {}'.format(token)
        }

        post_data = post_data or {}

        # Convert any params which are list-like to JSON strings
        # Example: `attachments` is a dict, and needs to be passed as JSON
        for k, v in six.iteritems(post_data):
            if isinstance(v, (list, dict)):
                post_data[k] = json.dumps(v)

        # Submit the request
        print(url)
        print(post_data)
        print(http_method)
        return requests.request(
            http_method,
            url,
            headers=headers,
            data=post_data,
            timeout=timeout,
            proxies=self.proxies
        )
