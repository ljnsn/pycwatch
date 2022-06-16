from apiclient import endpoint


@endpoint(base_url="https://api.cryptowat.ch")
class Endpoint:
    root = "/"
    list_assets = "/assets"
    asset_detail = "/assets/{assetCode}"
    list_pairs = "/pairs"
    pair_detail = "/pairs/{pair}"
    list_markets = "/markets"
    market_detail = "/markets/{exchange}/{pair}"
    all_market_prices = "/markets/prices"
    market_price = "/markets/{exchange}/{pair}/price"
    list_market_trades = "/markets/{exchange}/{pair}/trades"
    market_summary = "/markets/{exchange}/{pair}/summary"
    all_market_summaries = "/markets/summaries"
    market_orderbook = "/markets/{exchange}/{pair}/orderbook"
    market_orderbook_liquidity = "/markets/{exchange}/{pair}/orderbook/liquidity"
    market_orderbook_calculator = "/markets/{exchange}/{pair}/orderbook/calculator"
    market_ohlc = "/markets/{exchange}/{pair}/ohlc"
    list_exchanges = "/exchanges"
    exchange_detail = "/exchanges/{exchange}"
    exchange_markets = "/markets/{exchange}"
