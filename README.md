# Python App Store API Client

A python implmentation of the Intelligent Plant industrial appstore API client

# Installation

## Installing using pip

```bash
pip install intelligent-plant
```

## Installing from Source

Using pip:

```bash
pip install git+https://github.com/intelligentplant/py-app-store-api
```

Alternatively clone the Git repo:

```bash
git clone https://github.com/intelligentplant/py-app-store-api.git
```

# Example Scripts

The 'example' folder contains a series of examples which demonstrate the available authentication methods and queries that you can make using this library.

To install dependencies used by the example scripts run

```bash
pip install -r example-requirements.txt
```

## Querying the Industrial App Store

In order to query the industrial app store you must register as a developer and create an app registration. Full instructions can be found here: [https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers](https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers)

Once you have created and app registration you will need to copy and rename `config-example.json` to `config.json` and populate the `id` field with you app ID. The `secret` field should be set if you have a confidential client.

For examples of these OAuth flows in practice you can use the [OAuth Playground](https://www.oauth.com/playground/index.html).

### Authorization Code Grant Flow (Web and Native Apps)

For the authorization grant flow you will need to set a redirect URL in your app registration. The example scripts use `http://localhost:8080/auth`.

These authorization code grant flow examples are minimal proof of concepts. They should not be the basis of a production app since they have no user session management, there is a single globally logged in user.

To run the authorization code grant flow example with the PKCE extension run:

```bash
python example/authorization_code_grant_flow_pkce.py
```

This is the recommended flow for web and native applications.

To run the authorization code grant flow (without PKCE extension) example run:

```bash
python example/authorization_code_grant_flow.py
```

### Device Code Flow (Embedded Devices, Jupyter Lab and Scripts)

*The device code flow is disabled by default, you must enable it on the app registration*

To run the device code flow example run:

This is the recommended flow for CLI apps and tools.

```bash
python example/device_code_flow.py
```

If you want to query data from Jupyter lab for use with data visualistion, data analysis and machine learning libraries we recommend using the device code flow and a stored session (see below).

You can see an example of this here: `example/stored_session/jupyter.ipynb`


### Implicit Grant Flow (Deprecated)

To run the implicit grant flow example run:

*The implicit grant flow is deprecated and is disabled by default*

```bash
python example/implicit_grant_flow.py
```

### Saving your session to reduce number of logins

The `intelligent_plant.session_manager` module provides functionality to save your session to your operating systems keyvault using the library [keyring](https://pypi.org/project/keyring/). To use this module you must have keyring installed:

```bash
pip install keyring
```

With keyring installed you can now use it as shown in the stored session examples.

Running the stored session example will use the device code flow to authenticate the first time (or if your session expires) but will otherwise use the stored credentials:

```bash
python example/stored_session/stored_session.py
```

You can see the stored session values using:

```bash
python example/stored_session/get_stored_session.py
```

And you can clear the stored session using:

```bash
python example/stored_session/clear_session.py
```

## Querying a local App Store Connect or Data Core node (On Site Installations)

To run the NTLM (windows authentication) example you will need to have a data core node available on the local network.
If you have an App Store Connect (https://appstore.intelligentplant.com/Home/DataSources) installed locally you can run the example without modification. If you are trying to authenticate with a data core node you will need to change the `base_url` variable defined in the script to match the URL of the Data Core admin UI.

Run the example using:

```bash
python example/ntlm_example.py
```


