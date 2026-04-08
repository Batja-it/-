"""Модуль базовых расчётов обеда"""

def calculate_subtotal(dishes):
    """
    Расчёт промежуточной суммы.
    dishes: список [(name, price, quantity), ...]
    """
    return sum(price * qty for _, price, qty in dishes)

def apply_discount_and_markup(subtotal, discount_percent, markup_percent):
    """
    Применяет скидку, затем наценку.
    Возвращает (сумма_после_скидки, сумма_скидки, сумма_наценки, итог)
    """
    discount_amount = subtotal * discount_percent / 100
    after_discount = subtotal - discount_amount
    markup_amount = after_discount * markup_percent / 100
    total = after_discount + markup_amount
    return after_discount, discount_amount, markup_amount, total
