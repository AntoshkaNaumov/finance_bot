def calculate_balance(salary, extra_income, dividends, cashback, rental_income,
                      government_support, rent, groceries, credits, other_expenses,
                      leisure, education, other_optional_expenses):
    try:

        # Рассчет общего дохода и расходов
        total_income = salary + extra_income + dividends + cashback + rental_income + government_support
        total_expenses = rent + groceries + credits + other_expenses + leisure + education + other_optional_expenses

        # Рассчет баланса
        balance = total_income - total_expenses

        # Расчет и отображение процента сбережений
        if total_income != 0:
            savings_percentage = (balance / total_income) * 100
        else:
            return print("Ваш процент сбережений: 0.00%")

        return balance, total_income, total_expenses, savings_percentage

    except ValueError:
        # Обработка ошибки при неверном формате ввода
        print("Ошибка", "Неверный формат ввода. Введите числовые значения.")


def calculate_deposit_amount(annual_interest_rate, deposit_term, initial_deposit_amount):
    try:
        # Проверка на положительные значения
        if annual_interest_rate <= 0 or deposit_term <= 0 or initial_deposit_amount <= 0:
            raise ValueError("Все значения должны быть положительными")

        # Расчет суммы в конце срока
        total_amount = initial_deposit_amount * (1 + annual_interest_rate / 100) ** deposit_term

        return round(total_amount, 2)  # Округляем до двух знаков после запятой
    except ValueError as ve:
        return "Ошибка: " + str(ve)
    except Exception as e:
        return "Произошла ошибка: " + str(e)


if __name__ == "__main__":
    try:
        annual_rate = float(input("Введите годовую ставку (%): "))
        term = int(input("Введите срок вклада (в годах): "))
        deposit_amount = float(input("Введите сумму вклада: "))

        result = calculate_deposit_amount(annual_rate, term, deposit_amount)
        print("Сумма в конце срока составит:", result)
    except ValueError as ve:
        print("Ошибка ввода данных:", ve)
    except Exception as e:
        print("Произошла ошибка:", e)
