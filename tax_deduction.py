def calculate_tax_deduction2(salary_per_month, num_children, children_ages):
    # Constants
    tax_rate = 0.13
    child_deduction_1 = 1400
    child_deduction_2 = 1400 * 2
    child_deduction_3_more = 3000
    max_annual_income = 350000

    # Validate input
    if salary_per_month <= 0:
        return "Ошибка: Зарплата должна быть положительным числом."
    if num_children < 0:
        return "Ошибка: количество детей должно быть неотрицательным."
    if any(age <= 0 for age in children_ages):
        return "Ошибка: возраст детей должен быть положительным числом.."

    # Calculate child deductions
    total_child_deduction = 0
    annual_income = 0  # Initialize annual income
    for month in range(12):
        annual_income += salary_per_month  # Add monthly salary to annual income

        # Check if annual income exceeds the limit
        if annual_income > max_annual_income:
            break

        # Calculate child deductions for this month
        for age in children_ages:
            if age < 18:
                if num_children == 1:
                    total_child_deduction += child_deduction_1 * tax_rate
                elif num_children == 2:
                    total_child_deduction += child_deduction_2 * tax_rate
                else:
                    total_child_deduction += (child_deduction_3_more * tax_rate) + (
                            child_deduction_1 * (num_children - 1) * tax_rate)
            break

    return total_child_deduction

# Пример использования функции calculate_tax_deduction
#salary_per_month = 50000
#num_children = 2
#children_ages = [5, 8]  # возрасты ваших детей

#result = calculate_tax_deduction(salary_per_month, num_children, children_ages)
#print(result)
