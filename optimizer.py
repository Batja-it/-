"""
Модуль оптимизации выбора блюд.
"""

from itertools import combinations


def optimize_meal(menu, budget, has_card, hour):
    """Подбирает оптимальный набор блюд под бюджет"""
    from discounts import apply_discounts_and_surcharges

    best_combo = None
    best_diff = float('inf')

    items_list = list(menu.items())

    for r in range(1, 5):
        for combo in combinations(items_list, r):
            selected = {}
            for key, item in combo:
                selected[item['name']] = {"price": item['price'], "count": 1}

            base = sum(v['price'] * v['count'] for v in selected.values())
            final, _, _ = apply_discounts_and_surcharges(base, has_card, hour)

            diff = abs(final - budget)
            if diff < best_diff:
                best_diff = diff
                best_combo = {"items": selected, "cost": final}

    return best_combo