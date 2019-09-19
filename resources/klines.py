import requests
from requests_toolbelt.utils import dump


class Kline:
    def __init__(
        self,
        open_time,
        open,
        high,
        low,
        close,
        volume,
        close_time,
        quote_asste_volume,
        trades_qty,
        taker_buy_base_asset_volume,
        taker_buy_quote_asset_volume,
        additional_data
    ):
        self.open_time = open_time  # Open time (int)
        self.open = open  # Open (str) to (float)
        self.high = high  # High (str) to (float)
        self.low = low  # Low (str) to (float)
        self.close = close       # Close (str) to (float)
        self.volume = volume  # Volume (str) to (float)
        self.close_time = close_time  # Close time (int)
        self.quote_asste_volume = quote_asste_volume    # Quote asset volume (str)  to (float)
        self.trades_qty = trades_qty  # Number of trades (int)
        self.taker_buy_base_asset_volume = taker_buy_base_asset_volume  # Taker buy base asset volume (str) to (float)
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume  # Taker buy quote asset volume (str) to (float)
        self.additional_data = additional_data  # Can be ignored (str)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class KlinesService:
    def get_klines_history(klines_params):
        klines_url = 'https://api.binance.com/api/v1/klines'
        klines_array = []
        raw_klines = requests.get(klines_url, params=klines_params)

        # just for dubugging
        # data = dump.dump_all(raw_klines)
        # print(data.decode('utf-8'))
        # print(klines_params)

        raw_klines = raw_klines.json()
        # print(klines_params)
        # print(raw_klines)

        for kline in raw_klines:
            kline_object = Kline(
                kline[0],
                float(kline[1]),
                float(kline[2]),
                float(kline[3]),
                float(kline[4]),
                float(kline[5]),
                kline[6],
                float(kline[7]),
                kline[8],
                float(kline[9]),
                float(kline[10]),
                kline[11]
            )

            klines_array.append(kline_object)

        return klines_array
