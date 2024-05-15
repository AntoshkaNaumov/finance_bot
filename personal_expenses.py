# Создание словаря для хранения категорий расходов и списков сумм расходов по каждой категории за дни
expenses = {}

# Получение данных от пользователя с обработкой ошибок
while True:
    try:
        days = int(input("Введите количество дней: "))
        break
    except ValueError:
        print("Ошибка: количество дней должно быть целым числом. Попробуйте снова.")

while True:
    try:
        categories = int(input("Введите количество категорий: "))
        break
    except ValueError:
        print("Ошибка: количество категорий должно быть целым числом. Попробуйте снова.")

# Заполнение словаря данными
for day in range(1, days + 1):
    print(f"\nВведите расходы за день {day}:")
    for _ in range(categories):
        while True:
            category = input("Введите название категории: ")
            try:
                # Проверяем, что введенное значение не является числом
                float(category)
                print("Ошибка: название категории должно быть текстом. Попробуйте снова.")
                continue  # Переходим к следующей итерации цикла
            except ValueError:
                pass  # Продолжаем выполнение кода, если значение не является числом

            amount_input = input("Введите сумму расхода: ")
            try:
                amount = float(amount_input)
                break
            except ValueError:
                print("Ошибка: сумма расхода должна быть числом. Попробуйте снова.")

        if category in expenses:
            expenses[category].append(amount)
        else:
            expenses[category] = [amount]


# Подсчет общей суммы расходов за все дни
total_expenses = sum(sum(amounts) for amounts in expenses.values())

# Подсчет сумм расходов по каждой категории за все дни
category_totals = {category: sum(amounts) for category, amounts in expenses.items()}

# Подсчет средних ежедневных расходов для каждой категории
average_daily_expenses = {category: total / days for category, total in category_totals.items()}

# Вывод результатов
print("\nОбщая сумма расходов за все дни:", total_expenses)

print("\nСуммы расходов по категориям за все дни:")
for category, total in category_totals.items():
    print(f"{category}: {total}")

print("\nСредние ежедневные расходы по категориям:")
for category, average in average_daily_expenses.items():
    print(f"{category}: {average:.2f}")
