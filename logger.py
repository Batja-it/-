"""
Модуль логирования результатов.
"""

import logging
from pathlib import Path


def setup_logging():
    """Настраивает систему логирования"""
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/lunch_calculator.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def log_calculation(selected_items, base_cost, discount, surcharge, final_cost):
    """Записывает результат расчёта в лог"""
    logger = logging.getLogger(__name__)

    items_str = ", ".join([f"{name} x{info['count']}" for name, info in selected_items.items()])

    logger.info(f"Заказ: {items_str}")
    logger.info(f"Базовая стоимость: {base_cost:.2f} руб.")
    logger.info(f"Скидка: {discount:.2f} руб.")
    logger.info(f"Наценка: {surcharge:.2f} руб.")
    logger.info(f"Итог: {final_cost:.2f} руб.")
    logger.info("-" * 40)