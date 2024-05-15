def calculate_tax_deduction(year, expenses):
    try:
        year = int(year)
        expenses = float(expenses)
    except ValueError:
        print("Ошибка: Год обучения должен быть целым числом, а сумма расходов - числом.")
        return None

    if year < 2021:
        print("Вычет не может быть предоставлен за этот год.")
        return None

    if year == 2021 or year == 2022 or year == 2023:
        max_deduction_amount = 120000
    elif year == 2024:
        max_deduction_amount = 150000
    else:
        print("Неподдерживаемый год.")
        return None

    if expenses <= max_deduction_amount:
        tax_deduction = expenses * 0.13
    else:
        tax_deduction = max_deduction_amount * 0.13

    return tax_deduction


def calculate_child_education_deduction(year, expenses):
    try:
        year = int(year)
        expenses = float(expenses)
    except ValueError:
        print("Ошибка: Год обучения должен быть целым числом, а сумма расходов - числом.")
        return None

    if year < 2021:
        print("Вычет не может быть предоставлен за этот год.")
        return None

    if year <= 2023:
        max_deduction_amount = 50000
    else:
        max_deduction_amount = 110000

    if expenses <= max_deduction_amount:
        tax_deduction = expenses * 0.13
    else:
        tax_deduction = max_deduction_amount * 0.13

    return tax_deduction


if __name__ == '__main__':
    year = input("Введите год обучения ребенка (2021, 2022, 2023, 2024): ")
    expenses = input("Введите сумму расходов на обучение ребенка: ")

    deduction = calculate_child_education_deduction(year, expenses)
    if deduction is not None:
        print("Размер налогового вычета на обучение ребенка составляет:", deduction, "рублей.")
