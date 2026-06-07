"""
Модуль расчёта скидок и наценок.
"""

def is_peak_hour(hour):
    """Проверяет, является ли час пиковым"""
    return hour in [12, 13, 14, 18, 19, 20]


def calculate_discount(base_cost, has_card):
    """Рассчитывает скидку по карте (10% при сумме > 500)"""
    if has_card and base_cost > 500:
        return base_cost * 0.10
    return 0.0


def calculate_surcharge(base_cost, hour):
    """Рассчитывает наценку за час пик (20%)"""
    if is_peak_hour(hour):
        return base_cost * 0.20
    return 0.0


def apply_discounts_and_surcharges(base_cost, has_card, hour):
    """Применяет скидку и наценку"""
    discount = calculate_discount(base_cost, has_card)
    surcharge = calculate_surcharge(base_cost, hour)
    final_cost = base_cost - discount + surcharge
    return round(final_cost, 2), discount, surcharge
