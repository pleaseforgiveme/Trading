"""
1. Scan all large caps and find candidates as per
1.1 Consolidating. Definition: In the past X days, there existed a local bottom and top.
1.2 Add alert for the top and for the bottom after the top is conquered.
1.3 (important) When the top is conquered, and it lasts for ~24h, follow to join with 
moderate leverage (e.g. 3X or use the bottom as the liquidation price)
OR just use 1X so can hold if it doesn't play out. 
1.4 Once position opened, use stop order to ride the wave to the top. Adjust stop price 
every 12 - 24h using the 30m chart.

"""

import sys
#sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
sys.path.append('/Users/xl/Library/Python/3.9/lib/python/site-packages')
from binance.spot import Spot

api_key = 'oTcRPne8yYBkCaXrT6DItAu4dsEshAFnVjXyYyadfX6e5BFPNK4jwduu8seObvd0'
# read from key.txt and assign the value to api_scrt
def read_src():
    with open('key.txt', 'r') as file:
        return file.read().strip()
client = Spot(api_key=api_key,api_secret=read_src())

one_trillion = 1_000_000_000_000

# Catch at the bottom of a bounce back, e.g. PEOPLE 1/3/2024 or UNFIUSDT 6/7/2022
def catch_bottom():
    pass


# Scan all large caps and find candidates that falls back from a local top
def find_consolidating_candidates():
    # for each candidate, do:
    pass

# Scan all large caps and find candidates that breaks through a local top
def find_breakthrough_candidates():
    # for each candidate, do:
    pass

# Adjust the stop price during a blow-off top
def adjust_stop_price():
    pass

# add alert for the top where you should enter the market
def add_alert():
    pass

# Reorder the watchlist based on the current price
def reorder_watchlist():
    pass

#
def track_top_breakthrough():
    # for each candidate, do:
    pass

# Fetch prices from Binance api and return a list of close prices
def fetch_prices(symbol, interval, limit):
    prices = []
    klines = client.klines(symbol=symbol, interval=interval, limit=limit)
    for kline in klines:
        prices.append(float(kline[4]))
    return prices

# Fetch high and low prices from Binance api and return a list of prices
# sample usage: 'BTCUSDT', '1d', 30
def fetch_high_low_prices(symbol, interval, limit):
    # price should be a list of prices of tuple (high, low)
    prices = []
    # should fetch the past limit days
    klines = client.klines(symbol=symbol, interval=interval, limit=limit)
    for kline in klines:
        current_price = (float(kline[2]), float(kline[3]))
        prices.append(current_price)
    return prices

def is_consolidating(prices, percentage, limit):
    # scan for the past limit days for daily high/low
    resistance = 0 # also record the highest date(s)
    support = one_trillion  # also record the lowest date(s)
    for price in prices:
        resistance = max(resistance, price[0])
        support = min(support, price[1])
    bandwidth = resistance - support
    highest_days = []
    lowest_days = []
    # consolidation should satisfy the following:
    # 1. Today's highest <= resistance && lowest >= support
    # 2. at least two dates close to resistance or support,
    # i.e. |price - resistance| / resistance <= X% (or support)
    # We may need to tighten this rule to filter out fake ones.
    if prices[-1][0] > resistance or prices[-1][1] < support:
        return False
    highest_count, lowest_count = 0, 0
    print(f"resistance: {resistance}, support: {support}")
    for price in prices:
        assert resistance >= price[0] and support <= price[1]
        if (resistance - price[0]) / resistance <= percentage:
            highest_count += 1
        elif (price[1] - support) / support <= percentage:
            lowest_count += 1
    return highest_count >= 2 or lowest_count >= 2

# Given the symbol of a coin, purchase it with the given amount
def purchase_coin(symbol, amount):
    client.new_order(symbol=symbol, side='BUY', type='MARKET', quantity=amount)

# Given the symbol of a coin, purchase it with the given amount using limit order
def purchase_coin_limit(symbol, amount, price):
    client.new_order(symbol=symbol, side='BUY', type='LIMIT', quantity=amount, price=price)

# Given the symbol of a coin, sell it with the given amount
def sell_coin(symbol, amount):
    client.new_order(symbol=symbol, side='SELL', type='MARKET', quantity=amount)

def replace_order(symbol, order_id, quantity, price):
    client.cancel_order(symbol=symbol, orderId=order_id)
    client.new_order(symbol=symbol, side='BUY', type='LIMIT', quantity=quantity, price=price)

def get_balance(type='SPOT'):
    print(client.account_snapshot(type=type))

def main():
    # test case for is_consolidating for BTCUSDT for the past 23 and 24 days respectively
    #print(fetch_high_low_prices('BTCUSDT', '1d', 23))
    #assert is_consolidating(fetch_high_low_prices('BTCUSDT', '1d', 23), 0.05, 23) == True
    #assert is_consolidating(fetch_high_low_prices('BTCUSDT', '1d', 24), 0.05, 24) == False
    get_balance()



if __name__ == "__main__":
    main()
