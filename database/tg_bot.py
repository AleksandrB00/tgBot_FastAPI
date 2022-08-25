import config
import telebot


bot  =telebot.TeleBot(config.bot_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('Кошелек')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)
    text = f'Привет @{message.from_user.username}, я бот, который может управлять кошельками и производить транзакции между ними'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Кошелек')
def wallet(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')   
    markup.add(btn1)
    balance = 0    
    text = f'Ваш баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Перевести')
def transaction(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')   
    markup.add(btn1)   
    text = 'Перевод пока не возможен'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='История')
def transaction(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')   
    markup.add(btn1)   
    text = 'История транзакций пока не доступна'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Меню')
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    text = f'Привет @{message.from_user.username}, я бот, который может управлять кошельками и производить транзакции между ними'
    btn1 = telebot.types.KeyboardButton('Кошелек')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Я в консоли')
def print_me(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    print(message.from_user.to_dict())
    text = f'Ты: {message.from_user.to_dict()}'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == "Я админ, расчехляй мне админ панель")
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Общий баланс')
    btn2 = telebot.types.KeyboardButton('Все пользователи')
    btn3 = telebot.types.KeyboardButton('Данные по пользователю')
    btn4 = telebot.types.KeyboardButton('Удалить пользователя')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Админ-панель'
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Кто я?')
def print_me(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    print(message.from_user.to_dict())
    text = f'Ты: {message.from_user.to_dict()}'
    bot.send_message(message.chat.id, text, reply_markup=markup)

users = config.fake_database['users']
# делаем проверку на админ ли боту пишет проверяем текст сообщения
@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == "Все пользователи")
def all_users(message):
    text = f'Пользователи:'
    inline_markup = telebot.types.InlineKeyboardMarkup()  # создаем объект с инлайн-разметкой
    for user in users:  # в цикле создаем 3 кнопки и добавляем их поочередно в нашу разметку
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                             callback_data=f"user_{user['id']}"))
        # так как мы добавляем кнопки по одной, то у нас юзеры будут в 3 строчки
        # в коллбеке у нас будет текст, который содержит айди юзеров
    bot.send_message(message.chat.id, text,
                     reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению


# в качестве условия для обработки принимает только лямбда-функции
@bot.callback_query_handler(func=lambda call: True)  # хендлер принимает объект Call
def callback_query(call):
    query_type = call.data.split('_')[0]  # получаем тип запроса
    if query_type == 'user':
        user_id = call.data.split('_')[1]  # получаем айди юзера из нашей строки
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            if str(user['id']) == user_id:
                inline_markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='users'),
                                  telebot.types.InlineKeyboardButton(text="Удалить пользователя",
                                                                     callback_data=f'delete_user_{user_id}'))

                bot.edit_message_text(text=f'Данные по пользователю:\n'
                                           f'ID: {user["id"]}\n'
                                           f'Имя: {user["name"]}\n'
                                           f'Ник: {user["nick"]}\n'
                                           f'Баланс: {user["balance"]}',
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=inline_markup)
                print(f"Запрошен {user}")
                break

    if query_type == 'users':
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            # к каждой кнопке прикручиваем в callback_data айди юзера, чтобы можно было идентифицировать нажатую кнопку
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                                 callback_data=f"user_{user['id']}"))
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению

    if query_type == 'delete' and call.data.split('_')[1] == 'user':
        user_id = int(call.data.split('_')[2])  # получаем и превращаем наш айди в число
        for i, user in enumerate(users):
            if user['id'] == user_id:
                print(f'Удален пользователь: {users[i]}')
                users.pop(i)
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                                 callback_data=f"user_{user['id']}"))
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)  # прикрепляем нашу разметку к ответному сообщению


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == "Общий баланс")
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    btn2 = telebot.types.KeyboardButton('Я админ, расчехляй мне админ панель')
    markup.add(btn1, btn2)
    balance = 0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)

if __name__ == '__main__':
    bot.infinity_polling()

