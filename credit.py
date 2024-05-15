class Loan:
    def __init__(self, principal, interest_rate, duration_years):
        self.principal = principal  # Основная сумма кредита
        self.interest_rate = interest_rate  # Процентная ставка по кредиту (годовая)
        self.duration_years = duration_years  # Срок кредита в годах
        self.monthly_payment = self.calculate_monthly_payment()  # Ежемесячный платеж
        self.total_interest_paid = 0  # Общая сумма выплаченных процентов

    def calculate_monthly_payment(self):
        monthly_interest_rate = self.interest_rate / 12 / 100  # Ежемесячная процентная ставка
        num_payments = self.duration_years * 12  # Общее количество платежей
        if monthly_interest_rate != 0:
            # Формула расчета ежемесячного платежа для аннуитетного кредита
            monthly_payment = self.principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) \
                              / ((1 + monthly_interest_rate) ** num_payments - 1)
        else:
            # Для случая без процентов
            monthly_payment = self.principal / num_payments
        return monthly_payment

    def make_payment(self):
        monthly_interest = self.principal * (self.interest_rate / 12 / 100)  # Расчет ежемесячного процента
        self.total_interest_paid += monthly_interest  # Обновление общей суммы выплаченных процентов
        self.principal -= self.monthly_payment - monthly_interest  # Обновление остатка основной суммы кредита


# Функция для безопасного ввода числа с обработкой ошибок
def safe_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Ошибка: Введите число.")


if __name__ == '__main__':
    try:
        # Получение ввода от пользователя
        principal = safe_input("Введите сумму кредита: ")
        interest_rate = safe_input("Введите процентную ставку в год: ")
        duration_years = int(safe_input("Введите срок кредита в годах: "))

        # Создание объекта кредита
        credit_loan = Loan(principal=principal, interest_rate=interest_rate, duration_years=duration_years)

        # Симуляция платежей по кредиту в течение срока кредита
        for _ in range(duration_years * 12):
            credit_loan.make_payment()

        # Вывод ежемесячного платежа
        print(f"Ежемесячный платеж: {credit_loan.monthly_payment:.2f}")

        # Вывод общей суммы процентов по кредиту
        print(f"Общая сумма процентов: {credit_loan.total_interest_paid:.2f}")

    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
