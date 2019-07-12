import requests
import urllib

class AppStoreClient(object):
    """Access the Intelligent Plant Appstore API"""

    def __init__(self, base_url, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = base_url

        self.headers = {'Authorization': "Bearer " + self.access_token }

    def get_user_info(self):
        url = self.base_url + "/api/resource/userinfo"
        
        r = requests.get(url, headers = self.headers)

        if (r.status_code == requests.codes.ok):
            return r.json()
        else:
            r.raise_for_status()

    def get_user_balance(self):
        url = self.base_url + "/api/resource/userbalance"
        
        r = requests.get(url, headers = self.headers)

        if (r.status_code == requests.codes.ok):
            return r.text
        else:
            r.raise_for_status()


def get_authorization_code_grant_flow_url(base_url, app_id, redirect_uri, scopes):
    """Get the url that the client should use for authorization code grant flow
    """
    params = {
        'response_type': "code",
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': " ".join(scopes)
    }
    url = base_url + "/authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url

def complete_authorization_code_grant_flow(base_url, auth_code, app_id, app_secret, redirect_uri):
    """Complete logging in the user using authroization grant flow

    An app store client with the access token specified
    """
    url = base_url + "/authorizationserver/oauth/token"

    params = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri
    }
    
    r = requests.post(url, params)

    if (r.status_code == requests.codes.ok):
        token = r.json()

        return AppStoreClient(base_url, token['access_token'], None)
    else:
        r.raise_for_status()

    
def get_implicit_grant_flow_url(base_url, app_id, redirect_url, scopes):
    """Get the URL that the cleint should use for an implicit grant flow
    """
    params = {
        'response_type': "token",
        'client_id': app_id,
        'redirect_uri': redirect_url,
        'scope': " ".join(scopes)
    }

    url = base_url + "/authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url


