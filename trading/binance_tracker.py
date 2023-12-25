"""
1. Scan all large caps and find candidates as per
1.1 Consolidating. Definition: In the past X days, there existed a local bottom and top.
1.2 Add alert for the top
1.3 (important) When the top is conquered, and it lasts for ~24h, follow to join with 
moderate leverage (e.g. 3X or use the bottom as the liquidation price)
OR just use 1X so can hold if it doesn't play out. 
1.4 Once position opened, use stop order to ride the wave to the top. Adjust stop price 
every 12 - 24h using the 30m chart.

"""

from binance.spot import Spot

client = Spot()

one_trillion = 1_000_000_000_000

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


# main function
def main():
    # test case for is_consolidating for BTCUSDT for the past 23 and 24 days respectively
    print(fetch_high_low_prices('BTCUSDT', '1d', 23))
    #assert is_consolidating(fetch_high_low_prices('BTCUSDT', '1d', 23), 0.05, 23) == True
    #assert is_consolidating(fetch_high_low_prices('BTCUSDT', '1d', 24), 0.05, 24) == False


if __name__ == "__main__":
    main()
