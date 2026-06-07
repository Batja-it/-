"""
Модуль основной логики расчёта.
"""

def calculate_base_cost(selected_items):
    """Рассчитывает базовую стоимость всех блюд"""
    total_cost = 0.0
    details = []
    
    for name, info in selected_items.items():
        subtotal = info['price'] * info['count']
        total_cost += subtotal
        details.append(f"{name}: {info['count']} шт. x {info['price']} руб. = {subtotal} руб.")
    
    return total_cost, details


def validate_order(selected_items):
    """Проверяет, что выбран хотя бы один товар"""
    return len(selected_items) > 0
