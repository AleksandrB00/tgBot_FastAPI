import config
import telebot
import math

bot  = telebot.TeleBot(config.bot_token)

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

@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == "Админка")
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
total_pages = math.ceil(len(users) / 4)
current_page = 1
user_count = 4


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == 'Все пользователи')
def all_users(message):
    global current_page
    global total_pages
    current_page = 1
    user_count = 4
    text = 'Пользователи:'
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users[:4]:
        inline_markup.add(telebot.types.InlineKeyboardButton(
            text=user['name'],
            callback_data=f'user_{user["id"]}'
        ))
    inline_markup.row(
        telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None'),
        telebot.types.InlineKeyboardButton(text='Вперёд', callback_data='next_page')
    )
    bot.send_message(message.chat.id, text, reply_markup=inline_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global user_count
    global current_page
    global total_pages
    query_type = call.data.split('_')[0]
    if query_type == 'next':
        current_page += 1
        user_count += 4
        inline_markup = telebot.types.InlineKeyboardMarkup()
        if user_count > len(users):
            for user in users[user_count-4:len(users) + 1]:
                inline_markup.add(telebot.types.InlineKeyboardButton(
            text=user['name'],
            callback_data=f'user_{user["id"]}'
        ))
            inline_markup.row(
                telebot.types.InlineKeyboardButton(text='Назад', callback_data='prev_page'),
                telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None')
            )
            bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
            return
        for user in users[user_count-4:user_count]:
            inline_markup.add(telebot.types.InlineKeyboardButton(
            text=user['name'],
            callback_data=f'user_{user["id"]}'
        ))
        inline_markup.row(
            telebot.types.InlineKeyboardButton(text='Назад', callback_data='prev_page'),
            telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None'),
            telebot.types.InlineKeyboardButton(text='Вперёд', callback_data='next_page')
        )
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
    if query_type == 'prev':
        current_page -= 1
        inline_markup = telebot.types.InlineKeyboardMarkup()
        user_count -= 4
        if current_page == 1:
            for user in users[0:4]:
                inline_markup.add(telebot.types.InlineKeyboardButton(
                text=user['name'],
                callback_data=f'user_{user["id"]}'
                ))
            inline_markup.row(
                telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None'),
                telebot.types.InlineKeyboardButton(text='Вперёд', callback_data='next_page')
            )
            bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
            return
        for user in users[user_count-4:user_count]:
            inline_markup.add(telebot.types.InlineKeyboardButton(
            text=user['name'],
            callback_data=f'user_{user["id"]}'
            ))
        inline_markup.row(
            telebot.types.InlineKeyboardButton(text='Назад', callback_data='prev_page'),
            telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None'),
            telebot.types.InlineKeyboardButton(text='Вперёд', callback_data='next_page'),
        )
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
    if query_type == 'user':
        user_id = call.data.split('_')[1]
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            if str(user['id']) == user_id:
                inline_markup.add(
                    telebot.types.InlineKeyboardButton(text='Назад', callback_data='users'),
                    telebot.types.InlineKeyboardButton(text='Удалить пользователя', callback_data=f'delete_user_{user_id}')
                )
                bot.edit_message_text(
                    text=f'Данные по пользователю\n'
                    f'ID:{user["id"]}\n'
                    f'Name:{user["name"]}\n'
                    f'Nick:{user["nick"]}\n'
                    f'Balance:{user["balance"]}\n',
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=inline_markup
                )
                break
    if query_type == 'users':
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users[user_count-4:user_count]:
            inline_markup.add(telebot.types.InlineKeyboardButton(
                text=user["name"],
                callback_data=f'user_{user["id"]}'
            ))
        inline_markup.row(
            telebot.types.InlineKeyboardButton(text='Назад', callback_data='prev_page'),
            telebot.types.InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='None'),
            telebot.types.InlineKeyboardButton(text='Вперёд', callback_data='next_page')
        )
        bot.edit_message_text(
            text='Пользователи:',
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_markup
        )
    if query_type == 'delete' and call.data.split('_')[1] == 'user':
        user_id = int(call.data.split('_')[2])
        for i, user in enumerate(users):
            if user['id'] == user_id:
                users.pop(i)
            inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(
                text=user["name"],
                callback_data=f'user_{user["id"]}'
            ))
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)

@bot.message_handler(func=lambda message: message.from_user.id == config.tg_bot_admin and message.text == 'Общий баланс')
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    btn2 = telebot.types.KeyboardButton('Админка')
    markup.add(btn1, btn2)
    balance = 0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()

