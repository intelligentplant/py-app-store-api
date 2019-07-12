
from bottle import route, run, request, redirect

import json
import urllib

import intelligent_plant.app_store_client as app_store

app_id = None
app_secret = None
base_url = None

client = None

#load the json config file with the app information
with open('config.json') as json_config_file:
    config = json.load(json_config_file)

    print(config)

    app_id = config['app']['id']
    app_secret = config['app']['secret']
    base_url = config['app_store']['base_url']

@route('/auth')
def auth():
    global client
    auth_code = request.query.code

    client = app_store.complete_authorization_code_grant_flow(base_url, auth_code, app_id, app_secret, "http://localhost:8080/auth")
                                
    redirect('/info')

@route('/info')
def info():
    return str(client.get_user_info())

@route('/')
def index():
    url = app_store.get_authorization_code_grant_flow_url(base_url, app_id, "http://localhost:8080/auth", ["UserInfo", "DataRead"])
    redirect(url)


run(host='localhost', port=8080)

