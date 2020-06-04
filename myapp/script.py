import sys
import requests
from . import config

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
TENANT = 'tenant'
ACCESS_TOKEN = 'access_token'

def _get_access_token(tenant, client_id, client_secret):
        data = {
            CLIENT_ID: client_id,
            'scope': 'https://graph.microsoft.com/.default',
            CLIENT_SECRET: client_secret,
            'grant_type': 'client_credentials'
        }
        access_token = requests.post(
            f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
            data=data
        ).json()[ACCESS_TOKEN]
        print(access_token)
        return access_token
        
def main():
    access_token =_get_access_token(
            config.graph_auth[TENANT],
            config.graph_auth[CLIENT_ID],
            config.graph_auth[CLIENT_SECRET])
    print(access_token)


if __name__ == '__main__':
    main()
