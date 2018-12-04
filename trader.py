from dateutil.parser import parse
import xlrd

from resources.klines import KlinesService

# get xls data
data = xlrd.open_workbook('./xls/piratesignal_test_xls_output.xls')
table = data.sheet_by_index(0)
date_col = table.col_values(0)  # date column

last_date = int(parse(date_col[0]).timestamp())

klines_params = {
    'symbol': 'LTCBTC',  # get from table
    'interval': '1m',
    'startTime': last_date * 1000  # timestamp in ms
}

klines = KlinesService.get_klines_history(klines_params)

print(klines[0].open_time)

# def check_order_result(order, interval):
#     klines_params = {
#         order['pair'],
#         interval,
#         order['timestamp']
#     }
#     klines_array = KlinesService.get_klines_history(klines_params)
#     for kline in klines_array:
#
