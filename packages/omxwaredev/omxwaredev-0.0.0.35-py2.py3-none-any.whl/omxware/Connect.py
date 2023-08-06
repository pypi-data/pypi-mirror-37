import requests
import simplejson as json
import urllib3

from omxware.Config import Configuration
from omxware.ServiceException import ServiceException

# Disable the SSL warning
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Connection:
    """OMXWare connect class"""
    hosturl = ''
    token = ''
    # session: requests.Session
    # config: Configuration
    session: requests.Session
    config: Configuration
    headers: {}

    # def __init__(self, config: Configuration):
    def __init__(self, config):
        self.config = config
        self.hosturl = config.getServerURL()
        self.token = config.getAuthToken()

    def __setHeaders(self):
        self.token = self.config.getAuthToken()
        user_email = self.config.getUserInfo().get('email')
        self.headers = {
                        'From': ''+user_email,
                        'User-Agent': 'application/json',
                        'Authorization': 'Bearer '+self.token
                      }

    def connect(self):
        self.token = self.config.getAuthToken()

        """Connect to the OMXWare services"""
        self._session = requests.Session()
        self.__setHeaders()

    def getConfig(self):
        return self.config

    def get(self, methodurl, headers: {}, payload=None):
        """Issue a HTTP GET request

        Arguments:
          methodurl -- relative path to the GET method
          headers -- HTTP headers
          payload -- (optional) additional payload (HTTP body)
        """

        self.connect()

        if self._session is None:
            raise Exception("No connection has been established")

        headers.update(self.headers)

        # print(self.hosturl)
        # print(methodurl)
        # print(payload)
        # print(headers)

        response = self._session.get(self.hosturl + methodurl, verify=False, params=payload, headers=headers)

        # print(response.status_code)
        # print(response.text)

        if response.status_code < 200 or response.status_code >= 300:
            raise self._process_http_response(response)
        return response

    def post(self, methodurl, parameters=None, headers={}, files=None):
        """Issue a HTTP POST request

        Arguments:
        methodurl -- relative path to the POST method
        parameters -- (optional) form parameters
        headers -- (optional) HTTP headers
        files -- (optional) multi-part form file content
        """

        self.connect()

        if self._session is None:
            raise Exception("No connection has been established")

        headers.update(self.headers)

        # print(self.hosturl)
        # print(methodurl)
        # print(parameters)
        # print(headers)

        response = self._session.post(self.hosturl + methodurl, data=parameters, verify=False, headers=headers,
                                      files=files)

        # print(response.status_code)
        # print(response.text)

        if response.status_code < 200 or response.status_code >= 300:
            raise self._process_http_response(response)
        return response

    def delete(self, methodurl, headers={}, payload=None):
        """Issue a HTTP DELETE request

        Arguments:
        methodurl -- relative path to the POST method
        headers -- HTTP headers
        payload -- (optional) additional payload (HTTP body)
        """

        self.connect()

        if self._session is None:
            raise Exception("No connection has been established")

        headers.update(self.headers)

        response = self._session.delete(self.hosturl + methodurl, verify=False, params=payload, headers=headers)

        if response.status_code < 200 or response.status_code >= 300:
            raise self._process_http_response(response)
        return response

    def disconnect(self):
        """Disconnect from OMXWare services"""
        if self._session is None:
            raise Exception("No connection has been established")

        self._session.close()
        self._session = None

    def _process_http_response(self, response):
        """Internal method for processing HTTP response"""
        try:
            responseJ = json.loads(response.text)
        except SyntaxError:
            return ServiceException(response.text, response.status_code)
        except ValueError:
            return ServiceException(response.text, response.status_code)
        return ServiceException(responseJ['message'], response.status_code)
