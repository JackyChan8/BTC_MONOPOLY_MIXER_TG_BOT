from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Главное меню клавиатура
def start_admin_keyboard():
    button_wallets = KeyboardButton('💰 Посмотреть Кошельки')
    button_change_btc = KeyboardButton('Изменить Bitcoin')
    button_amount_mammoth = KeyboardButton('🦣 Количество Мамонтов')
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(button_wallets) \
        .row(button_change_btc) \
        .row(button_amount_mammoth)
    return menu


# Клавиатура при изменение кошельков
def change_admin_wallet():
    button_cancel = KeyboardButton('❌ Отменить')
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(button_cancel)
    return menu
