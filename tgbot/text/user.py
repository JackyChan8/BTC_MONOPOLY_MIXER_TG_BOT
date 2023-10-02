import os
import random

import requests

from database.database import get_user_wallet, get_wallets


def get_price(symbol):
    res = requests.get(f'https://api.binance.com/api/v1/ticker/24hr?symbol=BTC{symbol}')

    if res.status_code == 200:
        price = float(res.json()['lastPrice'])
        return price


def to_fixed(numObj, digits=0):
    return f"{numObj:.{digits}}"


name_service = os.environ.get("BOT_NICKNAME")
telegram_support = os.environ.get("TELEGRAM_SUPPORT")
review_chat = os.environ.get("REVIEW_CHAT")
news_channel = os.environ.get("NEWS_CHANNEL")
monopoly_bot = os.environ.get("MONOPOLY_BOT")
mixer_bot = os.environ.get('USERNAME_BOT')

start_text = f"""
<b><a href="https://i.imgur.com/6RtGCgR.png">🤖</a>Бот Миксер!</b>
   
У нас ты можешь замиксовать свои BTC и получить полностью чистые монеты на выходе.

Жми кнопку «⚡️Замиксовать BTC» или просто введи сумму BTC.

Пример: 0.001 или 0,001
 
<b>Резерв: 2.000000 BTC</b>
"""

commision_text = """
<a href="https://i.imgur.com/ozWobSf.png">💰</a> Условия работы с BTC Monopoly Mixer : 

Минимальная сумма сделки : 0.001 BTC 

Комиссия сервиса : 

От 0.5 BTC | 1,7%

От 0.3 до 0.5 BTC | 1,9%

От 0.1 до 0.3 BTC | 2,7%

От 0.03 до 0.1 BTC | 3%

От 0.01 до 0.03 BTC | 3,3%

От 0.004 до 0.01 BTC | 3,5%

От 0.001 до 0.004 BTC | 6,5%
"""

feedback_text = f"""
<a href="https://i.imgur.com/7LmKrnz.png">⏰</a>Круглосуточная техническая поддержка:

@{telegram_support} | Оператор 24/7 на связи и поможет с решением любого вопроса.

🔗Новостной канал BTC MONOPOLY:

@{news_channel} | Наш новостной канал, где мы публикуем актуальную информацию связанную с нашим сервисом.

⚡️Обменник BTC MONOPOLY:

@{monopoly_bot} | Наш обменник. Покупай и продавай BTC. Анонимно, быстро и выгодно.
"""

buy_sell_text = f"""
<b><a href="https://i.imgur.com/4oVLmwd.png">🤖</a>ОБМЕННИК BTC MONOPOLY</b>

Хочешь продать/купить BTC по самому выгодному курсу? Переходи в @{monopoly_bot}.
"""

partner_text = """
<b><a href="https://i.imgur.com/ZTWLQyE.png">📈</a>Условия партнерской программы:</b>

Приглашаем к сотрудничеству всех пользователей. Рекомендуйте наш сервис, делитесь своей реферальной ссылкой и создавайте пассивный доход.

Получайте 0,5% с каждой сделки.

Минимальная сумма на вывод: 0.001 BTC
"""


def my_partner_link(id):
    return f"""
<a href="https://i.imgur.com/ZTWLQyE.png">Ваша</a> ссылка для приглашения партнеров: 

https://t.me/{mixer_bot}?start={id}
Ваша ссылка для приглашения партнеров:
    """


def my_finance_text():
    return """
Общее количество рефералов : 0

Оплаченных заявок : 0

На балансе : 0 BTC

Минимальная сумма на вывод: 0.001 BT
    """


out_back_text = """
Пока что у Вас нет партнерских вознаграждений.

Вы сможете запросить вывод средств, если сумма реферальных вознаграждений достигла или превышает 0.001 BTC
"""

mix_text = """
Укажите сумму в <a href="https://i.imgur.com/PzbRj8m.png">BTC</a> :
Пример : 0.001 или 0,001
"""

add_bitcoin = """
<a href="https://i.imgur.com/AsGQfPZ.png">💰</a> Укажите BTC кошелек. На данный кошелек будут отправлены очищенные средства.
"""


async def order_text(id):
    user = await get_user_wallet(id)
    amount_btc = user[-1]
    if ',' in user[-1]:
        amount_btc = user[-1].replace(',', '.')
    num_order = random.randint(00000000, 99999999)

    get_btc = round(float(amount_btc) - (float(amount_btc) / 100 * 6.5), 6)

    # my_bitcoin_address = os.environ.get('BITCOIN_ADDRESS')
    my_bitcoin_address = get_wallets()

    return f"""
*📝Ваш заказ №{num_order} создан*

Итого к оплате : {amount_btc} BTC

Вы получите на кошелек : {get_btc} BTC

💸После оплаты средства будут переведены на кошелек:
*
{user[2]}
*

Если у вас есть вопрос, или возникли проблемы с оплатой, пишите поддержке : *@{telegram_support}*

🔗Оплатили заявку? Нажмите кнопку "Оплатил".

👇 Переведите средства на данный кошелек: 👇

```{my_bitcoin_address[1]}```
"""

referral_link_text = '❗ Нельзя регистрироваться по собственной реферальной ссылке!'
