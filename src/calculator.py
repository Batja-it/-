def calculate_base_cost(selected_items: dict) -> tuple:
    """Рассчитывает базовую стоимость"""
    total_cost = 0.0
    details = []
    for name, info in selected_items.items():
        subtotal = info['price'] * info['count']
        total_cost += subtotal
        details.append(f"{name}: {info['count']} шт. x {info['price']} руб. = {subtotal} руб.")
    return total_cost, details

def validate_order(selected_items: dict) -> bool:
    """Проверяет, что заказ не пуст"""
    return len(selected_items) > 0
