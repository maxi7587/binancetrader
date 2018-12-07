from resources.klines import KlinesService
import time


class Order:
    def __init__(self, timestamp, pair, open, take_profit, stop_loss, opened=None, closed = None, result=None):
        self.timestamp = timestamp
        self.pair = pair
        self.open = open  # list
        self.take_profit = take_profit  # list
        self.stop_loss = stop_loss
        self.opened = opened
        self.closed = closed
        self.result = result

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__dict__


class OrdersService:
    def get_order_result(order, interval='1m'):
        klines_params = {
            'symbol': order.pair,
            'interval': interval,
            'startTime': order.timestamp
        }
        klines_array = KlinesService.get_klines_history(klines_params)
        while klines_array[-1].open_time < int(round(time.time() * 1000)):
            for kline in klines_array:
                if order.opened is None:
                    if kline.high >= order.open[0] and kline.low <= order.open[1]:
                        print('OPENED')
                        order.opened = True
                    else:
                        # if it does not open after x time, discard order
                        if kline.close_time >= order.timestamp + 10800000:
                            return 'Never opened'
                        #  TODO: add parameter to allow opening after more time
                        # if kline.close_time >= int(round(time.time() * 1000)):
                        #     return 'Never opened'
                if order.opened:
                    if kline.high >= order.take_profit[0] and kline.low <= order.stop_loss:
                        print('TP & SL')
                        return 'TP an SL reached in the same kline'
                    if kline.high >= order.take_profit[0]:
                        print('TP1')
                        return 'TP1'
                    if kline.low <= order.stop_loss:
                        print('SL', kline.low, 'is lower than', order.stop_loss)
                        return 'SL'
                    if kline.close_time >= int(round(time.time() * 1000)):
                        print('Still open')
                        return ['Still open', kline.close]
            klines_params['startTime'] = klines_array[-1].open_time
            klines_array = KlinesService.get_klines_history(klines_params)
        return 'Never opened'
