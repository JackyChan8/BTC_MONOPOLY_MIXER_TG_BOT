import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_right_price(price):
    return f'{price[0]} {price[1::]}'


telegram_support = os.environ.get("TELEGRAM_SUPPORT")
review_chat = os.environ.get("REVIEW_CHAT")
news_channel = os.environ.get("NEWS_CHANNEL")
mixer_bot = os.environ.get("MIXER_BOT")


def start_inline_user_keyboadr():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    mix_btc = InlineKeyboardButton('⚡️Замиксовать BTC', callback_data='️Mix')
    partner_program = InlineKeyboardButton('💸 Партнерская программа', callback_data="Partner Programm")
    buy_sell_btc = InlineKeyboardButton('🔗Купить/Продать BTC', callback_data="Buy/Sell BTC")
    feedback = InlineKeyboardButton('📲 Обратная связь', callback_data="Feedback")
    commission = InlineKeyboardButton('Комиссия сервиса', callback_data="Commission")

    buttons \
        .add(mix_btc) \
        .add(partner_program) \
        .add(buy_sell_btc) \
        .add(feedback) \
        .add(commission)

    return buttons


def commission_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    mix_btc = InlineKeyboardButton('⚡️Замиксовать BTC', callback_data='️Mix')

    buttons.add(mix_btc)

    return buttons


def main_menu_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    main_menu = InlineKeyboardButton('Главное меню', callback_data='Main Menu')

    buttons.add(main_menu)

    return buttons


def partner_user_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    my_referral_link = InlineKeyboardButton('🔗Моя реферальная ссылка', callback_data='My partner link')
    my_finance = InlineKeyboardButton('💸Мои финансы', callback_data='My Finance')
    main_menu = InlineKeyboardButton('Главное меню', callback_data='Main Menu')

    buttons \
        .add(my_referral_link) \
        .add(my_finance) \
        .add(main_menu)

    return buttons


def my_finance_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    out_back = InlineKeyboardButton('🚀Вывод', callback_data='Out Back')
    main_menu = InlineKeyboardButton('Главное меню', callback_data='Main Menu')

    buttons \
        .add(out_back) \
        .add(main_menu)

    return buttons


def cancel_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    main_menu = InlineKeyboardButton('🚫Отменить заявку', callback_data='Main Menu')

    buttons.add(main_menu)

    return buttons


def paid_keyboard():
    buttons = InlineKeyboardMarkup(resize_keyboard=True)
    paid = InlineKeyboardButton('✅Оплатил', callback_data='Paid')
    main_menu = InlineKeyboardButton('🚫Отменить заявку', callback_data='Main Menu')

    buttons\
        .add(paid) \
        .add(main_menu)

    return buttons
