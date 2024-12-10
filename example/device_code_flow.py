"""A client app that uses the device code flow"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import json

import intelligent_plant.app_store_client as app_store_client

# Remeber to enable the device code flow in the app store app registration

#load the json config file with the app information
with open('config.json') as json_config_file:
    config = json.load(json_config_file)

    app_id = config['app']['id']
    app_secret = config['app']['secret']
    base_url = config['app_store']['base_url']


authorize_response = app_store_client.begin_device_code_flow(app_id, scopes=['DataRead'], app_secret=app_secret)

print(f"To login go here: {authorize_response['verification_uri']} and enter this code: {authorize_response['user_code']}")

app_store = app_store_client.poll_device_token(app_id, authorize_response['device_code'], authorize_response['interval'], app_secret=app_secret)

data_core = app_store.get_data_core_client()

print(list(map(lambda x: x['Name']['QualifiedName'], data_core.get_data_sources())))