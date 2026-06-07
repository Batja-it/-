"""
Главный модуль программы.
"""

from input_output import (
    show_menu, get_user_choice, get_time,
    has_discount_card, display_result
)
from calculator import calculate_base_cost, validate_order
from discounts import apply_discounts_and_surcharges
from logger import setup_logging, log_calculation
from optimizer import optimize_meal


def main():
    """Основная функция программы"""
    setup_logging()

    print("\n" + "=" * 50)
    print("   КАЛЬКУЛЯТОР СТОИМОСТИ ОБЕДА")
    print("=" * 50)

    while True:
        print("\nВыберите режим:")
        print("  1. Ручной выбор блюд")
        print("  2. Оптимизация под бюджет")

        mode = input("Ваш выбор (1/2): ").strip()

        if mode == "2":
            menu = show_menu()

            try:
                budget = float(input("\nВаш бюджет (руб.): "))
            except ValueError:
                print("Ошибка! Введите число.")
                continue

            hour = get_time()
            has_card = has_discount_card()

            result = optimize_meal(menu, budget, has_card, hour)

            if result and result.get("items"):
                print("\n" + "=" * 40)
                print("     ОПТИМАЛЬНЫЙ НАБОР")
                print("=" * 40)
                for name, info in result["items"].items():
                    print(f"  • {name}: {info['count']} шт. x {info['price']} руб.")
                print("-" * 40)
                print(f"  Итог: {result['cost']:.2f} руб.")
                print(f"  Отклонение: {abs(result['cost'] - budget):.2f} руб.")
                print("=" * 40)

                base_sum = sum(v['price'] * v['count'] for v in result["items"].values())
                log_calculation(result["items"], base_sum, 0, 0, result["cost"])
            else:
                print("\nНе удалось подобрать набор.")

        else:
            menu = show_menu()
            selected_items = get_user_choice(menu)

            if not validate_order(selected_items):
                print("\nОшибка: Вы не выбрали ни одного блюда!")
                continue

            hour = get_time()
            has_card = has_discount_card()

            base_cost, details = calculate_base_cost(selected_items)
            final_cost, discount, surcharge = apply_discounts_and_surcharges(
                base_cost, has_card, hour
            )

            display_result(details, base_cost, discount, surcharge, final_cost)
            log_calculation(selected_items, base_cost, discount, surcharge, final_cost)

        again = input("\nРассчитать ещё? (д/н): ").strip().lower()
        if again not in ['д', 'y', 'да']:
            print("\nДо свидания!")
            break


if __name__ == "__main__":
    main()