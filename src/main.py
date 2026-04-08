"""Главный модуль калькулятора обеда"""

from input_output import input_dishes, input_percentage, print_receipt
from calculator import calculate_subtotal, apply_discount_and_markup
from discount_service import max_discount_limit
from logger import log_calculation

def main():
    print("=== Калькулятор стоимости обеда ===")
    
    dishes = input_dishes()
    if not dishes:
        print("Обед не выбран. Завершение.")
        return
    
    subtotal = calculate_subtotal(dishes)
    
    discount = input_percentage("Скидка по карте (%): ")
    discount = max_discount_limit(discount)  # применение ограничения
    
    markup = input_percentage("Наценка за обслуживание (%): ")
    
    after_discount, discount_amount, markup_amount, total = apply_discount_and_markup(
        subtotal, discount, markup
    )
    
    print_receipt(dishes, subtotal, discount_amount, after_discount, markup_amount, total)
    log_calculation(dishes, subtotal, discount, markup, total)

if __name__ == "__main__":
    main()
