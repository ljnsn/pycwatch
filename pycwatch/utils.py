from typing import List, Union

ONE_WEEK_MONDAY = "604800_Monday"

period_mapping = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "12h": 43200,
    "1d": 86400,
    "3d": 259200,
    "1w": 604800,
    "1w_monday": ONE_WEEK_MONDAY,
}


def resolve_periods(periods: List[Union[str, int]]) -> str:
    """
    Resolve a list of period values or labels to a comma separated string of
    period values accepted by Cryptowatch.

    See https://docs.cryptowat.ch/rest-api/markets/ohlc#period-values

    >>> resolve_periods([60, 180, 7200])
    '60,180,7200'
    >>> resolve_periods([60,180,'604800_Monday'])
    '60,180,604800_Monday'
    >>> resolve_periods(['1m', '30m', '1w_monday'])
    '60,1800,604800_Monday'
    >>> resolve_periods([60,'30m'])
    '60,1800'
    >>> resolve_periods(['3m', 180])
    '180'
    """
    period_values = set()
    for period in periods:
        if period == ONE_WEEK_MONDAY:
            period_values.add(period)
        elif isinstance(period, int):
            assert period in list(period_mapping.values())
            period_values.add(period)
        else:
            value = period_mapping.get(period)
            if value is None:
                raise ValueError(f"Invalid period label: {period}")
            period_values.add(value)

    return ",".join(sorted(map(str, period_values), key=lambda p: len(p)))
