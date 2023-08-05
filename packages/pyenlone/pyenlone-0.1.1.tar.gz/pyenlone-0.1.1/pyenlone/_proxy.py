""" Proxies do the actual API requests. """
from abc import ABC, abstractmethod

import requests
import requests_cache
from munch import munchify

from .enloneexception import EnlOneException

class Proxy(ABC):
    """
    Proxy interface.
    """
    @abstractmethod
    def get(self, endpoint, params): pass
    @abstractmethod
    def post(self, endpoint, json): pass

class KeyProxy(Proxy):
    """
    Proxy implementation for authentication using API keys.
    """
    def __init__(self, base_url, apikey, cache=0):
        self._apikey = apikey
        self._base_url = base_url
        if cache > 0:
            requests_cache.install_cache('apikey_cache', backend='sqlite', expire_after=cache)
    def get(self, endpoint, params={}):
        """
        Do a get request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        params["apikey"] = self._apikey
        try:
            response = requests.get(url, params=params)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        if response and response.json()["status"] == "ok":
            return munchify(response.json()["data"])
        else:
            raise EnlOneException("enl.one API call error.")
    def post(self, endpoint, json):
        """
        Do a post request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        try:
            response = requests.post(url, params={"apikey" : self._apikey}, json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        if response and response.json()["status"] == "ok":
            return munchify(response.json()["data"])
        else:
            raise EnlOneException("enl.one API call error.")

class TokenProxy(Proxy):
    """
    Proxy implementation for authentication using OAuth tokens.
    """
    def __init__(self, base_url, token, cache=0):
        self._token = token
        self._base_url = base_url + "/oauth"
        if cache > 0:
            requests_cache.install_cache('token_cache', backend='sqlite', expire_after=cache)
    def get(self, endpoint, params={}):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization':'Bearer ' + self._token}
        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        if response and response.json()["status"] == "ok":
            return munchify(response.json()["data"])
        else:
            raise EnlOneException("enl.one API call error.")
    def post(self, endpoint, json):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization':'Bearer ' + self._token}
        try:
            response = requests.post(url, headers=headers, json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        if response and response.json()["status"] == "ok":
            return munchify(response.json()["data"])
        else:
            raise EnlOneException("enl.one API call error.")

class OpenProxy:
    """
    Proxy implementation for the open API.
    """
    def get(self, endpoint):
        """
        Do a get request with no auth.
        """
        url = "https://v.enl.one/OpenApi" + endpoint
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        if response and response.json()["status"] == "ok":
            return munchify(response.json()["data"])
        else:
            raise EnlOneException("enl.one API call error.")
