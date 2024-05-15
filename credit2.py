from tabulate import tabulate

class Loan:
    def __init__(self, principal, interest_rate, duration_years):
        self.principal = principal  # Основная сумма кредита
        self.interest_rate = interest_rate  # Процентная ставка по кредиту (годовая)
        self.duration_years = duration_years  # Срок кредита в годах
        self.monthly_payment = self.calculate_monthly_payment()  # Ежемесячный платеж
        self.total_interest_paid = 0  # Общая сумма выплаченных процентов
        self.payments = []  # Список для хранения информации о платежах

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
        principal_payment = self.monthly_payment - monthly_interest  # Выплата основной суммы
        self.principal -= principal_payment  # Обновление остатка основной суммы кредита
        self.payments.append((self.monthly_payment, principal_payment, monthly_interest, self.principal))

    def print_payments_table(self):
        headers = ["Месяц", "Ежемесячный платеж", "Основной долг", "Начисленные проценты", "Остаток задолженности"]
        data = []
        total_payments = [0] * 4
        for i, payment in enumerate(self.payments, start=1):
            month_data = [i] + list(map(lambda x: round(x, 2), payment))
            total_payments = [sum(x) for x in zip(total_payments, month_data[1:4])]
            data.append(month_data)
        total_payments.insert(0, "Итог:")
        data.append(total_payments)
        print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == '__main__':
    # Получение ввода от пользователя
    principal = float(input("Введите сумму кредита: "))
    interest_rate = float(input("Введите процентную ставку в год: "))
    duration_years = int(input("Введите срок кредита в годах: "))

    # Создание объекта кредита
    credit_loan = Loan(principal=principal, interest_rate=interest_rate, duration_years=duration_years)

    # Симуляция платежей по кредиту в течение срока кредита
    for _ in range(duration_years * 12):
        credit_loan.make_payment()

    # Вывод таблицы платежей
    credit_loan.print_payments_table()
