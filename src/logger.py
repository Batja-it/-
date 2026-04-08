"""Логирование расчётов обеда"""

import datetime

LOG_FILE = "calculations.log"

def log_calculation(dishes, subtotal, discount, markup, total):
    """Запись результата в лог-файл с временной меткой"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n[{timestamp}]\n")
        for name, price, qty in dishes:
            f.write(f"  {name}: {qty} x {price} = {price*qty}\n")
        f.write(f"  Сумма: {subtotal}\n")
        f.write(f"  Скидка: {discount}%\n")
        f.write(f"  Наценка: {markup}%\n")
        f.write(f"  Итог: {total}\n")
