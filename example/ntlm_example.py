"""A client app that uses NTLM authentication"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

from getpass import getpass


import intelligent_plant.data_core_client as data_core_client

# This is the format of the base url for an app store connected installed locally
# This is the same as the URL of the admin UI
# YOU MUST INCLUDE THE TRAILING '/'
base_url = 'http://localhost:2006/Service/runtime/[app store connect namespace]/datacore/'

print("Username:")
username = input()

password = getpass()

auth = {
    'user': username,
    'password': password
}

data_core= data_core_client.DataCoreClient(base_url=base_url, auth=auth)

data_sources = data_core.get_data_sources()

print(list(map(lambda x: x['Name']['QualifiedName'], data_sources)))