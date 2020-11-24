import logging

import pytest
import requests_mock

from tests.conftest import get_patched_api, log_has, register_resource
from pycwatch import resources
from pycwatch.errors import APIError
from pycwatch.rest import Allowance, RestAPI, KEY_HEADER


def test_key_setter(api_key):
    api = RestAPI()
    assert api.api_key is None
    assert KEY_HEADER not in list(api.client.headers)
    assert api.is_authenticated is False
    api.api_key = api_key
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


def test_init_with_key(api_key):
    api = RestAPI(api_key)
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


def test_perform_request_no_key(caplog, mock_resource):
    caplog.set_level(logging.INFO)
    api = RestAPI()
    line = "API Key needs to be set"
    with pytest.raises(APIError):
        api.perform_request(mock_resource)
        assert log_has(line, caplog)


@requests_mock.Mocker(kw='rmock')
def test_perform_request(mocker, api_key, mock_resource, **kwargs):
    api = RestAPI(api_key)
    mocker.patch("pycwatch.rest", api)
    resource = api.client.get_resource(mock_resource)
    response_expected = {
        "result": {
            "the-result": [1, 2, 3, 4, 5]
        }
    }
    update_allowance_mock = mocker.MagicMock()
    mocker.patch("pycwatch.rest.update_allowance", update_allowance_mock)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.perform_request(mock_resource)
    assert result == response_expected['result']
    update_allowance_mock.assert_called_once()


@requests_mock.Mocker(kw='rmock')
def test_update_allowance(mocker, api_key, mock_resource, **kwargs):
    api = RestAPI(api_key)
    mocker.patch("pycwatch.rest", api)
    resource = api.client.get_resource(mock_resource)
    response_expected = {
        "allowance": {
            "cost": 0.015,
            "remaining": 9.985,
            "upgrade": "Check https://cryptowat.ch"
        },
        "result": {}
    }
    allowance = Allowance(response_expected)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    assert api.allowance is None
    _ = api.perform_request(mock_resource)
    assert str(allowance) == str({
            'last_request_cost': 0.015,
            'remaining': 9.985,
            'remaining_paid': None
    })
    assert str(api.allowance) == str(allowance)
    assert api.allowance.cost == 0.015
    assert api.allowance.remaining == 9.985


@requests_mock.Mocker(kw='rmock')
def test_list_assets(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.ListAssetsResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 470,
             'symbol': 'trac',
             'name': 'OriginTrail',
             'fiat': False,
             'route': 'https://api.cryptowat.ch/assets/trac'},
            {'id': 4972,
             'symbol': 'trade',
             'name': 'Unitrade',
             'fiat': False,
             'route': 'https://api.cryptowat.ch/assets/trade'},
            {'id': 4971,
             'symbol': 'trb',
             'name': 'Tellor',
             'fiat': False,
             'route': 'https://api.cryptowat.ch/assets/trb'},
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_assets()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_asset_details(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    asset_code = 'eur'
    resource_ = resources.AssetDetailsResource(asset_code)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'id': 108,
            'symbol': 'eur',
            'name': 'euro',
            'fiat': True,
            'markets': {
                'base': [
                    {'id': 63898,
                     'exchange': 'bitfinex',
                     'pair': 'eurusdt-perpetual-future-inverse',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/eurusdt-perpetual-future-inverse'},
                    {'id': 61603,
                     'exchange': 'binance',
                     'pair': 'eurbusd',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/binance/eurbusd'},
                    {'id': 61604,
                     'exchange': 'binance',
                     'pair': 'eurusdt',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/binance/eurusdt'},
                    {'id': 82,
                     'exchange': 'bitstamp',
                     'pair': 'eurusd',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitstamp/eurusd'}
                ],
                'quote': [
                    {'id': 415,
                     'exchange': 'bitfinex',
                     'pair': 'btceur',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/btceur'},
                    {'id': 473,
                     'exchange': 'bitfinex',
                     'pair': 'iotaeur',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/iotaeur'},
                    {'id': 1028,
                     'exchange': 'bitfinex',
                     'pair': 'etheur',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/etheur'},
                    {'id': 1031,
                     'exchange': 'bitfinex',
                     'pair': 'neoeur',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/neoeur'},
                    {'id': 1034,
                     'exchange': 'bitfinex',
                     'pair': 'eoseur',
                     'active': True,
                     'route': 'https://api.cryptowat.ch/markets/bitfinex/eoseur'}
                ],
            }
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_asset_details(asset_code)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_list_pairs(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.ListPairsResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 984,
             'symbol': '1stbtc',
             'base': {'id': 404,
                      'symbol': '1st',
                      'name': 'FirstBlood',
                      'fiat': False,
                      'route': 'https://api.cryptowat.ch/assets/1st'},
             'quote': {'id': 60,
                       'symbol': 'btc',
                       'name': 'Bitcoin',
                       'fiat': False,
                       'route': 'https://api.cryptowat.ch/assets/btc'},
             'route': 'https://api.cryptowat.ch/pairs/1stbtc'},
            {'id': 809,
             'symbol': '1steth',
             'base': {'id': 404,
                      'symbol': '1st',
                      'name': 'FirstBlood',
                      'fiat': False,
                      'route': 'https://api.cryptowat.ch/assets/1st'},
             'quote': {'id': 77,
                       'symbol': 'eth',
                       'name': 'Ethereum',
                       'fiat': False,
                       'route': 'https://api.cryptowat.ch/assets/eth'},
             'route': 'https://api.cryptowat.ch/pairs/1steth'},
            {'id': 5179,
             'symbol': '1wobtc',
             'base': {'id': 3733,
                      'symbol': '1wo',
                      'name': '1World',
                      'fiat': False,
                      'route': 'https://api.cryptowat.ch/assets/1wo'},
             'quote': {'id': 60,
                       'symbol': 'btc',
                       'name': 'Bitcoin',
                       'fiat': False,
                       'route': 'https://api.cryptowat.ch/assets/btc'},
             'route': 'https://api.cryptowat.ch/pairs/1wobtc'}
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_pairs()
    assert result == response_expected['result']
