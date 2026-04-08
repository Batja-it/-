"""Дополнительные правила для скидок и наценок"""

def max_discount_limit(discount_percent, max_allowed=30):
    """Ограничение максимальной скидки (например, 30%)"""
    if discount_percent > max_allowed:
        print(f"Скидка {discount_percent}% превышает лимит {max_allowed}%. Установлено {max_allowed}%")
        return max_allowed
    return discount_percent

def markup_by_guests(markup_percent, guests_count):
    """Наценка за обслуживание компании (дополнительное правило)"""
    if guests_count > 4:
        return markup_percent + (guests_count - 4) * 2
    return markup_percent
