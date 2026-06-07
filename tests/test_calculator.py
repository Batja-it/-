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
    
    def test_multiple_items(self):
        items = {
            "Цезарь": {"price": 150, "count": 2},
            "Компот": {"price": 50, "count": 1}
        }
        total, _ = calculate_base_cost(items)
        self.assertEqual(total, 350)
    
    def test_empty_order(self):
        self.assertFalse(validate_order({}))
    
    def test_valid_order(self):
        items = {"Цезарь": {"price": 150, "count": 1}}
        self.assertTrue(validate_order(items))


if __name__ == "__main__":
    unittest.main()
