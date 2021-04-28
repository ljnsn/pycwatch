"""Tests for the REST API methods."""
import logging

import pytest
import requests_mock

from tests.conftest import get_patched_api, log_has, register_resource
from pycwatch import resources
from pycwatch.errors import APIError, APIKeyError
from pycwatch.rest import Allowance, RestAPI, KEY_HEADER, NO_KEY_MESSAGE


def test_key_setter(api_key, caplog):
    api = RestAPI()
    assert api.api_key is None
    assert KEY_HEADER not in list(api.client.headers)
    assert api.is_authenticated is False
    api.api_key = api_key
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key
    # test that `None' keys raise an error
    with pytest.raises(APIKeyError):
        api.api_key = None
        log_has("Please provide a valid API key", caplog)


def test_init_with_key(api_key):
    api = RestAPI(api_key)
    assert api.api_key == api_key
    assert api.is_authenticated
    assert api.client.headers[KEY_HEADER] == api_key


@requests_mock.Mocker(kw='rmock')
def test_perform_request_no_key(mocker, caplog, mock_resource, **kwargs):
    caplog.set_level(logging.DEBUG)
    api = RestAPI()
    mocker.patch("pycwatch.rest", api)
    resource = api.client.get_resource(mock_resource)
    response_expected = {
        "result": {
            "the-result": [1, 2, 3, 4, 5]
        }
    }
    update_allowance_mock = mocker.MagicMock()
    mocker.patch("pycwatch.rest._update_allowance", update_allowance_mock)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api._perform_request(mock_resource)
    assert log_has(NO_KEY_MESSAGE, caplog)
    assert result == response_expected['result']
    update_allowance_mock.assert_called_once()


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
    mocker.patch("pycwatch.rest._update_allowance", update_allowance_mock)
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api._perform_request(mock_resource)
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
    _ = api._perform_request(mock_resource)
    assert str(allowance) == str({
            'last_request_cost': 0.015,
            'remaining': 9.985,
            'remaining_paid': None
    })
    assert api.allowance is not None
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


@requests_mock.Mocker(kw='rmock')
def test_get_pair_details(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    pair = 'btceur'
    resource_ = resources.PairDetailsResource(pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'id': 232,
            'symbol': 'btceur',
            'base': {'id': 60,
                     'symbol': 'btc',
                     'name': 'Bitcoin',
                     'fiat': False,
                     'route': 'https://api.cryptowat.ch/assets/btc'},
            'quote': {'id': 108,
                      'symbol': 'eur',
                      'name': 'euro',
                      'fiat': True,
                      'route': 'https://api.cryptowat.ch/assets/eur'},
            'route': 'https://api.cryptowat.ch/pairs/btceur',
            'markets': [
                {'id': 136196,
                 'exchange': 'luno',
                 'pair': 'btceur',
                 'active': True,
                 'route': 'https://api.cryptowat.ch/markets/luno/btceur'}
            ]
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_pair_details(pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_list_markets(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.ListMarketsResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 1,
             'exchange': 'bitfinex',
             'pair': 'btcusd',
             'active': True,
             'route': 'https://api.cryptowat.ch/markets/bitfinex/btcusd'},
            {'id': 2,
             'exchange': 'bitfinex',
             'pair': 'ltcusd',
             'active': True,
             'route': 'https://api.cryptowat.ch/markets/bitfinex/ltcusd'},
            {'id': 3,
             'exchange': 'bitfinex',
             'pair': 'ltcbtc',
             'active': True,
             'route': 'https://api.cryptowat.ch/markets/bitfinex/ltcbtc'}
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_markets()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_market_details(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    resource_ = resources.MarketDetailsResource(exchange, pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'id': 61599,
            'exchange': 'binance',
            'pair': 'btceur',
            'active': True,
            'routes': {}
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_details(exchange, pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_market_price(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    resource_ = resources.MarketPriceResource(exchange, pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {'price': 15958.33}
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_price(exchange, pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_all_market_prices(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.AllMarketPricesResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'index:kraken-futures:cf-in-bchusd': 291.34,
            'index:kraken-futures:cf-in-ltcusd': 88.45,
            'index:kraken-futures:cf-in-xrpusd': 0.6286,
            'index:kraken-futures:cf-in-xrpxbt': 3.255e-05,
            'index:kraken-futures:cme-cf-brti': 19316,
            'index:kraken-futures:cme-cf-ethusd-rti': 613.59,
            'market:binance-us:adabtc': 8.5e-06,
            'market:binance-us:adausd': 0.1649,
            'market:binance-us:adausdt': 0.16415
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_all_market_prices()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_market_trades(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    resource_ = resources.MarketTradesResource(exchange, pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            [0, 1607016991, 15945.5, 0.045991],
            [0, 1607016992, 15941.05, 0.013129],
            [0, 1607016994, 15941.08, 0.01172],
            [0, 1607016994, 15940.79, 0.02],
            [0, 1607016996, 15940.57, 0.004254],
            [0, 1607016996, 15941.38, 0.001859],
            [0, 1607016998, 15939.77, 0.0063],
            [0, 1607016999, 15940.57, 0.00362]
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_trades(exchange, pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_market_summary(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    resource_ = resources.MarketSummaryResource(exchange, pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'price': {
                'last': 15940.1,
                'high': 16157.8,
                'low': 15612.08,
                'change': {
                    'percentage': 0.0170699508759572, 'absolute': 267.53
                }
            },
            'volume': 1553.62212,
            'volumeQuote': 24715191.19862352
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_summary(exchange, pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_all_market_summaries(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.AllMarketSummariesResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            '136758': {'price': {'last': 0.0032546138225909,
                                 'high': 0.0035258145794725,
                                 'low': 0.0020682657402101,
                                 'change': {'percentage': 0.442016845932418,
                                            'absolute': 0.0009976264428863}},
                       'volume': 9023250.056020504,
                       'volumeQuote': 25949.964961635487},
            '136759': {'price': {'last': 1.1566742437295428,
                                 'high': 1.1928931229448776,
                                 'low': 1.048950139219703,
                                 'change': {'percentage': 0.0072151815567088,
                                            'absolute': 0.0082858308962131}},
                       'volume': 24446.243211881865,
                       'volumeQuote': 28277.760167},
            '136760': {'price': {'last': 518.5,
                                 'high': 520,
                                 'low': 459.5,
                                 'change': {'percentage': 0.0961945031712474,
                                            'absolute': 45.5}},
                       'volume': 496.8052,
                       'volumeQuote': 236986.9319},
            '136761': {'price': {'last': 0,
                                 'high': 0,
                                 'low': 0,
                                 'change': {'percentage': 0,
                                            'absolute': 0}},
                       'volume': 0,
                       'volumeQuote': 0}
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_all_market_summaries()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def get_market_order_book(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    depth, span, limit = None, None, None
    resource_ = resources.MarketOrderBookResource(
        exchange, pair, depth, span, limit
    )
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'asks': [
                [15958.95, 0.002034], [15958.96, 0.159359], [15959, 1.172134]],
            'bids': [
                [15957.11, 0.007497], [15957.1, 0.003746], [15955.9, 0.019113]],
            'seqNum': 86205
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_order_book(exchange, pair, depth, span, limit)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_market_order_book_liquidity(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    resource_ = resources.MarketOrderBookLiquidityResource(exchange, pair)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'bid': {
                'base': {'100': '34.807274',
                         '150': '59.559088',
                         '200': '73.88794',
                         '25': '9.660119',
                         '250': '91.543012',
                         '300': '95.780908',
                         '400': '109.160828',
                         '50': '20.709284',
                         '500': '120.109764',
                         '75': '28.358117'},
                'quote': {'100': '553857.60153733',
                          '150': '944465.12134833',
                          '200': '1169551.58945745',
                          '25': '154210.99158204',
                          '250': '1445354.78887076',
                          '300': '1511259.96796962',
                          '400': '1717910.46927371',
                          '50': '330216.32030706',
                          '500': '1884897.72523364',
                          '75': '451693.04753122'}
            },
            'ask': {
                'base': {'100': '50.036217',
                         '150': '72.611901',
                         '200': '95.050988',
                         '25': '19.257992',
                         '250': '113.815565',
                         '300': '136.674555',
                         '400': '181.451991',
                         '50': '30.836849',
                         '500': '188.885995',
                         '75': '44.808089'},
                'quote': {'100': '802924.53049379',
                          '150': '1168210.2484117',
                          '200': '1533386.73456669',
                          '25': '308201.60658445',
                          '250': '1840123.13746447',
                          '300': '2215346.72293074',
                          '400': '2956298.13152846',
                          '50': '493935.63250687',
                          '500': '3080132.76397473',
                          '75': '718626.05512308'}
            }
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_order_book_liquidity(exchange, pair)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_ohlc(mocker, http_client, api_key, caplog, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    pair = 'btceur'
    before, after, periods = None, None, '1m'
    resource_ = resources.MarketOHLCResource(
        exchange, pair, before, after, periods)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            '60': [
                [1607020620, 16032, 16032, 16030, 16030, 0.346978, 5562.26295105],
                [1607020680, 16030, 16030, 16019.85, 16024.39, 0.212215, 3401.34688651],
                [1607020740, 16020.01, 16027.49, 16020, 16027.49, 0.175324, 2808.94010383],
                [1607020800, 16024.53, 16027.06, 16020, 16020, 0.8281, 13266.38931709],
                [1607020860, 16020, 16020, 16008.74, 16008.74, 0.887506, 14215.15540515],
                [1607020920, 16014.58, 16014.58, 16014.19, 16014.19, 0.041231, 660.28885073]
            ]
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_market_ohlc(exchange, pair, before, after, periods)
    assert result['1m'] == response_expected['result']['60']
    result = api.get_market_ohlc(exchange, pair, before, after, periods,
                                 result_key_type='int')
    assert result['60'] == response_expected['result']['60']
    with pytest.raises(ValueError):
        _ = api.get_market_ohlc(exchange, pair, before, after, periods,
                                result_key_type='period')
        assert log_has("`key_type` can be either 'str' or 'int'", caplog)


@requests_mock.Mocker(kw='rmock')
def test_list_exchanges(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.ListExchangesResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 24,
             'symbol': 'bithumb',
             'name': 'Bithumb',
             'route': 'https://api.cryptowat.ch/exchanges/bithumb',
             'active': True},
            {'id': 26,
             'symbol': 'quadriga',
             'name': 'QuadrigaCX',
             'route': 'https://api.cryptowat.ch/exchanges/quadriga',
             'active': False}
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_exchanges()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_list_exchanges(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    resource_ = resources.ListExchangesResource()
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 61,
             'symbol': 'okex',
             'name': 'Okex',
             'route': 'https://api.cryptowat.ch/exchanges/okex',
             'active': True},
            {'id': 11,
             'symbol': 'bitflyer',
             'name': 'bitFlyer',
             'route': 'https://api.cryptowat.ch/exchanges/bitflyer',
             'active': True}
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_exchanges()
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_get_exchange_details(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    resource_ = resources.ExchangeDetailsResource(exchange)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': {
            'id': 27,
            'symbol': 'binance',
            'name': 'Binance',
            'active': True,
            'routes': {'markets': 'https://api.cryptowat.ch/markets/binance'}
        }
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.get_exchange_details(exchange)
    assert result == response_expected['result']


@requests_mock.Mocker(kw='rmock')
def test_list_exchange_markets(mocker, http_client, api_key, **kwargs):
    api = get_patched_api(mocker, api_key)
    exchange = 'binance'
    resource_ = resources.ExchangeMarketsResource(exchange)
    resource = http_client.get_resource(resource_)
    response_expected = {
        'result': [
            {'id': 92885,
             'exchange': 'binance',
             'pair': 'xrpbearusdt',
             'active': True,
             'route': 'https://api.cryptowat.ch/markets/binance/xrpbearusdt'},
            {'id': 92886,
             'exchange': 'binance',
             'pair': 'xrpbearbusd',
             'active': True,
             'route': 'https://api.cryptowat.ch/markets/binance/xrpbearbusd'},
        ]
    }
    register_resource(kwargs['rmock'], resource, 'GET', 200,
                      json=response_expected)
    result = api.list_exchange_markets(exchange)
    assert result == response_expected['result']
