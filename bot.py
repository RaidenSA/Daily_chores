import telebot
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

import database
import properties

bot = telebot.TeleBot(properties.telegram_token)


def add_conn(function):
    def wrapper(message):
        conn = sqlite3.connect(properties.db_name)
        conn.row_factory = database.dict_factory
        function(message, conn)
        conn.close()

    return wrapper


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f'Я бот. Приятно познакомиться, {message.from_user.first_name}\nДля использования бота нужен аккаунт.\nЧтобы подключить существующий используй /login\nДля создания нового используй /register\nЧтобы отвязать акканут используй /logout')


@bot.message_handler(commands=['logout'])
@add_conn
def logout(message, conn):
    telegram = database.get_telegram(conn, message.from_user.id)
    if telegram is None:
        send = bot.send_message(message.from_user.id, f'Телеграм не привязан к аккаунту')
        return

    database.delete_telegram(conn, message.from_user.id)
    conn.commit()
    bot.send_message(message.from_user.id, f'Аккаут {telegram["username"]} отвязан')


@bot.message_handler(commands=['login'])
@add_conn
def login(message, conn):
    telegram = database.get_telegram(conn, message.from_user.id)
    if telegram is not None:
        send = bot.send_message(message.from_user.id, f'Телеграм аккаунт привязан к профилю {telegram["username"]}')
        return

    send = bot.send_message(message.from_user.id, f'Введи свой логин и пароль через пробел')
    bot.register_next_step_handler(send, login_chain)


@add_conn
def login_chain(message, conn):
    username, password = message.text.split(" ", 1)
    user = database.get_user(conn, username)
    if user is None:
        bot.send_message(message.from_user.id, f'Неверный логин или пароль')
        return

    if not check_password_hash(user['password'], password):
        bot.send_message(message.from_user.id, f'Неверный логин или пароль')
        return

    telegram = {"telegram": message.from_user.id, "username": user["username"]}
    database.add_telegram(conn, telegram)
    conn.commit()
    bot.send_message(message.from_user.id, f'Аккаунт {user["username"]} успешно привязан к вашему телеграм')


@bot.message_handler(commands=['register'])
@add_conn
def register(message, conn):
    telegram = database.get_telegram(conn, message.from_user.id)
    if telegram is not None:
        bot.send_message(message.from_user.id, f'Телеграм аккаунт привязан к профилю {telegram["username"]}')
        return

    send = bot.send_message(message.from_user.id, f'Для создания аккаунта введи свой логин и пароль через пробел\nЛогин и пароль должны состоять только из латинских букв и цифр')
    bot.register_next_step_handler(send, register_chain)


@add_conn
def register_chain(message, conn):
    username, password = message.text.split(" ", 1)
    if not username.isalnum() or not password.isalnum():
        bot.send_message(message.from_user.id, f'Логин и пароль должны состоять только из латинских букв и цифр')
        return

    user = database.get_user(conn, username)
    if user is not None:
        bot.send_message(message.from_user.id, f'Такой аккаунт уже существует')
        return

    telegram = {"telegram": message.from_user.id, "username": username}
    user = {"username": username, "password": generate_password_hash(password)}

    database.add_user(conn, user)
    database.add_telegram(conn, telegram)
    conn.commit()
    bot.send_message(message.from_user.id, f'Аккаунт {user["username"]} успешно привязан к вашему телеграм')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        print(type(message.from_user.id))
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


if __name__ == '__main__':
    database.init(sqlite3.connect(properties.db_name))
    bot.polling(none_stop=True)
