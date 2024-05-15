def calculate_future_value(present_value, inflation_rate, years):
    """
    Рассчитывает будущую стоимость финансовой цели с учетом инфляции.

    :param present_value: стоимость цели сегодня
    :param inflation_rate: годовая ставка инфляции (в долях)
    :param years: количество лет до достижения цели
    :return: будущая стоимость цели
    """
    future_value = present_value * (1 + inflation_rate/100) ** years

    return future_value


def calculate_amount_of_deductions(future_value, years):
    amount_of_deductions = (future_value / years) / 12
    return amount_of_deductions


def get_user_input():
    """
    Получает ввод данных от пользователя.

    :return: кортеж с введенными значениями
    """
    while True:
        try:
            present_value = float(input("Введите стоимость цели сегодня: "))
            inflation_rate = float(input("Введите годовую ставку инфляции (в долях): "))
            years = float(input("Введите количество лет до достижения цели: "))
            break
        except ValueError:
            print("Ошибка: Введите числовое значение.")
    return present_value, inflation_rate, years
