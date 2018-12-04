from klines import KlinesService


class Order:
    take_profit = []

    def __init__(self, open, take_profit, stop_loss, opened=None, closed = None, result=None):
        self.open = open
        self.take_profit = take_profit  # list
        self.stop_loss = stop_loss
        self.opnened = opened
        self.closed = closed
        self.result = result

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class OrdersService:
    def get_order_result(order, interval='1m'):
        klines_params = {
            order['pair'],
            interval,
            order['timestamp']
        }
        klines_array = KlinesService.get_klines_history(klines_params)
        for kline in klines_array:
            if kline.high >= order.take_profit[0] and kline.low <= order.stop_loss:
                return 'TP an SL reached in the same kline'
            if kline.high >= order.take_profit[0]:
                return 'TP1'
            if kline.low <= order.stop_loss:
                return 'SL'
            else:
                return None
