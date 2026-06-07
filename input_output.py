"""
Модуль ввода/вывода данных пользователя.
"""


def show_menu():
    """Отображает меню столовой"""
    menu = {
        "1": {"name": "Цезарь", "price": 150},
        "2": {"name": "Оливье", "price": 130},
        "3": {"name": "Борщ", "price": 120},
        "4": {"name": "Солянка", "price": 140},
        "5": {"name": "Гречка с котлетой", "price": 180},
        "6": {"name": "Плов", "price": 190},
        "7": {"name": "Макароны с сыром", "price": 150},
        "8": {"name": "Компот", "price": 50},
        "9": {"name": "Чай", "price": 40},
        "10": {"name": "Кофе", "price": 80}
    }

    print("\n" + "=" * 40)
    print("          МЕНЮ СТОЛОВОЙ")
    print("=" * 40)
    for key, item in menu.items():
        print(f"  {key}. {item['name']:15} {item['price']:>5} руб.")
    print("=" * 40)

    return menu


def get_user_choice(menu):
    """Запрашивает выбор блюд"""
    selected = {}

    for key, item in menu.items():
        answer = input(f"\nДобавить '{item['name']}'? (д/н): ").strip().lower()

        if answer in ['д', 'y']:
            while True:
                try:
                    count = int(input("  Количество порций (1-5): "))
                    if 1 <= count <= 5:
                        break
                    print("Ошибка! Введите число от 1 до 5")
                except ValueError:
                    print("Ошибка! Введите целое число")

            selected[item['name']] = {
                "price": item['price'],
                "count": count
            }

    return selected


def get_time():
    """Запрашивает час посещения"""
    while True:
        try:
            hour = int(input("\nВведите час посещения (8-20): "))
            if 8 <= hour <= 20:
                return hour
            print("Ошибка! Час должен быть от 8 до 20")
        except ValueError:
            print("Ошибка! Введите целое число")


def has_discount_card():
    """Запрашивает наличие скидочной карты"""
    answer = input("\nЕсть скидочная карта? (д/н): ").strip().lower()
    return answer in ['д', 'y']


def display_result(details, base_cost, discount, surcharge, final_cost):
    """Отображает результат расчёта"""
    print("\n" + "=" * 40)
    print("          ДЕТАЛИЗАЦИЯ ЗАКАЗА")
    print("=" * 40)
    for line in details:
        print(f"  {line}")
    print("-" * 40)
    print(f"  Базовая стоимость: {base_cost:>20.2f} руб.")
    print(f"  Скидка:            {discount:>20.2f} руб.")
    print(f"  Наценка (час пик): {surcharge:>20.2f} руб.")
    print("-" * 40)
    print(f"  ИТОГО К ОПЛАТЕ:    {final_cost:>20.2f} руб.")
    print("=" * 40)