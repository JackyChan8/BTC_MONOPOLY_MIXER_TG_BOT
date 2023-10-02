import os
import json
import sqlite3
import aiosqlite

from tgbot.settings import logger


async def create_table():
    """Создание таблиц"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Создаем таблицу wallets
        await cursor.execute("""CREATE TABLE wallets
                                          (
                                          id INTEGER PRIMARY KEY,
                                          bitcoin TEXT NOT NULL
                                          )

        """)
        # Создаем таблицу Реферальный кошелек
        await cursor.execute("""CREATE TABLE wallet_user
                                        (
                                        id_mammoth VARCHAR(30) NOT NULL,
                                        referral_bitcoin TEXT DEFAULT NULL,
                                        user_bitcoin TEXT DEFAULT NULL,
                                        btc_amount_buy TEXT DEFAULT NULL
                                        )

        """)
        # Создаем таблицу mammoths
        await cursor.execute("""CREATE TABLE mammoths
                                        (
                                        id_mammoth VARCHAR(30) NOT NULL,
                                        username VARCHAR(100) NOT NULL,
                                        referral_id INTEGER DEFAULT NULL
                                        )

        """)
        await cursor.close()
        await db.close()
    except aiosqlite.OperationalError as exc:
        logger.error(f"Exception create_table:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


# MIXER
async def add_wallet_user(id, value, action):
    """Изменения кошелька"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        if user:
            # Update Wallet
            if action == 'referrel':
                await cursor.execute(f"UPDATE wallet_user SET referral_bitcoin=? WHERE id_mammoth=?;", (value, id))
                await db.commit()
            elif action == 'buy':
                await cursor.execute(f"UPDATE wallet_user SET user_bitcoin=? WHERE id_mammoth=?;", (value, id))
                await db.commit()
        else:
            # Add To Database
            if action == 'referrel':
                await db.execute("""
                    INSERT INTO wallet_user(id_mammoth, referral_bitcoin) VALUES(?, ?);
                    """, (id, value)
                                 )
                await db.commit()
            elif action == 'buy':
                await db.execute("""
                    INSERT INTO wallet_user(id_mammoth, user_bitcoin) VALUES(?, ?);
                    """, (id, value)
                                 )
                await db.commit()
        await cursor.close()
        await db.close()
    except Exception as exc:
        logger.error(f"Exception update_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


async def add_amount_btc_wallet(id, amount):
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        if user:
            await cursor.execute(f"UPDATE wallet_user SET btc_amount_buy=? WHERE id_mammoth=?;", (amount, id))
            await db.commit()
        else:
            await db.execute("INSERT INTO wallet_user(id_mammoth, btc_amount_buy) VALUES(?, ?);", (id, amount))
            await db.commit()
        await cursor.close()
        await db.close()
    except Exception as exc:
        logger.error(f"Exception add_amount_btc_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


async def get_user_wallet(id):
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        await cursor.close()
        await db.close()
        return user
    except Exception as exc:
        logger.error(f"Exception get_user_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()

# ==================================================================================================== #


# Таблица wallets

async def add_wallets():
    """Добавление кошельков"""
    db = await aiosqlite.connect("mydatabase.db")
    try:
        bitcoin_address = os.environ.get('BITCOIN_ADDRESS')
        await db.execute("""
        INSERT INTO wallets(id, bitcoin) VALUES(
            1, ?
        );
        """, (bitcoin_address,))
        await db.commit()
        await db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception add_wallets:  {exc}")
        if db:
            await db.close()


def get_wallet(name_wallet):
    """Получение кошелька"""
    db = sqlite3.connect("mydatabase.db")
    cursor = db.execute(f'SELECT {name_wallet} FROM wallets WHERE id=1;')
    try:
        row = cursor.fetchone()
        if row:
            cursor.close()
            db.close()
            return row[0]
        else:
            cursor.close()
            db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception get_wallet:  {exc}")
        if cursor:
            cursor.close()
        if db:
            db.close()


def get_wallets():
    """Получение кошельков"""
    db = sqlite3.connect("mydatabase.db")
    cursor = db.execute(f'SELECT * FROM wallets WHERE id=1;')
    try:
        row = cursor.fetchone()
        if row:
            cursor.close()
            db.close()
            return row
        else:
            cursor.close()
            db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception get_wallets:  {exc}")
        if cursor:
            cursor.close()
        if db:
            db.close()


async def update_wallet(address_bitcoin):
    """Получение кошельков"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.execute(f'SELECT * FROM wallets WHERE id=1;')
    try:
        wallets = await cursor.fetchone()
        if wallets:
            await cursor.execute(f"UPDATE wallets SET bitcoin=? WHERE id=?;", (address_bitcoin, 1))
            await db.commit()
            await cursor.close()
            await db.close()
    except Exception as exc:
        logger.error(f"Exception update_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


async def add_amount_rub_wallet(id, amount):
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        if user:
            await cursor.execute(f"UPDATE wallet_user SET rub_amount_buy=? WHERE id_mammoth=?;", (amount, id))
            await db.commit()
        else:
            await db.execute("INSERT INTO wallet_user(id_mammoth, rub_amount_buy) VALUES(?, ?);", (id, amount))
            await db.commit()
        await cursor.close()
        await db.close()
    except Exception as exc:
        logger.error(f"Exception add_amount_rub_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


async def get_amount_price(id, action):
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        await cursor.close()
        await db.close()
        if action == 'amount_btc':
            return user[-2]
        elif action == 'amount_rub':
            return user[-1]
    except Exception as exc:
        logger.error(f"Exception get_amount_price:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


async def add_method_pay(id, name):
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM wallet_user WHERE id_mammoth=?;', (id,))
        user = await cursor.fetchone()
        if user:
            await cursor.execute(f"UPDATE wallet_user SET choose_method_pay=? WHERE id_mammoth=?;", (name, id))
            await db.commit()
        else:
            await db.execute("INSERT INTO wallet_user(id_mammoth, choose_method_pay) VALUES(?, ?);", (id, name))
            await db.commit()
        await cursor.close()
        await db.close()
    except Exception as exc:
        logger.error(f"Exception add_method_pay:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


# Таблица Мамонты
async def add_mammoths(id_user, username, referrer_id=None):
    """Добавление Мамонта"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM mammoths WHERE id_mammoth=?;', (id_user,))
        user = await cursor.fetchone()
        if not user:
            # Добавление в базу данных
            await db.execute(
                f"INSERT INTO mammoths(id_mammoth, username, referral_id) VALUES(?, ?, ?);", (
                    id_user, username, referrer_id
                )
            )
            await db.commit()
            await db.close()
        else:
            await db.commit()
            await db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception add_mammoths:  {exc}")
        if db:
            await db.close()


def get_mammoths():
    """Получение Мамонтов"""
    db = sqlite3.connect("mydatabase.db")
    cursor = db.execute(f'SELECT * FROM mammoths;')
    try:
        row = cursor.fetchall()
        if row:
            cursor.close()
            db.close()
            return row
        else:
            cursor.close()
            db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception get_mammoths:  {exc}")
        if cursor:
            cursor.close()
        if db:
            db.close()


# Таблицы данных

async def add_shop_data():
    """Добавление Информации: Города, Районы, Продукты"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Проверка на существование в Базе Данных
        await cursor.execute(f'SELECT * FROM shop WHERE id_shop=1;')
        shop_info = await cursor.fetchone()
        if not shop_info:
            # Добавление в базу данных
            with open('data.json', encoding='utf-8-sig') as json_file:
                json_data = json.loads(json_file.read())

            await db.execute("""
                                INSERT INTO shop(id_shop, data) VALUES(
                                    1, ?
                                );
                            """, (json.dumps(json_data),)
                             )
            await db.commit()
            await db.close()
        else:
            await db.commit()
            await db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception add_shop_data:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()


def get_data_shop():
    """Получение Данных"""
    db = sqlite3.connect("mydatabase.db")
    cursor = db.execute('SELECT * FROM shop WHERE id_shop=1;')
    try:
        row = cursor.fetchone()
        if row:
            cursor.close()
            db.close()
            return row
        else:
            cursor.close()
            db.close()
    except (aiosqlite.OperationalError, aiosqlite.IntegrityError) as exc:
        logger.error(f"Exception get_data_shop:  {exc}")
        if cursor:
            cursor.close()
        if db:
            db.close()


async def update_shop_data():
    """Изменения Информации: Города, Районы, Продукты"""
    db = await aiosqlite.connect("mydatabase.db")
    cursor = await db.cursor()
    try:
        # Update Shop Information
        print('1')
        with open('data.json', encoding='utf-8-sig') as json_file:
            json_data = json.loads(json_file.read())

        print('=========================update shop data======================')
        print('================================================================')
        await cursor.execute(f"UPDATE shop SET data=? WHERE id_shop=1;", (json.dumps(json_data),))
        await db.commit()
        await cursor.close()
        await db.close()
    except aiosqlite.OperationalError as exc:
        logger.error(f"Exception update_wallet:  {exc}")
        if cursor:
            await cursor.close()
        if db:
            await db.close()
