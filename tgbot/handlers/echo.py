from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.text.user import *
from tgbot.misc.states import *

from tgbot.text.admin import num_btc, get_amount_mammoth, get_my_wallets
from tgbot.keyboards.reply_admin import *
from tgbot.text.admin import start_text as start_text_admin

from tgbot.misc.states_user import AmountBitcoin, get_amount, get_wallet_state
from tgbot.keyboards.inline import *


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    print('message - bot_echo_all: ', message)
    if message.document.mime_type == 'application/json':
        pass
    else:
        text = [
            f'Эхо в состоянии {hcode(state_name)}',
            'Содержание сообщения:',
            hcode(message.text)
        ]
        await message.answer('\n'.join(text))


# Команды для пользователя
async def commands_echo_user(message: types.Message):
    print('message - commands_echo_user: ', message)
    match message.text:
        case _:
            await message.answer("Такой команды не существует!")


# Команды для админа
async def commands_echo_admin(message: types.Message):
    match message.text:
        # Главное меню
        case "💰 Посмотреть Кошельки":
            await message.answer(get_my_wallets(), reply_markup=start_admin_keyboard(), parse_mode="Markdown")
        case "Изменить Bitcoin":
            await BitcoinWalletAdmin.btc_wallet.set()
            await message.answer(num_btc, reply_markup=change_admin_wallet())
        case "🦣 Количество Мамонтов":
            await message.answer(get_amount_mammoth())
        case "❌ Отменить":
            await message.answer(start_text_admin, reply_markup=start_admin_keyboard(), parse_mode="Markdown")
        case _:
            await message.answer("Такой команды не существует!")


def register_echo(dp: Dispatcher):
    # dp.register_message_handler(commands_echo_user, is_admin=False)
    dp.register_message_handler(commands_echo_admin, is_admin=True)
    dp.register_message_handler(get_amount, state=AmountBitcoin.amount, is_admin=False)
    dp.register_message_handler(get_wallet_state, state=AmountBitcoin.wallet, is_admin=False)
    dp.register_message_handler(get_text_btc_admin, state=BitcoinWalletAdmin, is_admin=True)

    async def delete_before_message(query: types.CallbackQuery):
        await query.message.delete()

    # Buy Bitcoin

    @dp.callback_query_handler(text='️Mix', is_admin=False)
    async def mix_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await AmountBitcoin.amount.set()
        await query.message.answer(mix_text, reply_markup=cancel_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='Commission', is_admin=False)
    async def commission_service_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(commision_text, reply_markup=commission_user_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='Feedback', is_admin=False)
    async def feedback_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(feedback_text, reply_markup=main_menu_user_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='Main Menu', is_admin=False)
    async def back_main_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(start_text, reply_markup=start_inline_user_keyboadr(), parse_mode='HTML')

    @dp.callback_query_handler(text='Buy/Sell BTC', is_admin=False)
    async def buy_sell_btc_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(buy_sell_text, reply_markup=main_menu_user_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='Partner Programm', is_admin=False)
    async def partner_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(partner_text, reply_markup=partner_user_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='My partner link', is_admin=False)
    async def my_partner_link_command(query: types.CallbackQuery):
        await query.message.answer(
            my_partner_link(query.from_user.id), reply_markup=partner_user_keyboard(), parse_mode='HTML')

    @dp.callback_query_handler(text='My Finance', is_admin=False)
    async def my_finance_command(query: types.CallbackQuery):
        await query.message.answer(my_finance_text(), reply_markup=my_finance_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Out Back', is_admin=False)
    async def out_back_command(query: types.CallbackQuery):
        await delete_before_message(query)
        await query.message.answer(out_back_text, reply_markup=my_finance_keyboard(), parse_mode='Markdown')

    @dp.callback_query_handler(text='Paid', is_admin=False)
    async def paid_command(query: types.CallbackQuery):
        await delete_before_message(query)
        text = await order_text(query.from_user.id)
        await query.message.answer(text, reply_markup=paid_keyboard(), parse_mode='Markdown')
