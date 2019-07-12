import requests
import json
import webview
import urllib

import intelligent_plant.app_store_client as app_store_client

redirect_url = "https://appstore.intelligentplant.com"

base_url = None

def test_client(token):
    client = app_store_client.AppStoreClient(base_url, token, None)

    print(client.get_user_info())
    print(client.get_user_balance())

def on_loaded(window):
    while True:
        url = window.get_current_url()

        if (url.startswith(redirect_url)):
            window.destroy()
            #we can get the code
            parsed = urllib.parse.urlparse(url)
            print(parsed)
            test_client(urllib.parse.parse_qs(parsed.fragment)['access_token'][0])
            break

#load the json config file with the app information
with open('config.json') as json_config_file:
    config = json.load(json_config_file)

    app_id = config['app']['id']
    app_secret = config['app']['secret']
    base_url = config['app_store']['base_url']

    url = app_store_client.get_implicit_grant_flow_url(base_url, app_id, redirect_url, ["UserInfo", "DataRead"])

    window = webview.create_window('Login', url)
    webview.start(on_loaded, window, debug=True)
    