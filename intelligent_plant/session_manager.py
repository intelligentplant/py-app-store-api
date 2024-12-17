"""Session manager for Industrial App Store sessions"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import time

import keyring

import intelligent_plant.app_store_client as app_store_client

service_id = 'IP-Industrial-App-Store-Python'

def delete_session(app_id: str):

    try:
        keyring.delete_password(service_id, f'{app_id}_access_token')
    except:
        pass
    try:
        keyring.delete_password(service_id, f'{app_id}_refresh_token')
    except:
        pass
    try:
        keyring.delete_password(service_id, f'{app_id}_expiry_time')
    except:
        pass

def store_session(app_id: str, app_store: app_store_client.AppStoreClient):

    try:
        keyring.set_password(service_id, f'{app_id}_access_token', app_store.access_token)
    except:
        pass
    try:
        keyring.set_password(service_id, f'{app_id}_refresh_token', app_store.refresh_token)
    except:
        pass
    try:
        keyring.set_password(service_id, f'{app_id}_expiry_time', str(app_store.expiry_time))
    except:
        pass

def load_session(app_id: str, base_url: str = app_store_client.DEFAULT_BASE_URL) -> app_store_client.AppStoreClient:

    try:
        access_token = keyring.get_password(service_id, f'{app_id}_access_token')
    except:
        access_token = None
    try:
        refresh_token = keyring.get_password(service_id, f'{app_id}_refresh_token')
    except:
        refresh_token = None
    try:
        expiry_time = float(keyring.get_password(service_id, f'{app_id}_expiry_time'))
    except:
        expiry_time = None

    app_store = app_store_client.AppStoreClient(access_token, refresh_token=refresh_token, base_url=base_url)

    app_store.expiry_time = expiry_time

    return app_store

def load_session_or_login(app_id: str, app_secret: str = None, scopes: list[str] = None, base_url: str = app_store_client.DEFAULT_BASE_URL) -> app_store_client.AppStoreClient:
    f"""
    Login to the Industrial App Store using the device code flow but use a stored session from the keyring first if available.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param device_code: The device code specified in the reponse of begin_device_code_flow(..)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param base_url: The app store base url (optional, default value is {app_store_client.DEFAULT_BASE_URL})

    :return: The logged in app store client.
    
    :raises: :class:`DeviceCodeFlowError` if an unrecoverable error occurs with the device code flow.
    :raises: :class:`HTTPError` if an HTTP error occurrs.
    :raises: :class:`JSONDecodeError` if JSON decoding fails.
    """
    # get the session details for the specified app id from the keychain
    app_store = load_session(app_id, base_url)

    if app_store.access_token is None:
        app_store = app_store_client.device_code_login(app_id, app_secret, scopes, base_url)
    else:
        if app_store.expiry_time < time.time():
            # sesion has expired attempt to refresh
            try:
                app_store.refresh_session(app_id, app_secret)
            except:
                # refesh failed send the user to the login page
                app_store = app_store_client.device_code_login(app_id, app_secret, scopes, base_url)

    # we should now have a working session but it may be different than what is stored so store the new session
    store_session(app_id, app_store)

    #return the logged in session
    return app_store

