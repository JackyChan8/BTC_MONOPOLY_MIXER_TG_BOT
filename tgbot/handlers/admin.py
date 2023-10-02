from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply_admin import start_admin_keyboard
from tgbot.text.admin import start_text


# Старт
async def admin_start(message: Message):
    await message.answer(start_text, reply_markup=start_admin_keyboard(), parse_mode='Markdown')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
