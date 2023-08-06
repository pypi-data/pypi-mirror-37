from keycloak import KeycloakOpenID as KeyCloak
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure client
keycloak = KeyCloak(server_url="https://omx-auth.sl.cloud9.ibm.com/auth/",
                    client_id="omx-zeppelin",
                    realm_name="omxware",
                    client_secret_key="1320e78d-025d-48eb-ad3e-451281786932",
                    verify=False)

# Get WellKnow
config_well_know = keycloak.well_know()

# Get Token
token = keycloak.token("0", "temp4now")

# Get Userinfo
userinfo = keycloak.userinfo(token['access_token'])
for key in userinfo.keys():
    print(key + " ==> " + str(userinfo.get(key)))

# Refresh token
token = keycloak.refresh_token(token['refresh_token'])

# Logout
keycloak.logout(token['refresh_token'])
