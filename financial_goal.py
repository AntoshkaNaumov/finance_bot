def get_goal_name():
    while True:
        goal_name = input("Введите название вашей финансовой цели: ")
        if goal_name.strip():  # Проверка на пустую строку
            return goal_name
        else:
            print("Ошибка: Введите непустое название.")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Ошибка: Введите числовое значение.")


async def calculate_time_and_savings(goal_name, target_amount, current_savings, monthly_savings):
    # Вычисление времени, необходимого для достижения цели
    months_to_goal = (target_amount - current_savings) / monthly_savings
    years_to_goal = months_to_goal / 12

    # Вычисление общей суммы сбережений к моменту достижения цели
    total_savings = current_savings + monthly_savings * months_to_goal

    # Вывод результатов
    return (f"Для достижения вашей финансовой цели '{goal_name}' потребуется {months_to_goal:.1f} месяцев или примерно"
            f" {years_to_goal:.1f} лет. Общая сумма ваших сбережений к моменту достижения цели составит"
            f" {total_savings:.2f} ₽.")
