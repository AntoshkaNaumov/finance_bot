from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from property_deduction import calculate_property_deduction
from fin_goal import calculate_future_value, calculate_amount_of_deductions
from financial_goal import calculate_time_and_savings
from social_deductions import calculate_tax_deduction
from state import LoanState, FutureCostGoalStates, TimeToAchieveGoalStates, PersonalBudget, DepositCalculationStates,\
    TaxDeduction, TaxDeduction2, PropertyDeductionState
from credit import Loan
from main2 import calculate_balance, calculate_deposit_amount
from keyboard import finance_keyboard


async def start(message: types.Message):
    await message.answer("Добро пожаловать в finance bot!\nВыберите один из вариантов ниже:",
                         reply_markup=finance_keyboard)


async def deposit_calculation(message: types.Message):
    await message.answer("Давайте начнем расчет вклада.\nВведите годовую ставку (%):")
    await DepositCalculationStates.waiting_for_rate.set()


async def process_rate(message: types.Message, state: FSMContext):
    try:
        rate = float(message.text)
        await state.update_data(rate=rate)
        await message.answer("Введите срок вклада (в годах):")
        await DepositCalculationStates.waiting_for_term.set()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для годовой ставки.")


# Обработчик ввода срока вклада
# @dp.message_handler(state=DepositCalculationStates.waiting_for_term)
async def process_term(message: types.Message, state: FSMContext):
    try:
        term = int(message.text)
        await state.update_data(term=term)
        await message.answer("Введите сумму вклада:")
        await DepositCalculationStates.waiting_for_amount.set()
    except ValueError:
        await message.answer("Пожалуйста, введите целочисленное значение для срока вклада (в годах).")


# Обработчик ввода суммы вклада и расчета результатов
# @dp.message_handler(state=DepositCalculationStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        rate = data.get("rate")
        term = data.get("term")
        total_amount = calculate_deposit_amount(rate, term, amount)
        await message.answer(f"Сумма в конце срока составит: {total_amount:.2f} ₽")
        # Сброс состояний
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для суммы вклада.")


# Обработчик для кнопки "💰 Личный бюджет"
# @dp.message_handler(text="💰 Личный бюджет")
async def personal_budget(message: types.Message):
    await message.answer("Введите свои доходы за месяц, числовое значение:\n"
                         "1. Заработная плата в месяц")
    await PersonalBudget.waiting_for_salary.set()


# Обработчики для каждого параметра ввода данных
# @dp.message_handler(state=PersonalBudget.waiting_for_salary)
async def process_salary(message: types.Message, state: FSMContext):
    try:
        salary = float(message.text)
        await state.update_data(salary=salary)
        await message.answer("2. Введите дополнительный доход:")
        await PersonalBudget.waiting_for_extra_income.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_extra_income)
async def process_extra_income(message: types.Message, state: FSMContext):
    try:
        extra_income = float(message.text)
        await state.update_data(extra_income=extra_income)
        await message.answer("3. Введите дивиденды:")
        await PersonalBudget.waiting_for_dividends.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_dividends)
async def process_dividends(message: types.Message, state: FSMContext):
    try:
        dividends = float(message.text)
        await state.update_data(dividends=dividends)
        await message.answer("4. Введите проценты-кэшбэк:")
        await PersonalBudget.waiting_for_cashback.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_cashback)
async def process_cashback(message: types.Message, state: FSMContext):
    try:
        cashback = float(message.text)
        await state.update_data(cashback=cashback)
        await message.answer("5. Введите доход от сдачи квартиры в аренду:")
        await PersonalBudget.waiting_for_rental_income.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_rental_income)
async def process_rental_income(message: types.Message, state: FSMContext):
    try:
        rental_income = float(message.text)
        await state.update_data(rental_income=rental_income)
        await message.answer("6. Введите доход от государства:")
        await PersonalBudget.waiting_for_government_support.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_government_support)
async def process_government_support(message: types.Message, state: FSMContext):
    try:
        government_support = float(message.text)
        await state.update_data(government_support=government_support)
        await message.answer(
                            "Введите свои расходы за месяц, числовое значение:\n"
                            "1. Введите расходы на аренду:"
                             )
        await PersonalBudget.waiting_for_rent.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_rent)
async def process_rent(message: types.Message, state: FSMContext):
    try:
        rent = float(message.text)
        await state.update_data(rent=rent)
        await message.answer("2. Введите расходы на продукты:")
        await PersonalBudget.waiting_for_groceries.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_groceries)
async def process_groceries(message: types.Message, state: FSMContext):
    try:
        groceries = float(message.text)
        await state.update_data(groceries=groceries)
        await message.answer("3. Введите расходы на кредиты:")
        await PersonalBudget.waiting_for_credits.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_credits)
async def process_credits(message: types.Message, state: FSMContext):
    try:
        credits = float(message.text)
        await state.update_data(credits=credits)
        await message.answer("4. Введите прочие обязательные расходы:")
        await PersonalBudget.waiting_for_other_expenses.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_other_expenses)
async def process_other_expenses(message: types.Message, state: FSMContext):
    try:
        other_expenses = float(message.text)
        await state.update_data(other_expenses=other_expenses)
        await message.answer("5. Введите расходы на отпуск и фитнес:")
        await PersonalBudget.waiting_for_leisure.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_leisure)
async def process_other_leisure(message: types.Message, state: FSMContext):
    try:
        leisure = float(message.text)
        await state.update_data(leisure=leisure)
        await message.answer("5. Введите расходы на образование:")
        await PersonalBudget.waiting_for_education.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# @dp.message_handler(state=PersonalBudget.waiting_for_education)
async def process_education(message: types.Message, state: FSMContext):
    try:
        education = float(message.text)
        await state.update_data(education=education)
        await message.answer("5. Введите прочие необязательные расходы:")
        await PersonalBudget.waiting_for_other_optional_expenses.set()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# Обработчик для последнего параметра, после которого происходит расчет баланса
# @dp.message_handler(state=PersonalBudget.waiting_for_other_optional_expenses)
async def process_other_optional_expenses(message: types.Message, state: FSMContext):
    try:
        other_optional_expenses = float(message.text)
        async with state.proxy() as data:
            # Получаем данные из состояния
            salary = data['salary']
            extra_income = data['extra_income']
            dividends = data['dividends']
            cashback = data['cashback']
            rental_income = data['rental_income']
            government_support = data['government_support']
            rent = data['rent']
            groceries = data['groceries']
            credits = data['credits']
            other_expenses = data['other_expenses']
            leisure = data['leisure']
            education = data['education']
            # Вызываем функцию calculate_balance с полученными данными
            balance, total_income, total_expenses, savings_percentage = calculate_balance(
                salary, extra_income, dividends,
                cashback, rental_income,
                government_support, rent,
                groceries, credits,
                other_expenses, leisure,
                education,
                other_optional_expenses
            )
            # Выводим результат пользователю
            await message.answer(f"Ваш личный баланс: {balance} ₽\n"
                                 f"Итого доходов: {total_income} ₽\n"
                                 f"Итого расходов: {total_expenses} ₽\n"
                                 f"Ваш процент сбережений: {savings_percentage:.2f}%")
            await state.finish()
    except ValueError:
        await message.answer("Ошибка: введите числовое значение.")


# Обработчик для кнопки "Кредитный калькулятор"
# @dp.message_handler(text="🏦 Кредитный калькулятор")
async def credit_calculator(message: types.Message, state: FSMContext):
    await message.answer("Для расчета кредита введите сумму кредита, процентную ставку и срок кредита в годах, "
                         "каждое значение в отдельном сообщении, через Enter.")

    # Установка начального состояния
    await LoanState.waiting_for_principal.set()


# Обработчик ввода суммы кредита
# @dp.message_handler(state=LoanState.waiting_for_principal)
async def process_principal(message: types.Message, state: FSMContext):
    try:
        principal = float(message.text)
        await state.update_data(principal=principal)
        await LoanState.next()
        await message.answer("Введите процентную ставку в год:")
    except ValueError:
        await message.answer("Некорректный ввод. Пожалуйста, введите числовое значение.")


# Обработчик ввода процентной ставки
# @dp.message_handler(state=LoanState.waiting_for_interest_rate)
async def process_interest_rate(message: types.Message, state: FSMContext):
    try:
        interest_rate = float(message.text)
        await state.update_data(interest_rate=interest_rate)
        await LoanState.next()
        await message.answer("Введите срок кредита в годах:")
    except ValueError:
        await message.answer("Некорректный ввод. Пожалуйста, введите числовое значение.")


# Обработчик ввода срока кредита
# @dp.message_handler(state=LoanState.waiting_for_duration)
async def process_duration(message: types.Message, state: FSMContext):
    try:
        duration_years = int(message.text)
        await state.update_data(duration_years=duration_years)

        # Получение данных из состояния
        async with state.proxy() as data:
            principal = data['principal']
            interest_rate = data['interest_rate']
            duration_years = data['duration_years']

        # Создание объекта кредита
        credit_loan = Loan(principal=principal, interest_rate=interest_rate, duration_years=duration_years)

        # Симуляция платежей по кредиту в течение срока кредита
        for _ in range(duration_years * 12):
            credit_loan.make_payment()

        # Отправка результатов пользователю
        await message.answer(f"Ежемесячный платеж: {credit_loan.monthly_payment:.2f}")
        await message.answer(f"Общая сумма выплаченных процентов: {credit_loan.total_interest_paid:.2f}")

        # Сброс состояния
        await state.finish()

    except ValueError:
        await message.answer("Некорректный ввод. Пожалуйста, введите целочисленное значение.")


# Обработчик для кнопки "Финансовая цель"
# @dp.message_handler(text="🏆 Финансовая цель")
async def financial_goal(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    future_cost_button = KeyboardButton("📈 Будущая стоимость цели")
    time_to_achieve_button = KeyboardButton("⏳ Срок достижения цели")
    back_button = KeyboardButton("🔙 Назад")
    keyboard.add(future_cost_button, time_to_achieve_button, back_button)

    await message.answer("Это раздел для расчета финансовой цели. Здесь вы сможете рассчитать цель с учетом инфляции.",
                         reply_markup=keyboard)


# Обработчик для кнопки "Будущая стоимость цели"
# @dp.message_handler(text="📈 Будущая стоимость цели")
async def future_cost_goal(message: types.Message):
    await message.answer("Введите стоимость цели сегодня:")
    await FutureCostGoalStates.WaitingForPresentValue.set()


# @dp.message_handler(state=FutureCostGoalStates.WaitingForPresentValue)
async def process_present_value(message: types.Message, state: FSMContext):
    try:
        present_value = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    await state.update_data(present_value=present_value)
    await message.answer("Введите годовую ставку инфляции (в долях):")
    await FutureCostGoalStates.WaitingForInflationRate.set()


# @dp.message_handler(state=FutureCostGoalStates.WaitingForInflationRate)
async def process_inflation_rate(message: types.Message, state: FSMContext):
    try:
        inflation_rate = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    await state.update_data(inflation_rate=inflation_rate)
    await message.answer("Введите количество лет до достижения цели:")
    await FutureCostGoalStates.WaitingForYears.set()


# @dp.message_handler(state=FutureCostGoalStates.WaitingForYears)
async def process_years(message: types.Message, state: FSMContext):
    try:
        years = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    data = await state.get_data()
    present_value = data.get('present_value')
    inflation_rate = data.get('inflation_rate')

    future_value = calculate_future_value(present_value, inflation_rate, years)
    amount_of_deductions = calculate_amount_of_deductions(future_value, years)

    await message.answer(f"Будущая стоимость цели через {years} лет: {future_value:.2f} ₽")
    await message.answer(f"Величина ежемесячных отчислений составит {amount_of_deductions:.2f} ₽")

    # Завершение состояния
    await state.finish()


# Обработчик для кнопки "Срок достижения цели"
# @dp.message_handler(text="⏳ Срок достижения цели")
async def time_to_achieve_goal(message: types.Message):
    await message.answer("Введите название вашей финансовой цели:")
    await TimeToAchieveGoalStates.WaitingForGoalName.set()


# @dp.message_handler(state=TimeToAchieveGoalStates.WaitingForGoalName)
async def process_goal_name(message: types.Message, state: FSMContext):
    goal_name = message.text.strip()
    if not goal_name:
        await message.answer("Ошибка: Введите непустое название.")
        return

    await state.update_data(goal_name=goal_name)
    await message.answer("Введите сумму, которую вы хотите накопить:")
    await TimeToAchieveGoalStates.WaitingForTargetAmount.set()


# @dp.message_handler(state=TimeToAchieveGoalStates.WaitingForTargetAmount)
async def process_target_amount(message: types.Message, state: FSMContext):
    try:
        target_amount = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    await state.update_data(target_amount=target_amount)
    await message.answer("Введите текущую сумму ваших сбережений:")
    await TimeToAchieveGoalStates.WaitingForCurrentSavings.set()


# @dp.message_handler(state=TimeToAchieveGoalStates.WaitingForCurrentSavings)
async def process_current_savings(message: types.Message, state: FSMContext):
    try:
        current_savings = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    await state.update_data(current_savings=current_savings)
    await message.answer("Введите сумму, которую вы готовы откладывать ежемесячно на вашу цель:")
    await TimeToAchieveGoalStates.WaitingForMonthlySavings.set()


# @dp.message_handler(state=TimeToAchieveGoalStates.WaitingForMonthlySavings)
async def process_monthly_savings(message: types.Message, state: FSMContext):
    try:
        monthly_savings = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите числовое значение.")
        return

    data = await state.get_data()
    goal_name = data.get('goal_name')
    target_amount = data.get('target_amount')
    current_savings = data.get('current_savings')

    # Вызов асинхронной функции из financial_goal.py
    result = await calculate_time_and_savings(goal_name, target_amount, current_savings, monthly_savings)
    await message.answer(result)

    # Завершение состояния
    await state.finish()


# Обработчик для кнопки "Назад"
# @dp.message_handler(text="🔙 Назад")
async def go_back_to_main_menu(message: types.Message):
    await start(message)


# Обработчик для кнопки "Налоговый вычет"
# @dp.message_handler(text="💸 Налоговый вычет")
async def tax_deduction(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    standard_deduction_button = KeyboardButton("Стандартный")
    social_deduction_button = KeyboardButton("Социальный")
    investment_deduction_button = KeyboardButton("Инвестиционный")
    property_deduction_button = KeyboardButton("Имущественный")
    back_button = KeyboardButton("🔙 Назад")
    keyboard.row(standard_deduction_button)
    keyboard.row(social_deduction_button)
    keyboard.row(investment_deduction_button)
    keyboard.row(property_deduction_button)
    keyboard.row(back_button)

    await message.answer("Это раздел для расчета налогового вычета. Здесь вы сможете рассчитать стандартный,"
                         " социальный, инвестиционный, имущественный вычеты.",
                         reply_markup=keyboard)


# Обработчик для кнопки "Социальный"
# @dp.message_handler(text="Социальный")
async def social_deduction_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    education_button = KeyboardButton("На обучение")
    healthcare_button = KeyboardButton("На лечение и лекарства")
    sport_button = KeyboardButton("На спорт")
    back_button = KeyboardButton("🔙 Назад")
    keyboard.row(education_button)
    keyboard.row(healthcare_button)
    keyboard.row(sport_button)
    keyboard.row(back_button)

    await message.answer("Пожалуйста, выберите вид социального вычета для расчета:",
                         reply_markup=keyboard)


# Обработчик для кнопки "На спорт"
# @dp.message_handler(text="На спорт")
async def sport_deduction_handler(message: types.Message, state: FSMContext):
    # Переходим в состояние ожидания года
    await TaxDeduction2.waiting_for_year.set()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton("🔙 Назад")
    keyboard.add(back_button)

    await message.answer("Укажите год в формате ГГГГ:",
                         reply_markup=keyboard)


# Обработчик для ввода года
# @dp.message_handler(state=TaxDeduction2.waiting_for_year)
async def process_sport_year(message: types.Message, state: FSMContext):
    year = message.text

    # Сохраняем введенный год в состоянии
    await state.update_data(year=year)

    # Переходим в состояние ожидания суммы расходов на спорт
    await TaxDeduction2.next()

    await message.answer("Укажите сумму расходов на спорт:")


# Обработчик для ответа на вопрос об указании суммы расходов на спорт
# @dp.message_handler(state=TaxDeduction2.waiting_for_expenses)
async def process_sport_expenses(message: types.Message, state: FSMContext):
    data = await state.get_data()
    year = data.get('year')
    expenses = message.text

    # Вызываем функцию для расчета налогового вычета
    tax_deduction = calculate_tax_deduction(year, expenses)

    if tax_deduction is not None:
        await message.answer(f"Ваш налоговый вычет на спорт составит {tax_deduction} ₽.")
    else:
        await message.answer("Произошла ошибка при расчете налогового вычета. Указан неверный год")

    # Возвращаемся в начальное состояние
    await state.finish()


# Обработчик для кнопки "На лечение и лекарства"
# @dp.message_handler(text="На лечение и лекарства")
async def healthcare_deduction_handler(message: types.Message, state: FSMContext):
    # Переходим в состояние ожидания
    await TaxDeduction.waiting_for_healthcare.set()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton("🔙 Назад")
    keyboard.add(back_button)

    await message.answer("Укажите сумму расходов на лечение и лекарства:",
                         reply_markup=keyboard)


# Обработчик для ответа на вопрос об указании суммы расходов
# @dp.message_handler(state=TaxDeduction.waiting_for_healthcare)
async def process_healthcare_amount(message: types.Message, state: FSMContext):
    expenses = message.text

    # Вызываем функцию для расчета налогового вычета
    tax_deduction = calculate_tax_deduction(2024, expenses)  # Предполагаем, что год всегда 2024

    if tax_deduction is not None:
        await message.answer(f"Ваш налоговый вычет на лечение и лекарства составит {tax_deduction} ₽.")
    else:
        await message.answer("Произошла ошибка при расчете налогового вычета.")

    # Возвращаемся в начальное состояние
    await state.finish()


# Обработчик для кнопки "На обучение"
# @dp.message_handler(text="На обучение")
async def education_deduction_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    children_education_button = KeyboardButton("На обучение своих или подопечных детей")
    family_education_button = KeyboardButton("На свое обучение, на обучение брата или сестры, а также мужа или жены")
    back_button = KeyboardButton("🔙 Назад")
    keyboard.row(children_education_button)
    keyboard.row(family_education_button)
    keyboard.row(back_button)

    await message.answer("Пожалуйста, выберите тип обучения для расчета социального вычета на обучение:",
                         reply_markup=keyboard)


# Обработчик для кнопки "Имущественный"
# @dp.message_handler(text="Имущественный")
async def property_deduction_handler(message: types.Message):
    await message.answer("Брали ли вы ипотеку (да/нет)?")

    # Устанавливаем состояние ожидания ответа на вопрос о наличии ипотеки
    await PropertyDeductionState.WaitingForMortgage.set()


# Обработчик в состоянии ожидания ответа на вопрос о наличии ипотеки
# @dp.message_handler(state=PropertyDeductionState.WaitingForMortgage)
async def process_mortgage_answer(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer not in ['да', 'нет']:
        await message.answer("Пожалуйста, ответьте 'да' или 'нет'.")
        return

    if answer == 'да':
        await message.answer("Введите сумму уплаченных процентов по ипотеке:")
        await PropertyDeductionState.WaitingForMortgageInterest.set()
    else:
        await message.answer("Введите стоимость квартиры или дома:")
        await PropertyDeductionState.WaitingForPropertyValue.set()


# Обработчик в состоянии ожидания ввода суммы уплаченных процентов по ипотеке
# @dp.message_handler(state=PropertyDeductionState.WaitingForMortgageInterest)
async def process_mortgage_interest(message: types.Message, state: FSMContext):
    try:
        mortgage_interest = float(message.text)
        if mortgage_interest < 0:
            raise ValueError("Сумма процентов не может быть отрицательной.")
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        return

    await state.update_data(mortgage_interest=mortgage_interest)
    await message.answer("Введите стоимость квартиры или дома:")
    await PropertyDeductionState.WaitingForPropertyValue.set()


# Обработчик в состоянии ожидания ввода стоимости квартиры
# @dp.message_handler(state=PropertyDeductionState.WaitingForPropertyValue)
async def process_property_value(message: types.Message, state: FSMContext):
    try:
        property_value = float(message.text)
        if property_value < 0:
            raise ValueError("Стоимость квартиры, дома не может быть отрицательной.")
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        return

    # Получаем данные о наличии ипотеки и сумме уплаченных процентов из состояния
    async with state.proxy() as data:
        mortgage_interest = data.get('mortgage_interest', 0)

    # Вызываем функцию из файла property_deduction.py для расчета вычета
    deduction = calculate_property_deduction(property_value, mortgage_interest)

    await message.answer(f"Имущественный налоговый вычет составит: {deduction:.2f} ₽")

    # Сбрасываем состояние
    await state.finish()
