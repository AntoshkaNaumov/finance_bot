import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from state import *
from handler import *  # Импорт обработчиков из handlers.py
from tax_deduction import calculate_tax_deduction2
from social_deductions import calculate_child_education_deduction

# Загрузка переменных окружения из файла .env
load_dotenv()
# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Получение токена бота из переменных окружения
bot_token = os.getenv("BOT_TOKEN")

# Инициализация бота с использованием токена из переменной окружения
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# Регистрация обработчиков
dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(deposit_calculation, lambda message: message.text == "💰🔄 Расчет вклада")
dp.register_message_handler(process_rate, state=DepositCalculationStates.waiting_for_rate)
dp.register_message_handler(process_term, state=DepositCalculationStates.waiting_for_term)
dp.register_message_handler(process_amount, state=DepositCalculationStates.waiting_for_amount)

dp.register_message_handler(personal_budget, text="💰 Личный бюджет")
dp.register_message_handler(process_salary, state=PersonalBudget.waiting_for_salary)
dp.register_message_handler(process_extra_income, state=PersonalBudget.waiting_for_extra_income)
dp.register_message_handler(process_dividends, state=PersonalBudget.waiting_for_dividends)
dp.register_message_handler(process_cashback, state=PersonalBudget.waiting_for_cashback)
dp.register_message_handler(process_rental_income, state=PersonalBudget.waiting_for_rental_income)
dp.register_message_handler(process_government_support,
                            state=PersonalBudget.waiting_for_government_support)
dp.register_message_handler(process_rent, state=PersonalBudget.waiting_for_rent)
dp.register_message_handler(process_groceries, state=PersonalBudget.waiting_for_groceries)
dp.register_message_handler(process_credits, state=PersonalBudget.waiting_for_credits)
dp.register_message_handler(process_other_expenses, state=PersonalBudget.waiting_for_other_expenses)
dp.register_message_handler(process_other_leisure, state=PersonalBudget.waiting_for_leisure)
dp.register_message_handler(process_education, state=PersonalBudget.waiting_for_education)
dp.register_message_handler(process_other_optional_expenses, state=PersonalBudget.waiting_for_other_optional_expenses)
dp.register_message_handler(credit_calculator, text="🏦 Кредитный калькулятор")
dp.register_message_handler(process_principal, state=LoanState.waiting_for_principal)
dp.register_message_handler(process_interest_rate, state=LoanState.waiting_for_interest_rate)
dp.register_message_handler(process_duration, state=LoanState.waiting_for_duration)
dp.register_message_handler(financial_goal, text="🏆 Финансовая цель")
dp.register_message_handler(future_cost_goal, text="📈 Будущая стоимость цели")
dp.register_message_handler(process_present_value, state=FutureCostGoalStates.WaitingForPresentValue)
dp.register_message_handler(process_inflation_rate, state=FutureCostGoalStates.WaitingForInflationRate)
dp.register_message_handler(process_years, state=FutureCostGoalStates.WaitingForYears)

dp.register_message_handler(time_to_achieve_goal, text="⏳ Срок достижения цели")
dp.register_message_handler(process_goal_name, state=TimeToAchieveGoalStates.WaitingForGoalName)
dp.register_message_handler(process_target_amount, state=TimeToAchieveGoalStates.WaitingForTargetAmount)
dp.register_message_handler(process_current_savings, state=TimeToAchieveGoalStates.WaitingForCurrentSavings)
dp.register_message_handler(process_monthly_savings, state=TimeToAchieveGoalStates.WaitingForMonthlySavings)
dp.register_message_handler(go_back_to_main_menu, text="🔙 Назад")

dp.register_message_handler(tax_deduction, text="💸 Налоговый вычет")
dp.register_message_handler(social_deduction_handler, text="Социальный")
dp.register_message_handler(sport_deduction_handler, text="На спорт")
dp.register_message_handler(process_sport_year, state=TaxDeduction2.waiting_for_year)
dp.register_message_handler(process_sport_expenses, state=TaxDeduction2.waiting_for_expenses)

dp.register_message_handler(healthcare_deduction_handler, text="На лечение и лекарства")
dp.register_message_handler(process_healthcare_amount, state=TaxDeduction.waiting_for_healthcare)

dp.register_message_handler(education_deduction_handler, text="На обучение")


# Обработчик для кнопки "На свое обучение, на обучение брата или сестры, а также мужа или жены"
@dp.message_handler(Text(equals="На свое обучение, на обучение брата или сестры, а также мужа или жены"))
async def family_education_handler(message: types.Message):
    await message.answer("Введите год обучения (2021, 2022, 2023, 2024):")
    await MyStates.waiting_for_year.set()  # Переводим пользователя в состояние ожидания ввода года обучения


# Обработчик состояния ожидания ввода года обучения
@dp.message_handler(state=MyStates.waiting_for_year)
async def process_year(message: types.Message, state: FSMContext):
    year = message.text
    if year not in ["2021", "2022", "2023", "2024"]:
        await message.answer("Пожалуйста, введите год обучения корректно (2021, 2022, 2023, 2024):")
        return
    await state.update_data(year=year)
    await message.answer("Введите сумму расходов на обучение:")
    await MyStates.waiting_for_expenses.set()  # Переводим пользователя в состояние ожидания ввода суммы расходов


# Обработчик состояния ожидания ввода суммы расходов
@dp.message_handler(state=MyStates.waiting_for_expenses)
async def process_expenses(message: types.Message, state: FSMContext):
    expenses = message.text
    try:
        expenses = float(expenses)
    except ValueError:
        await message.answer("Пожалуйста, введите сумму расходов на обучение корректно (число):")
        return

    user_data = await state.get_data()
    year = user_data.get("year")
    tax_deduction = calculate_tax_deduction(year, expenses)
    if tax_deduction is not None:
        await message.answer(f"Размер налогового вычета на обучение составляет: {tax_deduction} ₽.")

    await state.finish()  # Завершаем состояние


# Добавим клавиатуру к основному обработчику, чтобы пользователь мог вернуться назад
@dp.message_handler(text="🔙 Назад", state="*")
async def back(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись назад.")
    await state.finish()  # Завершаем состояние


# Обработчик для кнопки "На обучение своих или подопечных детей"
@dp.message_handler(Text(equals="На обучение своих или подопечных детей"))
async def children_education_handler(message: types.Message):
    await message.answer("Введите год обучения ребенка (2021, 2022, 2023, 2024):")
    await MyStates2.waiting_for_year_child.set()  # Переводим пользователя в состояние ожидания ввода года обучения


# Обработчик состояния ожидания ввода года обучения ребенка
@dp.message_handler(state=MyStates2.waiting_for_year_child)
async def process_year_child(message: types.Message, state: FSMContext):
    year = message.text
    if year not in ["2021", "2022", "2023", "2024"]:
        await message.answer("Пожалуйста, введите год обучения ребенка корректно (2021, 2022, 2023, 2024):")
        return
    await state.update_data(year=year)
    await message.answer("Введите сумму расходов на обучение ребенка:")
    await MyStates2.waiting_for_expenses_child.set()  # Переводим пользователя в состояние ожидания ввода суммы расходов


# Обработчик состояния ожидания ввода суммы расходов на обучение ребенка
@dp.message_handler(state=MyStates2.waiting_for_expenses_child)
async def process_expenses_child(message: types.Message, state: FSMContext):
    expenses = message.text
    try:
        expenses = float(expenses)
    except ValueError:
        await message.answer("Пожалуйста, введите сумму расходов на обучение ребенка корректно (число):")
        return

    user_data = await state.get_data()
    year = user_data.get("year")
    tax_deduction = calculate_child_education_deduction(year, expenses)
    if tax_deduction is not None:
        await message.answer(f"Размер налогового вычета на обучение ребенка составляет: {tax_deduction} ₽.")

    await state.finish()  # Завершаем состояние


# Добавим клавиатуру к основному обработчику, чтобы пользователь мог вернуться назад
@dp.message_handler(text="🔙 Назад", state="*")
async def back(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись назад.")
    await state.finish()  # Завершаем состояние


# Обработчик для кнопки "Стандартный"
@dp.message_handler(text="Стандартный", state=None)
async def standard_deduction(message: types.Message):
    await message.answer("Введите вашу зарплату в месяц:")
    await TaxDeductionState.WaitingForSalary.set()


# Обработчик в состоянии ожидания зарплаты
@dp.message_handler(state=TaxDeductionState.WaitingForSalary)
async def process_salary(message: types.Message, state: FSMContext):
    try:
        salary_per_month = float(message.text)
    except ValueError:
        await message.answer("Ошибка: Введите корректное значение для зарплаты.")
        return

    await message.answer("Введите количество ваших детей:")
    await state.update_data(salary_per_month=salary_per_month)
    await TaxDeductionState.WaitingForChildrenNumber.set()


# Обработчик в состоянии ожидания количества детей
@dp.message_handler(state=TaxDeductionState.WaitingForChildrenNumber)
async def process_children_number(message: types.Message, state: FSMContext):
    try:
        num_children = int(message.text)
        if num_children < 0:
            raise ValueError
    except ValueError:
        await message.answer("Ошибка: Введите корректное целое неотрицательное число для количества детей.")
        return

    await message.answer("Введите возраст ваших детей, через пробел:")
    await state.update_data(num_children=num_children)
    await TaxDeductionState.WaitingForChildrenAges.set()


# Обработчик в состоянии ожидания возраста детей
@dp.message_handler(state=TaxDeductionState.WaitingForChildrenAges)
async def process_children_ages(message: types.Message, state: FSMContext):
    children_ages = message.text.split()
    try:
        children_ages = [int(age) for age in children_ages]
        if any(age <= 0 for age in children_ages):
            raise ValueError
    except ValueError:
        await message.answer("Ошибка: Введите корректное положительное число для возраста детей.")
        return

    # Получаем сохраненные данные
    data = await state.get_data()
    salary_per_month = data.get('salary_per_month')
    print(salary_per_month)
    print(children_ages)
    num_children = data.get('num_children')
    print(num_children)

    # Вычисляем налоговый вычет
    result = calculate_tax_deduction2(salary_per_month, num_children, children_ages)

    if isinstance(result, float):
        await message.answer(f"Вам должны в год: {result:.2f} ₽")
    else:
        await message.answer(result)

    # Сброс состояния
    await state.finish()

dp.register_message_handler(property_deduction_handler, text="Имущественный")
dp.register_message_handler(process_mortgage_answer, state=PropertyDeductionState.WaitingForMortgage)
dp.register_message_handler(process_mortgage_interest, state=PropertyDeductionState.WaitingForMortgageInterest)
dp.register_message_handler(process_property_value, state=PropertyDeductionState.WaitingForPropertyValue)


# Обработчик для кнопки "Отправить Донат"
@dp.message_handler(text="🎁 Отправить донат")
async def send_donation(message: types.Message):
    # Путь к изображению
    photo_path = "photo_2024-03-22_10-40-40.jpg"

    # Отправка изображения
    with open(photo_path, "rb") as photo:
        await bot.send_photo(message.chat.id, photo, caption="Поддержите мой проект отправив донат на любую сумму")


# Обработчик для неизвестных команд или кнопок
@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.answer("Извините, я не знаю данной команды. Пожалуйста, воспользуйтесь предложенными кнопками.")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
