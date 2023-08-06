# -*- coding: utf-8 -*-

"""
cloudcix.auth
~~~~~~~~~~~~~

This module implements the CloudCIX API Client Authentications
"""

import requests

import cloudcix.api
import cloudcix.conf


def get_admin_token():
    """
    Generates an `admin` token using the credentials specified in the settings module
    """
    data = {
        'email': cloudcix.conf.settings.CLOUDCIX_API_USERNAME,
        'password': cloudcix.conf.settings.CLOUDCIX_API_PASSWORD,
        'api_key': cloudcix.conf.settings.CLOUDCIX_API_KEY,
    }
    response = cloudcix.api.Membership.token.create(data=data)
    if response.status_code == 201:
        return response.json()['token']
    raise Exception(response.json()['error_code'])


class TokenAuth(requests.auth.AuthBase):
    """
    CloudCIX Token-based authentication
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['X-Auth-Token'] = self.token
        return request

    def __eq__(self, other):
        return self.token == other.token
