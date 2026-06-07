"""
Графический интерфейс на Tkinter для калькулятора обеда
"""

import tkinter as tk
from tkinter import ttk, messagebox
from calculator import calculate_base_cost, validate_order
from discounts import apply_discounts_and_surcharges
from optimizer import optimize_meal

# Меню столовой
MENU = {
    "Цезарь": 150,
    "Оливье": 130,
    "Борщ": 120,
    "Солянка": 140,
    "Гречка с котлетой": 180,
    "Плов": 190,
    "Макароны с сыром": 150,
    "Компот": 50,
    "Чай": 40,
    "Кофе": 80
}


class LunchCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор стоимости обеда")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Стиль
        self.root.configure(bg='#f0f0f0')

        # Заголовок
        title = tk.Label(root, text="🍽 Калькулятор стоимости обеда",
                         font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333')
        title.pack(pady=15)

        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка ручного выбора
        self.manual_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.manual_tab, text="Ручной выбор")

        # Вкладка оптимизации
        self.opt_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.opt_tab, text="Оптимизация")

        self.setup_manual_tab()
        self.setup_opt_tab()

    def setup_manual_tab(self):
        # Рамка для выбора блюд
        frame_items = tk.LabelFrame(self.manual_tab, text="Выберите блюда",
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_items.pack(fill='both', expand=True, padx=10, pady=10)

        # Создаём чекбоксы для блюд
        self.item_vars = {}
        self.item_counts = {}

        # Создаём сетку 2x5
        for i, (name, price) in enumerate(MENU.items()):
            row = i // 5
            col = i % 5

            frame = tk.Frame(frame_items, bg='#f0f0f0')
            frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')

            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=f"{name}\n{price} руб.",
                                variable=var, bg='#f0f0f0', font=('Arial', 10),
                                command=lambda n=name, v=var: self.toggle_count(n, v))
            cb.pack()
            self.item_vars[name] = var

            # Spinbox для количества
            spin = tk.Spinbox(frame, from_=1, to=5, width=5, state='disabled')
            spin.pack(pady=5)
            self.item_counts[name] = spin

        # Рамка с параметрами
        frame_params = tk.LabelFrame(self.manual_tab, text="Параметры заказа",
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_params.pack(fill='x', padx=10, pady=10)

        # Час
        tk.Label(frame_params, text="Час посещения (8-20):", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10)
        self.hour_var = tk.IntVar(value=12)
        tk.Scale(frame_params, from_=8, to=20, orient='horizontal',
                 variable=self.hour_var, bg='#f0f0f0').grid(row=0, column=1, padx=10, pady=10)

        # Скидочная карта
        tk.Label(frame_params, text="Скидочная карта:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10)
        self.card_var = tk.BooleanVar()
        tk.Checkbutton(frame_params, text="Есть карта", variable=self.card_var,
                       bg='#f0f0f0').grid(row=1, column=1, padx=10, pady=10)

        # Кнопка расчёта
        btn_calc = tk.Button(self.manual_tab, text="Рассчитать стоимость",
                             command=self.calculate, bg='#4CAF50', fg='white',
                             font=('Arial', 12, 'bold'), padx=20, pady=10)
        btn_calc.pack(pady=10)

        # Результат
        self.result_text = tk.Text(self.manual_tab, height=10, width=70, font=('Courier', 10))
        self.result_text.pack(padx=10, pady=10)

    def setup_opt_tab(self):
        # Рамка для параметров
        frame_params = tk.LabelFrame(self.opt_tab, text="Параметры оптимизации",
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_params.pack(fill='x', padx=10, pady=10)

        # Бюджет
        tk.Label(frame_params, text="Бюджет (руб.):", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10)
        self.budget_var = tk.IntVar(value=300)
        tk.Entry(frame_params, textvariable=self.budget_var, width=10).grid(row=0, column=1, padx=10, pady=10)

        # Час
        tk.Label(frame_params, text="Час посещения:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10)
        self.opt_hour_var = tk.IntVar(value=12)
        tk.Scale(frame_params, from_=8, to=20, orient='horizontal',
                 variable=self.opt_hour_var, bg='#f0f0f0').grid(row=1, column=1, padx=10, pady=10)

        # Скидочная карта
        tk.Label(frame_params, text="Скидочная карта:", bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=10)
        self.opt_card_var = tk.BooleanVar()
        tk.Checkbutton(frame_params, text="Есть карта", variable=self.opt_card_var,
                       bg='#f0f0f0').grid(row=2, column=1, padx=10, pady=10)

        # Кнопка оптимизации
        btn_opt = tk.Button(self.opt_tab, text="Подобрать оптимальный набор",
                            command=self.optimize, bg='#2196F3', fg='white',
                            font=('Arial', 12, 'bold'), padx=20, pady=10)
        btn_opt.pack(pady=10)

        # Результат
        self.opt_result_text = tk.Text(self.opt_tab, height=15, width=70, font=('Courier', 10))
        self.opt_result_text.pack(padx=10, pady=10)

    def toggle_count(self, name, var):
        """Включение/выключение выбора количества"""
        if var.get():
            self.item_counts[name].config(state='normal')
        else:
            self.item_counts[name].config(state='disabled')
            self.item_counts[name].delete(0, tk.END)
            self.item_counts[name].insert(0, '1')

    def calculate(self):
        """Расчёт стоимости"""
        selected = {}
        for name, var in self.item_vars.items():
            if var.get():
                count = int(self.item_counts[name].get())
                selected[name] = {"price": MENU[name], "count": count}

        if not selected:
            messagebox.showwarning("Ошибка", "Выберите хотя бы одно блюдо!")
            return

        hour = self.hour_var.get()
        has_card = self.card_var.get()

        base_cost, details = calculate_base_cost(selected)
        final_cost, discount, surcharge = apply_discounts_and_surcharges(base_cost, has_card, hour)

        # Показываем результат
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, "ДЕТАЛИЗАЦИЯ ЗАКАЗА\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")

        for detail in details:
            self.result_text.insert(tk.END, f"{detail}\n")

        self.result_text.insert(tk.END, "\n" + "-" * 50 + "\n")
        self.result_text.insert(tk.END, f"Базовая стоимость: {base_cost:>20.2f} руб.\n")
        self.result_text.insert(tk.END, f"Скидка:            {discount:>20.2f} руб.\n")
        self.result_text.insert(tk.END, f"Наценка (час пик): {surcharge:>20.2f} руб.\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        self.result_text.insert(tk.END, f"ИТОГО К ОПЛАТЕ:    {final_cost:>20.2f} руб.\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")

    def optimize(self):
        """Оптимизация под бюджет"""
        budget = self.budget_var.get()
        hour = self.opt_hour_var.get()
        has_card = self.opt_card_var.get()

        # Преобразуем меню в нужный формат
        menu_dict = {str(i): {"name": name, "price": price}
                     for i, (name, price) in enumerate(MENU.items(), 1)}

        result = optimize_meal(menu_dict, budget, has_card, hour)

        self.opt_result_text.delete(1.0, tk.END)
        self.opt_result_text.insert(tk.END, "=" * 50 + "\n")
        self.opt_result_text.insert(tk.END, "ОПТИМАЛЬНЫЙ НАБОР БЛЮД\n")
        self.opt_result_text.insert(tk.END, "=" * 50 + "\n\n")

        if result and result.get("items"):
            for name, info in result["items"].items():
                self.opt_result_text.insert(tk.END, f"  • {name}: {info['count']} шт. x {info['price']} руб.\n")

            self.opt_result_text.insert(tk.END, "\n" + "-" * 50 + "\n")
            self.opt_result_text.insert(tk.END, f"Итоговая стоимость: {result['cost']:.2f} руб.\n")
            self.opt_result_text.insert(tk.END, f"Отклонение от бюджета: {abs(result['cost'] - budget):.2f} руб.\n")
            self.opt_result_text.insert(tk.END, "=" * 50 + "\n")
        else:
            self.opt_result_text.insert(tk.END, "Не удалось подобрать набор блюд под ваш бюджет.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = LunchCalculatorApp(root)
    root.mainloop()