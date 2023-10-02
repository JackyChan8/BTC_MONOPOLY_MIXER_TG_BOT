import re

from tgbot.text.user import mix_text, add_bitcoin


async def validate_form(form_field, message):
    match form_field:
        case "bitcoin_wallet":
            pattern_btc = r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}'
            bitcoin = re.search(pattern_btc, message.text)
            if not bitcoin:
                await message.answer(f'Неправильный формат Bitcoin кошелька!', parse_mode='Markdown')
                await message.answer(add_bitcoin, parse_mode='HTML')
            else:
                return True
        case "bitcoin_wallet_admin":
            pattern_btc = r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}'
            bitcoin = re.search(pattern_btc, message.text)
            if not bitcoin:
                await message.answer(f'Неправильный формат Bitcoin кошелька!', parse_mode='Markdown')
            else:
                return True
        case "amount":
            if message.text.isdigit():
                return True
            else:
                try:
                    if isinstance(float(message.text), float):
                        return True
                except ValueError:
                    if ',' in message.text:
                        text_user = message.text.replace(',', '.')
                        if text_user.isdigit():
                            return True
                        else:
                            try:
                                if isinstance(float(text_user), float):
                                    return True
                            except ValueError:
                                await message.answer('Не верная сумма обмена!')
                                await message.answer(mix_text, parse_mode='HTML')
                                return False
                    else:
                        await message.answer('Не верная сумма обмена!')
                        await message.answer(mix_text, parse_mode='HTML')
                        return False
        case _:
            pass
