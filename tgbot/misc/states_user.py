from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from tgbot.text.user import add_bitcoin, order_text
from tgbot.validate.validate import validate_form
from tgbot.keyboards.inline import paid_keyboard
#
from database.database import add_wallet_user, add_amount_btc_wallet


class AmountBitcoin(StatesGroup):
    amount = State()
    wallet = State()


class AddressBitcoin(StatesGroup):
    wallet = State()


async def get_amount(message: types.Message, state: AmountBitcoin.amount):
    async with state.proxy() as data:
        data['text'] = message.text

    res_valid = await validate_form('amount', message)
    if res_valid:
        # Добавляем Сумму BTC в базу данных
        await add_amount_btc_wallet(message.from_user.id, data['text'])

        # Возращаем сообщение пользователю
        await message.answer(add_bitcoin, parse_mode='HTML')
        await AmountBitcoin.next()


async def get_wallet_state(message: types.Message, state: AmountBitcoin.wallet):
    async with state.proxy() as data:
        data['text'] = message.text
    res_valid = await validate_form('bitcoin_wallet', message)
    if res_valid:
        # Добавляем Bitcoin кошелек в базу данных
        await add_wallet_user(message.from_user.id, data['text'], 'buy')
        # Возращаем сообщение пользователю
        text = await order_text(message.from_user.id)
        await message.answer(text, reply_markup=paid_keyboard(), parse_mode='Markdown')
        await state.finish()
