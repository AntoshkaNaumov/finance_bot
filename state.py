from aiogram.dispatcher.filters.state import State, StatesGroup


# Определение состояний
class LoanState(StatesGroup):
    waiting_for_principal = State()
    waiting_for_interest_rate = State()
    waiting_for_duration = State()


class FutureCostGoalStates(StatesGroup):
    WaitingForPresentValue = State()
    WaitingForInflationRate = State()
    WaitingForYears = State()


class TimeToAchieveGoalStates(StatesGroup):
    WaitingForGoalName = State()
    WaitingForTargetAmount = State()
    WaitingForCurrentSavings = State()
    WaitingForMonthlySavings = State()


# Определяем состояния
class MyStates(StatesGroup):
    waiting_for_year = State()
    waiting_for_expenses = State()


# Определяем состояния
class MyStates2(StatesGroup):
    waiting_for_year_child = State()
    waiting_for_expenses_child = State()


# Определение состояния для ожидания данных для налогового вычета
class TaxDeductionState(StatesGroup):
    WaitingForSalary = State()
    WaitingForChildrenNumber = State()
    WaitingForChildrenAges = State()


# Определяем состояния (States) для каждого параметра ввода данных
class PersonalBudget(StatesGroup):
    waiting_for_salary = State()
    waiting_for_extra_income = State()
    waiting_for_dividends = State()
    waiting_for_cashback = State()
    waiting_for_rental_income = State()
    waiting_for_government_support = State()
    waiting_for_rent = State()
    waiting_for_groceries = State()
    waiting_for_credits = State()
    waiting_for_other_expenses = State()
    waiting_for_leisure = State()
    waiting_for_education = State()
    waiting_for_other_optional_expenses = State()


# Класс состояний для управления состояниями пользователя
class DepositCalculationStates(StatesGroup):
    waiting_for_rate = State()
    waiting_for_term = State()
    waiting_for_amount = State()


# Определяем состояния
class TaxDeduction(StatesGroup):
    waiting_for_healthcare = State()


# Определяем состояния
class TaxDeduction2(StatesGroup):
    waiting_for_year = State()
    waiting_for_expenses = State()


# Определение состояний для обработки ввода данных для налогового вычета
class PropertyDeductionState(StatesGroup):
    WaitingForMortgage = State()
    WaitingForPropertyValue = State()
    WaitingForMortgageInterest = State()
