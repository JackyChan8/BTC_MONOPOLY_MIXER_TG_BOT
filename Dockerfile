FROM python:3.10.4

WORKDIR /home/Telegram_bot
COPY ./requirements.txt /home/Telegram_bot/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r /home/Telegram_bot/requirements.txt

COPY . /home/Telegram_bot