import unittest
from src.discounts import (
    is_peak_hour, calculate_discount, 
    calculate_surcharge, apply_discounts_and_surcharges
)


class TestDiscounts(unittest.TestCase):
    """Тесты для модуля discounts.py"""
    
    def test_is_peak_hour_true(self):
        """Тест: часы пик"""
        peak_hours = [12, 13, 14, 18, 19, 20]
        for hour in peak_hours:
            self.assertTrue(is_peak_hour(hour))
    
    def test_is_peak_hour_false(self):
        """Тест: не часы пик"""
        non_peak_hours = [8, 9, 10, 11, 15, 16, 17]
        for hour in non_peak_hours:
            self.assertFalse(is_peak_hour(hour))
    
    def test_discount_applies(self):
        """Тест: скидка применяется при сумме >500 и наличии карты"""
        discount = calculate_discount(600, True)
        self.assertEqual(discount, 60)
    
    def test_discount_no_card(self):
        """Тест: скидка не применяется без карты"""
        discount = calculate_discount(600, False)
        self.assertEqual(discount, 0)
    
    def test_discount_low_amount(self):
        """Тест: скидка не применяется при сумме <=500"""
        discount = calculate_discount(500, True)
        self.assertEqual(discount, 0)
    
    def test_surcharge_peak_hour(self):
        """Тест: наценка в час пик"""
        surcharge = calculate_surcharge(100, 13)
        self.assertEqual(surcharge, 20)
    
    def test_surcharge_non_peak(self):
        """Тест: нет наценки вне часов пик"""
        surcharge = calculate_surcharge(100, 10)
        self.assertEqual(surcharge, 0)
    
    def test_combined_discount_and_surcharge(self):
        """Тест: одновременное применение скидки и наценки"""
        final, discount, surcharge = apply_discounts_and_surcharges(600, True, 12)
        self.assertEqual(final, 660)  # 600 - 60 + 120
        self.assertEqual(discount, 60)
        self.assertEqual(surcharge, 120)


if __name__ == "__main__":
    unittest.main()
