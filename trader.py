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


trade_results = {
    'profit': 0.0,
    'loss': 0.0,
    'trading': 0.000,
    'trading_closed': 0
}
start_amount = 0.01
trade_amount = 0.001
months_working = 36
# should take ell the rows in the file, but the actual data is corrupted
for x in range(1, 56):
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

    # using "is" does not work
    # IMPROVE THIS SECTION (STILL OPEN)
    if first_order_result[0] == 'Still open' and  not first_order.pair.find('USDT'):
        print('STILL OPEN')
        trade_results['trading'] += trade_amount
        print('Closing this order rsults in:', ((trade_amount / first_order.open[1]) * first_order_result[1]) - trade_amount * 0.001)
        trade_results['trading_closed'] += ((trade_amount / first_order.open[1]) * first_order_result[1]) - trade_amount * 0.001
    if first_order_result[0] == 'Still open' and first_order.pair.find('USDT'):
        print('STILL OPEN')
        trade_results['trading'] += trade_amount
        trade_results['trading_closed'] += ((trade_amount * first_order.open[1]) / first_order_result[1]) - trade_amount * 0.001
    if first_order_result is 'SL' and not first_order.pair.find('USDT'):
        trade_results['loss'] += ((trade_amount / first_order.open[1]) * first_order.take_profit[0]) + trade_amount * 0.001
    if first_order_result is 'SL' and first_order.pair.find('USDT'):
        trade_results['loss'] += ((trade_amount * first_order.open[1]) / first_order.take_profit[0]) + trade_amount * 0.001
    if first_order_result is 'TP1' and not first_order.pair.find('USDT'):
        trade_results['profit'] += ((trade_amount / first_order.open[1]) * first_order.take_profit[0]) - trade_amount * 0.001
    if first_order_result is 'TP1' and first_order.pair.find('USDT'):
        trade_results['profit'] += ((trade_amount * first_order.open[1]) / first_order.take_profit[0]) - trade_amount * 0.001

close_positions_cost = trade_results['trading'] * 0.001  # its not trade amount, it's binance's 0.1% comission

print('Profit:', trade_results['profit'])
print('Loss:', trade_results['loss'])
print('Trading:', trade_results['trading'])
print('In wallet;', start_amount + trade_results['profit'] - trade_results['loss'] - trade_results['trading'] - close_positions_cost)
print('Closing positions cost:', close_positions_cost)
print('Total profit (closing positions at entry value)', trade_results['profit'] - trade_results['loss'] - close_positions_cost)
print('Total capital', start_amount + trade_results['profit'] - trade_results['loss'] - close_positions_cost)

sell_all_total = start_amount - trade_results['trading'] + trade_results['profit'] + trade_results['trading_closed'] - trade_results['loss']
sell_all_profit = sell_all_total - start_amount
print('Total capital closing trades now at real value:', start_amount - trade_results['trading'] + trade_results['profit'] + trade_results['trading_closed'] - trade_results['loss'])
print('Total profit percent:', sell_all_profit)

daily_profit_percent = ((((sell_all_profit/7)/2)*100)/start_amount)
monthly_profit_percent = ((((sell_all_profit/7)/2)*100)/start_amount)*30
print('Daily profit percent:', ((((sell_all_profit/7)/2)*100)/start_amount))
print('Monthly profit percent:', ((((sell_all_profit/7)/2)*100)/start_amount)*30)
print('Year profit percent:', ((((sell_all_profit/7)/2)*100)/start_amount)*30*months_working)

print('Yearly total with monthly compound interest:', start_amount*((1+(monthly_profit_percent/100))**months_working))
