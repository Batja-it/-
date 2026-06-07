import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.calculator import calculate_base_cost, validate_order

class TestCalculator(unittest.TestCase):
    def test_single_item(self):
        items = {"Цезарь": {"price": 150, "count": 1}}
        total, _ = calculate_base_cost(items)
        self.assertEqual(total, 150)
    
    def test_validate_order_empty(self):
        self.assertFalse(validate_order({}))

if __name__ == '__main__':
    unittest.main()
