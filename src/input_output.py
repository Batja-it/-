"""Модуль ввода/вывода данных обеда"""

def input_dishes():
    """
    Ввод блюд от пользователя.
    Возвращает список кортежей: [(название, цена, количество), ...]
    """
    dishes = []
    print("Введите блюда (название, цена, количество). Для завершения введите 'стоп'")
    while True:
        name = input("Название блюда: ").strip()
        if name.lower() == 'стоп':
            break
        try:
            price = float(input("Цена: "))
            quantity = int(input("Количество: "))
            if price < 0 or quantity <= 0:
                print("Цена должна быть ≥0, количество >0")
                continue
            dishes.append((name, price, quantity))
        except ValueError:
            print("Ошибка: введите число")
    return dishes

def input_percentage(prompt):
    """Ввод процента (скидки или наценки)"""
    while True:
        try:
            val = float(input(prompt))
            if 0 <= val <= 100:
                return val
            print("Введите число от 0 до 100")
        except ValueError:
            print("Ошибка: введите число")

def print_receipt(dishes, subtotal, discount_amount, after_discount, markup_amount, total):
    """Вывод чека"""
    print("\n--- ЧЕК ---")
    for name, price, qty in dishes:
        print(f"{name} x{qty} = {price * qty:.2f} ₽")
    print(f"Сумма: {subtotal:.2f} ₽")
    print(f"Скидка: -{discount_amount:.2f} ₽")
    print(f"Сумма после скидки: {after_discount:.2f} ₽")
    print(f"Наценка: +{markup_amount:.2f} ₽")
    print(f"ИТОГО: {total:.2f} ₽")
