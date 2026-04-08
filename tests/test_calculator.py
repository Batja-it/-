import unittest
from src.calculator import calculate_base_cost, validate_order


class TestCalculator(unittest.TestCase):
    """Тесты для модуля calculator.py"""
    
    def test_single_item(self):
        """Тест: одно блюдо"""
        items = {"Цезарь": {"price": 150, "count": 1}}
        total, details = calculate_base_cost(items)
        self.assertEqual(total, 150)
        self.assertEqual(len(details), 1)
    
    def test_multiple_items(self):
        """Тест: несколько блюд"""
        items = {
            "Цезарь": {"price": 150, "count": 2},
            "Компот": {"price": 50, "count": 1}
        }
        total, details = calculate_base_cost(items)
        self.assertEqual(total, 350)
        self.assertEqual(len(details), 2)
    
    def test_zero_items(self):
        """Тест: пустой заказ"""
        items = {}
        total, details = calculate_base_cost(items)
        self.assertEqual(total, 0)
        self.assertEqual(len(details), 0)
    
    def test_max_quantity(self):
        """Тест: максимальное количество порций"""
        items = {"Плов": {"price": 190, "count": 5}}
        total, _ = calculate_base_cost(items)
        self.assertEqual(total, 950)
    
    def test_validate_order_valid(self):
        """Тест: валидация непустого заказа"""
        items = {"Цезарь": {"price": 150, "count": 1}}
        self.assertTrue(validate_order(items))
    
    def test_validate_order_empty(self):
        """Тест: валидация пустого заказа"""
        items = {}
        self.assertFalse(validate_order(items))


if __name__ == "__main__":
    unittest.main()
