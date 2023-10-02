from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from tgbot.text.admin import start_text
from tgbot.keyboards.reply_admin import start_admin_keyboard
from tgbot.validate.validate import validate_form
from database.database import update_wallet


# =========================================== Изменение Кошельков =========================================== #
class BitcoinWalletAdmin(StatesGroup):
    btc_wallet = State()


async def get_text_btc_admin(message: types.Message, state: BitcoinWalletAdmin.btc_wallet):
    async with state.proxy() as data:
        data['text'] = message.text

    if message.text == "❌ Отменить":
        await state.finish()
        await message.answer(start_text, reply_markup=start_admin_keyboard())
    else:
        res_valid = await validate_form('bitcoin_wallet_admin', message)
        if res_valid:
            # Add wallet to database
            await update_wallet(data['text'])
            # Возращаем сообщение пользователю
            await message.reply(
                "🎉 Номер Bitcoin кошелька успешно изменен!",
                reply_markup=start_admin_keyboard()
            )
            await state.finish()
