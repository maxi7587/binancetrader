import requests
import json

# format url?symbol&interval&startTime
klines_url = 'https://api.binance.com/api/v1/klines'

klines_params = {
    'symbol': 'LTCBTC',
    'interval': '1m',
    'startTime': '1483243199000' # in ms since 1/1/1970
}

candlesticks = requests.get(klines_url, params = klines_params).json()
print(candlesticks)
