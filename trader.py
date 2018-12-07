from dateutil.parser import parse
import xlrd

from resources.klines import KlinesService
from resources.orders import Order, OrdersService

# get xls data
data = xlrd.open_workbook('./xls/piratesignal_test_xls_output.xls')
table = data.sheet_by_index(0)
date_col = table.col_values(0)  # date column

last_date = int(parse(date_col[1]).timestamp())

# klines_params = {
#     'symbol': 'LTCBTC',  # get from table
#     'interval': '1m',
#     'startTime': 1544137989000
#     # 'startTime': last_date * 1000  # timestamp in ms
# }
#
# klines = KlinesService.get_klines_history(klines_params)
# print(klines[-1])

# print(klines[0].open_time)

# should take ell the rows in the file, but the actual data is corrupted
for x in range(1, 31):
    print('------------------', x, '-----------------')
    raw_first_order = table.row_values(x)
    first_order = Order(
        int(parse(raw_first_order[0]).timestamp()) * 1000,
        raw_first_order[1],
        raw_first_order[2:4],
        raw_first_order[5:9],
        raw_first_order[4]
    )
    first_order_result = OrdersService.get_order_result(first_order)

    print(first_order_result)
