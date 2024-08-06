import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ваш токен, полученный от BotFather
TOKEN = '6816564480:AAHf0UhCNVut2ZGQX0YSZ1WzZeyBwKeGba0'

# Словарь для хранения состояний пользователей
user_states = {}

# Функция старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Стоит два стула: на одном Пики точенные, на другом Хуи дроченные. На какой сам сядешь? На какой мать посадишь?')

# Функция для возврата к вводу пароля
def back_to_the_future(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    update.message.reply_text('Бэк ту зэ фьюче! Введи пароль!')

# Обработка паролей
def handle_password(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    password = update.message.text.strip()
    
    if password == 'Пики точенные':
        user_states[user_id] = 'mode_1'
        update.message.reply_text('Введи сумму с сайта.')
    elif password == 'Хуи дроченные':
        user_states[user_id] = 'mode_2'
        update.message.reply_text('Введи сумму с сайта.')
    else:
        update.message.reply_text('Неверный пароль. Давай шуруй отсюда')

# Обработка чисел
def handle_number(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    mode = user_states.get(user_id)

    if mode is None:
        update.message.reply_text('Э.. Олень, сперва пароль введи.')
        return

    try:
        A = float(update.message.text)

        if mode == 'mode_1':
            # Функционал 1
            CP = A * 10000
            TAX = CP * 0.09
            PIDOR = TAX * 0.30
            TOTAL = CP - PIDOR + 1500000
        elif mode == 'mode_2':
            # Функционал 2
            CP = A * 10000
            TAX = CP * 0.09
            PIDOR = TAX * 0.15
            TOTAL = CP - PIDOR

        # Форматирование результата с пробелами между каждыми тремя цифрами
        formatted_total = "{:,.0f}".format(TOTAL).replace(",", " ")

        update.message.reply_text(f"Итого : {formatted_total}")
    
    except ValueError:
        update.message.reply_text('Руки из жопы?')

def main() -> None:
    # Создание Updater и передача ему токена
    updater = Updater(TOKEN)

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация командного обработчика для команды /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Регистрация командного обработчика для команды /backtothefuture
    dispatcher.add_handler(CommandHandler("backtothefuture", back_to_the_future))

    # Регистрация обработчика сообщений для пароля
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.regex(r'^\d+(\.\d+)?$'), handle_password))

    # Регистрация обработчика сообщений для чисел
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^\d+(\.\d+)?$'), handle_number))

    # Запуск бота
    updater.start_polling()

    # Ожидание завершения программы
    updater.idle()

if __name__ == '__main__':
    main()
