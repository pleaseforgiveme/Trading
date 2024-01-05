"""
Test functions in binance_tracker.py
"""

import unittest

from binance_tracker import purchase_coin, sell_coin



class IntegerArithmeticTestCase(unittest.TestCase):
    def testAdd(self):  # test method names begin with 'test'
        self.assertEqual((1 + 2), 3)
        self.assertEqual(0 + 1, 1)
    def testMultiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)

# class TestBinanceTracker(unittest.TestCase):
#     def test_purchase_coin(self):
#         self.assertEqual(purchase_coin('BTCUSDT', 0.1), 0.1)

# Test the function purchase_coin in binance_tracker.py
def test_purchase_coin():
    purchase_coin('BTCUSDT', 0.001)

#Test sell coin
def test_sell_coin():
    sell_coin('BTCUSDT', 0.000999)

def main():
    test_sell_coin()

if __name__ == "__main__":
    main()