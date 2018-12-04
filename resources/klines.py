import requests


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
        self.open = open  # Open (str)
        self.high = high  # High (str)
        self.low = low  # Low (str)
        self.close = close       # Close (str)
        self.volume = volume  # Volume (str)
        self.close_time = close_time  # Close time (int)
        self.quote_asste_volume = quote_asste_volume    # Quote asset volume (str)
        self.trades_qty = trades_qty  # Number of trades (int)
        self.taker_buy_base_asset_volume = taker_buy_base_asset_volume  # Taker buy base asset volume (str)
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume  # Taker buy quote asset volume (str)
        self.additional_data = additional_data  # Can be ignored (str)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class KlinesService:
    def get_klines_history(klines_params):
        klines_url = 'https://api.binance.com/api/v1/klines'
        klines_array = []
        raw_klines = requests.get(klines_url, params = klines_params).json()

        for kline in raw_klines:
            kline_object = Kline(
                kline[0],
                kline[1],
                kline[2],
                kline[3],
                kline[4],
                kline[5],
                kline[6],
                kline[7],
                kline[8],
                kline[9],
                kline[10],
                kline[11]
            )

            klines_array.append(kline_object)

        return klines_array
