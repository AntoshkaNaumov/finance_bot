from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создание клавиатуры с кнопками
finance_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавление кнопок с текстом
button_personal_budget = KeyboardButton("💰 Личный бюджет")
button_loan_calculator = KeyboardButton("🏦 Кредитный калькулятор")
button_financial_goal = KeyboardButton("🏆 Финансовая цель")
button_tax_deduction = KeyboardButton("💸 Налоговый вычет")
button_send_donation = KeyboardButton("🎁 Отправить донат")
button_deposit_calculation = KeyboardButton("💰🔄 Расчет вклада")

# Добавление кнопок на клавиатуру
finance_keyboard.row(button_personal_budget, button_financial_goal)
finance_keyboard.row(button_loan_calculator, button_deposit_calculation)
finance_keyboard.row(button_tax_deduction, button_send_donation)
