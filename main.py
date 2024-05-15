import tkinter as tk
from tkinter import messagebox


def calculate_balance():
    try:
        # Получение значений из полей ввода
        salary = float(entry_salary.get()) if entry_salary.get().isdigit() else 0
        extra_income = float(entry_extra_income.get()) if entry_extra_income.get().isdigit() else 0
        dividends = float(entry_dividends.get()) if entry_dividends.get().isdigit() else 0
        cashback = float(entry_cashback.get()) if entry_cashback.get().isdigit() else 0
        rental_income = float(entry_rental_income.get()) if entry_rental_income.get().isdigit() else 0
        government_support = float(entry_government_support.get()) if entry_government_support.get().isdigit() else 0

        rent = float(entry_rent.get()) if entry_rent.get().isdigit() else 0
        groceries = float(entry_groceries.get()) if entry_groceries.get().isdigit() else 0
        credits = float(entry_credits.get()) if entry_credits.get().isdigit() else 0
        other_expenses = float(entry_other_expenses.get()) if entry_other_expenses.get().isdigit() else 0
        leisure = float(entry_leisure.get()) if entry_leisure.get().isdigit() else 0
        education = float(entry_education.get()) if entry_education.get().isdigit() else 0
        other_optional_expenses = float(
            entry_other_optional_expenses.get()) if entry_other_optional_expenses.get().isdigit() else 0

        # Рассчет общего дохода и расходов
        total_income = salary + extra_income + dividends + cashback + rental_income + government_support
        total_expenses = rent + groceries + credits + other_expenses + leisure + education + other_optional_expenses

        # Рассчет баланса
        balance = total_income - total_expenses

        # Обновление меток с результатами
        label_balance.config(text=f"Ваш личный баланс: {balance}")
        label_total_income.config(text=f"Итого доходов: {total_income}")
        label_total_expenses.config(text=f"Итого расходов: {total_expenses}")

        # Расчет и отображение процента сбережений
        if total_income != 0:
            savings_percentage = (balance / total_income) * 100
            label_savings_percentage.config(text=f"Ваш процент сбережений: {savings_percentage:.2f}%")
        else:
            label_savings_percentage.config(text="Ваш процент сбережений: 0.00%")

    except ValueError:
        # Обработка ошибки при неверном формате ввода
        tk.messagebox.showerror("Ошибка", "Неверный формат ввода. Введите числовые значения.")


root = tk.Tk()
root.title("Учет личных финансов")

# Установка размера формы
root.geometry("700x600")  # Ширина x Высота

# Шрифт для заголовка
title_font = ("Arial", 16, "bold")

# Доходы
frame_income = tk.LabelFrame(root, text="Доходы", font=title_font)
frame_income.grid(row=0, column=0, padx=10, pady=5, sticky="w")

label_salary = tk.Label(frame_income, text="Заработная плата в месяц:")
label_salary.grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_salary = tk.Entry(frame_income)
entry_salary.grid(row=0, column=1, padx=5, pady=2)

label_extra_income = tk.Label(frame_income, text="Дополнительный доход:")
label_extra_income.grid(row=1, column=0, padx=5, pady=2, sticky="w")
entry_extra_income = tk.Entry(frame_income)
entry_extra_income.grid(row=1, column=1, padx=5, pady=2)

label_dividends = tk.Label(frame_income, text="Дивиденды:")
label_dividends.grid(row=2, column=0, padx=5, pady=2, sticky="w")
entry_dividends = tk.Entry(frame_income)
entry_dividends.grid(row=2, column=1, padx=5, pady=2)

label_cashback = tk.Label(frame_income, text="Проценты-кэшбэк:")
label_cashback.grid(row=3, column=0, padx=5, pady=2, sticky="w")
entry_cashback = tk.Entry(frame_income)
entry_cashback.grid(row=3, column=1, padx=5, pady=2)

label_rental_income = tk.Label(frame_income, text="Доход от сдачи квартиры в аренду:")
label_rental_income.grid(row=4, column=0, padx=5, pady=2, sticky="w")
entry_rental_income = tk.Entry(frame_income)
entry_rental_income.grid(row=4, column=1, padx=5, pady=2)

label_government_support = tk.Label(frame_income, text="Доходы от государства:")
label_government_support.grid(row=5, column=0, padx=5, pady=2, sticky="w")
entry_government_support = tk.Entry(frame_income)
entry_government_support.grid(row=5, column=1, padx=5, pady=2)

# Расходы
frame_expenses = tk.LabelFrame(root, text="Расходы", font=title_font)
frame_expenses.grid(row=1, column=0, padx=10, pady=5, sticky="w")

label_rent = tk.Label(frame_expenses, text="Аренда:")
label_rent.grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_rent = tk.Entry(frame_expenses)
entry_rent.grid(row=0, column=1, padx=5, pady=2)

label_groceries = tk.Label(frame_expenses, text="Продукты:")
label_groceries.grid(row=1, column=0, padx=5, pady=2, sticky="w")
entry_groceries = tk.Entry(frame_expenses)
entry_groceries.grid(row=1, column=1, padx=5, pady=2)

label_credits = tk.Label(frame_expenses, text="Кредиты:")
label_credits.grid(row=2, column=0, padx=5, pady=2, sticky="w")
entry_credits = tk.Entry(frame_expenses)
entry_credits.grid(row=2, column=1, padx=5, pady=2)

label_other_expenses = tk.Label(frame_expenses, text="Прочие обязательные расходы:")
label_other_expenses.grid(row=3, column=0, padx=5, pady=2, sticky="w")
entry_other_expenses = tk.Entry(frame_expenses)
entry_other_expenses.grid(row=3, column=1, padx=5, pady=2)

label_leisure = tk.Label(frame_expenses, text="Расходы на отпуск и фитнес:")
label_leisure.grid(row=4, column=0, padx=5, pady=2, sticky="w")
entry_leisure = tk.Entry(frame_expenses)
entry_leisure.grid(row=4, column=1, padx=5, pady=2)

label_education = tk.Label(frame_expenses, text="Расходы на образование:")
label_education.grid(row=5, column=0, padx=5, pady=2, sticky="w")
entry_education = tk.Entry(frame_expenses)
entry_education.grid(row=5, column=1, padx=5, pady=2)

label_other_optional_expenses = tk.Label(frame_expenses, text="Прочие необязательные расходы:")
label_other_optional_expenses.grid(row=6, column=0, padx=5, pady=2, sticky="w")
entry_other_optional_expenses = tk.Entry(frame_expenses)
entry_other_optional_expenses.grid(row=6, column=1, padx=5, pady=2)

# Метка для вывода итогов доходов
label_total_income = tk.Label(root, text="Итого доходов: ", font=title_font)
label_total_income.grid(row=4, column=0, padx=10, pady=5)

# Метка для вывода итогов расходов
label_total_expenses = tk.Label(root, text="Итого расходов: ", font=title_font)
label_total_expenses.grid(row=5, column=0, padx=10, pady=5)

# Кнопка для расчета баланса
button_calculate = tk.Button(root, text="Рассчитать баланс", command=calculate_balance)
button_calculate.grid(row=2, column=0, padx=10, pady=5)

# Метка для вывода баланса
label_balance = tk.Label(root, text="Ваш личный баланс: ", font=title_font)
label_balance.grid(row=6, column=0, padx=10, pady=5)

# Метка для вывода процента сбережений
label_savings_percentage = tk.Label(root, text="Ваш процент сбережений: ", font=title_font)
label_savings_percentage.grid(row=7, column=0, padx=10, pady=5)

root.mainloop()
