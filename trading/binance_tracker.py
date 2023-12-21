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

#
def track_top_breakthrough():
    # for each candidate, do:
    pass

def is_consolidating(prices, percentage, days=0):
    # scan for the past d days for daily high/low
    resistance = 0 # also record the highest date(s)
    support = 0  # also record the lowest date(s)
    for price in prices:
        resistance = max(resistance, price)
        support = min(resistance, price)
    bandwidth = resistance - support
    highest_days = []
    lowest_days = []
    # consolidation should satisfy the following:
    # 1. Today's highest <= resistance && lowest >= support
    # 2. at least two dates close to resistance or support,
    # i.e. |price - resistance| / resistance <= X% (or support)
    # We may need to tighten this rule to filter out fake ones.
    if prices[-1] > resistance or prices[-1] < support:
        return False
    highest_count, lowest_count = 0, 0
    for price in prices:
        if (resistance - price) / resistance <= percentage:
            highest_count += 1
        elif (price - support) / support <= percentage:
            lowest_count += 1
    return highest_count >= 2 or lowest_count >= 2
