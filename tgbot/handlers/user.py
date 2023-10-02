from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.text.user import start_text, referral_link_text
from database.database import add_mammoths

# Обменик
from tgbot.keyboards.inline import start_inline_user_keyboadr


# Старт
async def user_start(message: Message):
    if message.chat.type == 'private':
        # Проверка на реферальную программу
        referrer_id = str(message.text[7:])
        if not str(message.from_user.id) == referrer_id:
            if referrer_id:
                await add_mammoths(message.from_user.id, message.from_user.username, referrer_id)
                await message.answer(start_text, reply_markup=start_inline_user_keyboadr())
            else:
                await message.answer(start_text, reply_markup=start_inline_user_keyboadr(), parse_mode='html')
                await add_mammoths(message.from_user.id, message.from_user.username)
        else:
            await message.answer(referral_link_text, reply_markup=start_inline_user_keyboadr())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*", is_admin=False)
