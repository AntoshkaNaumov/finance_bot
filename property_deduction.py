def calculate_property_deduction(property_value, mortgage_interest):
    max_property_with_mortgage = 3000000  # Максимальная сумма квартиры при наличии ипотеки
    max_property_without_mortgage = 2000000  # Максимальная сумма квартиры без ипотеки
    deduction_rate = 0.13  # Ставка налогового вычета

    if mortgage_interest > 0:
        total_value = min(property_value + mortgage_interest, max_property_with_mortgage)
    else:
        total_value = min(property_value, max_property_without_mortgage)

    deduction = total_value * deduction_rate

    return deduction
