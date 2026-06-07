import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.discounts import (
    is_peak_hour, calculate_discount, 
    calculate_surcharge, apply_discounts_and_surcharges
)


class TestDiscounts(unittest.TestCase):
    def test_peak_hours(self):
        self.assertTrue(is_peak_hour(12))
        self.assertTrue(is_peak_hour(13))
        self.assertTrue(is_peak_hour(18))
        self.assertFalse(is_peak_hour(10))
    
    def test_discount_applies(self):
        discount = calculate_discount(600, True)
        self.assertEqual(discount, 60)
    
    def test_discount_no_card(self):
        discount = calculate_discount(600, False)
        self.assertEqual(discount, 0)
    
    def test_surcharge_peak(self):
        surcharge = calculate_surcharge(100, 13)
        self.assertEqual(surcharge, 20)
    
    def test_surcharge_normal(self):
        surcharge = calculate_surcharge(100, 10)
        self.assertEqual(surcharge, 0)


if __name__ == "__main__":
    unittest.main()
