#  Description: Music Monolith Marketing Website
#  Author: Benjamin Orrvick
#  Author URL:  https://github.com/borrvick/
#  Purpose: connect to spotify api and get tokens and searches
#  Tags: Music, Marketing, Business, Website, Application


import datetime
import requests
import base64
from urllib.parse import urlencode


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, pClient_id, pClient_secret, *args, **kwargs):
        # if u ever need to inherit its already here
        super().__init__(*args, **kwargs)
        self.client_id = pClient_id
        self.client_secret = pClient_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret is None or client_id is None:
            raise Exception("You must set client id and secret")
        client_creds = f"{client_id}:{client_secret}"
        # for security reasons Spotify encodes the secrets in base 64 so here we encode the dictionary
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {"Authorization": f"Basic {client_creds_b64}"}

    def get_token_data(self):
        return {"grant_type": "client_credentials"}

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        # any code that isnt between 200 and 300 means it had issues
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client")
        data = r.json()
        # get current time for token expiriation validation
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):

        # currently set to none or what ever last token was when called
        token = self.access_token
        # currently set to current time when class was created or if program is on
        # long enough to need token refresh
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    # to use for all search resource retrieval methods. Right now search is the only implemented one
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    def base_search(self, pQuery_Params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{pQuery_Params}"
        r = requests.get(lookup_url, headers=headers)
        # if it failed the return empty dictionary
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    # in the future search may need changed so it is easiest to do that here
    def search(
        self,
        pQuery,
        pSearch_Type,
        pCONST_LIMIT,
        pOffset,
        pOperator=None,
        pOperator_Query=None,
    ):
        if pQuery is None:
            raise Exception("A query is required")
        # if the search is a dictonary it will still work but we probably wont use this functionality
        if isinstance(pQuery, dict):
            pQuery = " ".join([f"{k}:{v}" for k, v in pQuery.items()])
        if pOperator is not None and pOperator_Query is not None:
            # only two operators spotify has at the moment is or and not
            if pOperator.lower() == "or" or pOperator.lower() == "not":
                # spotify requires operators to be uppercase
                pOperator = pOperator.upper()
        query_params = urlencode(
            {
                "q": pQuery,
                "type": pSearch_Type.lower(),
                "limit": pCONST_LIMIT,
                "offset": pOffset,
            }
        )
        return self.base_search(query_params)
