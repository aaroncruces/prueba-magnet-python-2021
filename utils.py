"""
DO NOT EDIT THIS FILE, IT'S NOT PART OF THE TEST.
If you edit this file your application will be automatically rejected.
"""

# standard library
import http.client
import json
from urllib.parse import urlparse

# typing
from typing import Any
from typing import Dict
from typing import List

# Must change in test repository
BASE_URL = 'http://localhost:8000'


def request(
    method: str,
    url: str,
    data: Dict[str, str]=None,
    token: str=None,
    error_message: str=None
) -> Dict[Any, Any]:
    """
    Constructs and send a request
    :param method: method for the request: 'POST' and 'GET'
    :param url: URL for the request, include params
    :param data: (optional) Dictionary to send in the body
    :param token: (optional) Authorization token for protected endpoints
    :param error_message: (optional) Custom error message

    :return: Dictionary with the response data
    """
    # parse url
    parsed_url = urlparse(url)
    base_url = parsed_url.netloc
    url = '{}'.format(parsed_url.path)

    if parsed_url.query:
        url = '{}?{}'.format(url, parsed_url.query)

    # make request
    try:
        # connection
        conn = http.client.HTTPConnection(base_url)
        headers = {
            'content-type': 'application/json',
        }

        # add token if exists
        if token:
            headers['Authorization'] = 'JWT {}'.format(token)

        # required request data
        kwargs = {}  # type: Dict[str, Any]

        # put body
        if data:
            kwargs['body'] = json.dumps(data)

        # request
        conn.request(method, url, headers=headers, **kwargs)

        # manage response
        res = conn.getresponse()
        response_data = json.loads(res.read().decode())
    except Exception:
        error_message = error_message if error_message else 'Url must be wrong'
        raise ValueError(error_message)

    return response_data


def post(url: str, data: dict, token: str) -> Dict[Any, Any]:
    """
    Constructs and send a POST request
    :param url: URL for the request, include params
    :param data: Dictionary to send in the body
    :param token: (Authorization token for protected endpoints

    :return: Dictionary with the response data
    """
    # check token
    if not token:
        raise ValueError('You must include a valid token')
    return request('POST', url, data=data, token=token)


def get(url: str, token: str) -> Dict[Any, Any]:
    """
    Constructs and send a GET request
    :param url: URL for the request, include params
    :param token: Authorization token for protected endpoints

    :return: Dictionary with the response data
    """
    # check token
    if not token:
        raise ValueError('You must include a valid token')
    return request('GET', url, token=token)


def auth(email: str, password: str) -> Dict[Any, Any]:
    """
    Constructs and send an Auth request
    :param email: user account email
    :param password: user account password

    :return: Dictionary with the response data, include a token
    """
    # set credentials
    data = {
        'email': email,
        'password': password,
    }
    error_message = 'Invalid credentials'

    return request(
        'POST',
        BASE_URL + '/api/v1/auth/',
        data=data,
        error_message=error_message,
    )