def is_peak_hour(hour: int) -> bool:
    """Проверка часа пик"""
    return hour in [12, 13, 14, 18, 19, 20]

def calculate_discount(base_cost: float, has_card: bool) -> float:
    """Расчёт скидки 10% при сумме >500 и наличии карты"""
    if has_card and base_cost > 500:
        return base_cost * 0.10
    return 0.0

def calculate_surcharge(base_cost: float, hour: int) -> float:
    """Расчёт наценки 20% в час пик"""
    if is_peak_hour(hour):
        return base_cost * 0.20
    return 0.0

def apply_discounts_and_surcharges(base_cost: float, has_card: bool, hour: int) -> tuple:
    """Применяет скидку и наценку"""
    discount = calculate_discount(base_cost, has_card)
    surcharge = calculate_surcharge(base_cost, hour)
    final_cost = base_cost - discount + surcharge
    return round(final_cost, 2), discount, surcharge
