# -*- coding: utf-8 -*-
from pyasista import AsistaInput
from unittest import mock

import pytest


def mock_successful_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({
        'success': True,
        'token': {
            'access_token': 'NEW_ACCESS_TOKEN'
        }
    }, 200)


def mock_unsuccessful_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({
        'success': False,
        'token': {
            'access_token': 'NEW_ACCESS_TOKEN'
        }
    }, 200)


def mock_http_fail(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(None, 400)


def event_with_token():
    return {
        'environment': 'PRODUCTION',
        'language': 'TR',
        'token': {
            'access_token': 'ACCESS_TOKEN',
            'asista_refresh_data': 'REFRESH_DATA',
            'asista_refresh_token_uri': 'https://dummy.co/dummy',
            'asista_client_key': 'CLIENT_KEY'
        }
    }


@mock.patch('requests.post', side_effect=mock_successful_response)
def test_refresh_access_token(*args, **kwargs):
    asista_input = AsistaInput(event_with_token())
    token = asista_input.token
    assert token.refresh()
    assert token.access_token == 'NEW_ACCESS_TOKEN'


@mock.patch('requests.post', side_effect=mock_unsuccessful_response)
def test_refresh_access_token_fail(*args, **kwargs):
    asista_input = AsistaInput(event_with_token())
    token = asista_input.token
    assert not token.refresh()
    assert token.access_token == 'ACCESS_TOKEN'


@mock.patch('requests.post', side_effect=mock_http_fail)
def test_refresh_access_token_http_fail(*args, **kwargs):
    asista_input = AsistaInput(event_with_token())
    token = asista_input.token
    assert not token.refresh()
    assert token.access_token == 'ACCESS_TOKEN'
