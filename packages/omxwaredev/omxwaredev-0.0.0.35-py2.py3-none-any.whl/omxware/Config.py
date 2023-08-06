from keycloak import KeycloakOpenID as KeyCloak
from omxware.AESCipher import AESCipher
import urllib3
from keycloak.exceptions import KeycloakAuthenticationError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""OMXWware Configuration class"""
class Configuration:
    __omx_token = ''
    __keycloak_token = ''
    __server = ''
    __userinfo = {}

    def __init__(self, omx_token, server_url):
        self.__omx_token = omx_token
        self.__server = server_url

        if self.isValidOMXToken() != True:
            raise ConnectionError

    def getServerURL(self):
        return self.__server

    def getOMXToken(self):
        return self.__omx_token

    def getUserInfo(self):
        return self.__userinfo

    def getAuthToken(self):
        self.isValidOMXToken()
        return self.__keycloak_token

    def __parse_token(self):
        aes = AESCipher()
        token_decrypted = aes.decrypt(self.getOMXToken())

        return token_decrypted.split('::::')

    def isValidOMXToken(self):

        credentials = self.__parse_token();
        username = credentials[1]
        pwd = credentials[2]

        keycloak = KeyCloak(server_url="https://omx-auth.sl.cloud9.ibm.com/auth/",
                            client_id="omx-zeppelin",
                            realm_name="omxware",
                            client_secret_key="1320e78d-025d-48eb-ad3e-451281786932",
                            verify=False)

        try:
            # Get Token
            token = keycloak.token(username, pwd)
            self.__userinfo = keycloak.userinfo(token['access_token'])

            self.__keycloak_token = token['access_token']

            return True

        except KeycloakAuthenticationError as auth_error:
            # Exception object looks like this
            # keycloak.exceptions.KeycloakAuthenticationError:
            # 401: b'{"error":"invalid_grant","error_description":"Invalid user credentials"}'

            error_msg = ''

            if auth_error['error_description'] != None:
                error_msg = auth_error['error_description']

            if error_msg.strip() != None:
                print(error_msg)
            else:
                print(auth_error['error_description'])

            return False
