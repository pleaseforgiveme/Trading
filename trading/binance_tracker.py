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
