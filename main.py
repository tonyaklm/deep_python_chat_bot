import telebot
from telebot import types
from collections import defaultdict
import random
from PIL import Image
import requests
from io import BytesIO

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
users = defaultdict(lambda: set())
in_ban = defaultdict(lambda: set())
dict_of_name_and_id = dict()
photos = {1: 'https://i.pinimg.com/564x/e5/12/eb/e512ebb615a4652c21eadc2f22be5b3e.jpg',
          2: 'https://i.pinimg.com/564x/45/e5/ac/45e5acdba3171b8fa3ff4dc0201c15af.jpg',
          3: 'https://i.pinimg.com/564x/88/5e/24/885e24e41e27db3aef95851872405afe.jpg',
          4: 'https://i.pinimg.com/750x/9f/8e/36/9f8e36b9ea8af836979f38c10bdc043d.jpg',
          5: 'https://i.pinimg.com/564x/00/95/cd/0095cdfcf7bce2c926a64447cef24411.jpg',
          6: 'https://i.pinimg.com/564x/0c/a0/8c/0ca08c84632d76f96c6173658403e95c.jpg',
          7: 'https://i.pinimg.com/564x/59/6a/bd/596abd83418539633f3a9a28063e4321.jpg',
          8: 'https://i.pinimg.com/564x/79/fa/0a/79fa0a0f69a7c607e11aeab2664b57d2.jpg',
          9: 'https://i.pinimg.com/564x/86/04/c9/8604c9daa52a2885683d40f91dbaff29.jpg',
          10: 'https://i.pinimg.com/564x/5a/67/4a/5a674acf6f98a8cd5d505eef8cd1838f.jpg',
          11: 'https://i.pinimg.com/564x/dd/5f/ec/dd5fec8267799fa35b16d03893b5f965.jpg',
          12: 'https://i.pinimg.com/564x/ef/07/2a/ef072a08441e4f245f6f77874ee1ad66.jpg',
          13: 'https://i.pinimg.com/564x/1b/99/1c/1b991c6f42e913c47c829fc7b6642542.jpg',
          14: 'https://i.pinimg.com/564x/cb/13/d3/cb13d33d5f85ae0e6ae2765efd30fdee.jpg',
          15: 'https://i.pinimg.com/564x/03/33/93/03339378992293f41ede19598fa0a547.jpg',
          16: 'https://i.pinimg.com/564x/b6/fb/ae/b6fbae1f99068e574b28d8d805ea606b.jpg',
          17: 'https://i.pinimg.com/564x/f7/6f/aa/f76faa196bcc3c5aa622db0388db423b.jpg',
          18: 'https://i.pinimg.com/564x/11/c7/e2/11c7e2d9dd83b1391353c5962c951312.jpg',
          19: 'https://i.pinimg.com/564x/3b/e5/14/3be5140e426d4271cc59fd9cfa85fd4b.jpg',
          20: 'https://i.pinimg.com/564x/0e/da/dc/0edadc9a4f5f651d8e8f497b904c3c08.jpg',
          21: 'https://i.pinimg.com/564x/78/69/72/786972cceb9f7bf266778a5775848b12.jpg',
          22: 'https://i.pinimg.com/564x/2a/3c/cf/2a3ccf755d71da13bbf00b7274ea91e7.jpg',
          23: 'https://i.pinimg.com/564x/09/b1/26/09b12648a1a6a70f4ded324527518d25.jpg',
          24: 'https://i.pinimg.com/564x/bf/0f/e5/bf0fe51542fbeed58d4707956ca1682d.jpg',
          25: 'https://i.pinimg.com/564x/6c/bc/ce/6cbcce6ba56c806a67e2e42a8f10fc72.jpg',
          }


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, 'Hey ✌️ , write "/info" to see what i can ')


@bot.message_handler(commands=['set_photo'])
def set_photo(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        markup_reply = types.InlineKeyboardMarkup()
        if bot.user.id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
        else:
            i = random.randint(1, 25)
            response = requests.get(photos[i])
            image = Image.open(BytesIO(response.content))
            bot.set_chat_photo(message.chat.id, photo=image)
    except telebot.apihelper.ApiTelegramException:
        pass


@bot.message_handler(commands=['button', 'info', 'get_info'])
def button_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text="Leave chat", callback_data="leave chat")  # e
    item_2 = types.InlineKeyboardButton(text="Get statistics", callback_data="get statistics")  # e
    item_3 = types.InlineKeyboardButton(text="See description of commands", callback_data="see all options")  # e
    item_4 = types.InlineKeyboardButton(text="Choose somebody to ban", callback_data="ban someone")
    item_5 = types.InlineKeyboardButton(text="Choose somebody to unban", callback_data="unban someone")
    item_6 = types.InlineKeyboardButton(text="Promote somebody to admin", callback_data="make an admin")
    item_7 = types.InlineKeyboardButton(text="Set chat random photo", callback_data="set chat random photo")
    markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)
    bot.send_message(message.chat.id, 'I can:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "leave chat":
        try:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(call.message.chat.id, 'bye', reply_markup=markup_reply)
            bot.leave_chat(call.message.chat.id)
        except telebot.apihelper.ApiTelegramException:
            pass
    elif call.data == "get statistics":
        try:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(call.message.chat.id,
                             f'In this chat {bot.get_chat_members_count(call.message.chat.id)} members '
                             f', {len(bot.get_chat_administrators(call.message.chat.id))} administrators',
                             reply_markup=markup_reply)
        except telebot.apihelper.ApiTelegramException:
            markup_reply = types.InlineKeyboardMarkup()
            try:
                bot.send_message(call.message.chat.id, "group chat was upgraded", reply_markup=markup_reply)
            except telebot.apihelper.ApiTelegramException:
                pass
    elif call.data == "see all options":
        try:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(call.message.chat.id, f'"/start" - to see the greeting. Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id, f'"/info" - to see all options. Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"/ban" - to ban the user which message you reply, you cannot ban another administrator.'
                             f'Administrator cannot ban another administrator.'
                             f' Only administrators can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id, f'"/unban" - to unban the user which message you reply.'
                                                   f' Only administrators can use this function ',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"/admin" - to make an administrator the user which message you reply. '
                             f'Only administrators can use this function ',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"/set_photo" - to set the chat photo by the random. '
                             f'Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"Get statistics" - to see count of members and admins. Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id, f'"Leave chat" - ask bot to leave. Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"Choose somebody to ban" - to choose user from list to ban. '
                             f'Administrator cannot ban another administrator.'
                             f' Only administrators can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"Choose somebody to unban" - to choose user from list to unban. '
                             f'Only administrators can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"Promote somebody to admin" - to choose user from list to Promote somebody to admin. '
                             f'Only administrators can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'"Set chat random photo" - to set the chat photo by the random. '
                             f'Everyone can use this function',
                             reply_markup=markup_reply)
            bot.send_message(call.message.chat.id,
                             f'For all function I need to ba an administrator', reply_markup=markup_reply)
        except telebot.apihelper.ApiTelegramException:
            pass

    elif call.data == "ban someone":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        try:
            admins = bot.get_chat_administrators(call.message.chat.id)
            if bot.user.id not in [user.user.id for user in admins]:
                markup_reply = types.InlineKeyboardMarkup()
                bot.send_message(call.message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
            else:
                markup.add(types.KeyboardButton("cancel"))
                admins = bot.get_chat_administrators(call.message.chat.id)
                for user in users[call.message.chat.id]:
                    if user not in [user1.user.username for user1 in admins]:
                        markup.add(types.KeyboardButton("ban " + user))
                bot.send_message(call.message.chat.id, "Choose somebody to ban", reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            pass
    elif call.data == "unban someone":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        try:
            admins = bot.get_chat_administrators(call.message.chat.id)
            if len(in_ban[call.message.chat.id]) == 0:
                bot.send_message(call.message.chat.id, "Ban list is empty", reply_markup=markup)
            elif bot.user.id not in [user.user.id for user in admins]:
                markup_reply = types.InlineKeyboardMarkup()
                bot.send_message(call.message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
            else:
                markup.add(types.KeyboardButton("cancel"))
                for user in in_ban[call.message.chat.id]:
                    markup.add(types.KeyboardButton("unban " + user))
                bot.send_message(call.message.chat.id, "Choose somebody to unban", reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            pass
    elif call.data == "make an admin":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        try:
            admins = bot.get_chat_administrators(call.message.chat.id)
            if bot.user.id not in [user.user.id for user in admins]:
                markup_reply = types.InlineKeyboardMarkup()
                bot.send_message(call.message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
            else:
                markup.add(types.KeyboardButton("cancel"))
                for user in users[call.message.chat.id]:
                    if user not in [user1.user.username for user1 in admins]:
                        markup.add(types.KeyboardButton("admin " + user))
                bot.send_message(call.message.chat.id, "Choose somebody to make an admin", reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            pass
    elif call.data == "set chat random photo":
        try:
            admins = bot.get_chat_administrators(call.message.chat.id)
            markup_reply = types.InlineKeyboardMarkup()
            if bot.user.id not in [user.user.id for user in admins]:
                bot.send_message(call.message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
            else:
                i = random.randint(1, 25)
                image = types.InputFile(photos[i])
                bot.set_chat_photo(call.message.chat.id, photo=image)
        except telebot.apihelper.ApiTelegramException:
            pass


@bot.message_handler(commands=['ban'])
def ban(message):
    admins = bot.get_chat_administrators(message.chat.id)
    markup_reply = types.InlineKeyboardMarkup()
    if message.reply_to_message:
        new_in_ban = message.reply_to_message.from_user.username
        wish_user_id = message.from_user.id
        if bot.user.id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "I'm not the administrator", reply_markup=markup_reply)

        elif wish_user_id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                             reply_markup=markup_reply)
        else:
            if new_in_ban in [user.user.username for user in admins]:
                bot.send_message(message.chat.id, "You can't ban the administrator", reply_markup=markup_reply)
            else:
                try:
                    bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                    bot.send_message(message.reply_to_message.chat.id,
                                     f'Well done, {message.reply_to_message.from_user.first_name} '
                                     f'{message.reply_to_message.from_user.last_name} in ban',
                                     reply_markup=markup_reply)
                    if message.reply_to_message.from_user.username in users[message.chat.id]:
                        users[message.chat.id].remove(message.reply_to_message.from_user.username)
                    in_ban[message.chat.id].add(new_in_ban)
                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)

    else:
        bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)


@bot.message_handler(commands=['unban'])
def unban(message):
    admins = bot.get_chat_administrators(message.chat.id)
    markup_reply = types.InlineKeyboardMarkup()
    if message.reply_to_message:
        if bot.user.id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "I'm not the administrator", reply_markup=markup_reply)
        elif message.from_user.id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                             reply_markup=markup_reply)
        else:
            bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, f'{message.reply_to_message.from_user.first_name} unban',
                             reply_markup=markup_reply)
            if message.reply_to_message.from_user.username in in_ban[message.chat.id]:
                in_ban[message.chat.id].remove(message.reply_to_message.from_user.username)
    else:
        bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)


@bot.message_handler(commands=['admin'])
def admin(message):
    admins = bot.get_chat_administrators(message.chat.id)
    markup_reply = types.InlineKeyboardMarkup()
    if message.reply_to_message:
        new_admin = message.reply_to_message.from_user.id
        wish_user_id = message.from_user.id
        if new_admin in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, f'{message.reply_to_message.from_user.first_name} already administrator',
                             reply_markup=markup_reply)
        elif bot.user.id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "I'm not the administrator",
                             reply_markup=markup_reply)
        elif wish_user_id not in [user.user.id for user in admins]:
            bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                             reply_markup=markup_reply)
        else:
            try:
                bot.promote_chat_member(chat_id=message.reply_to_message.chat.id,
                                        user_id=new_admin,
                                        can_promote_members=True, can_change_info=True, can_invite_users=True)
                bot.send_message(message.reply_to_message.chat.id,
                                 f'Well done, {message.reply_to_message.from_user.first_name}'
                                 f' {message.reply_to_message.from_user.last_name} is administrator ',
                                 reply_markup=markup_reply)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)
    else:
        bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    first_name = message.new_chat_members[0].first_name
    is_bot = message.new_chat_members[0].is_bot
    last_name = message.new_chat_members[0].last_name
    username = message.new_chat_members[0].username
    user_id = message.new_chat_members[0].id
    if is_bot == False:
        bot.send_message(message.chat.id, f'What is your favourite popug, {first_name} {last_name}?')
        users[message.chat.id].add(username)
        dict_of_name_and_id[username] = user_id
        if username in in_ban[message.chat.id]:
            in_ban[message.chat.id].remove(username)


@bot.message_handler(content_types=["left_chat_member"])
def handler_new_member(message):
    username = message.left_chat_member.username
    if username in users[message.chat.id]:
        users[message.chat.id].remove(username)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    markup_reply = types.ReplyKeyboardRemove()
    admins = bot.get_chat_administrators(message.chat.id)
    if message.text == "cancel":
        bot.send_message(message.chat.id, "OK",
                         reply_markup=markup_reply)
        return
    if len(message.text.split()) == 2:
        command = message.text.split()[0]
        user = message.text.split()[1]
        if command == "ban" and user in users[message.chat.id]:
            wish_user_id = message.from_user.id
            if bot.user.id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "I'm not the administrator", reply_markup=markup_reply)

            elif wish_user_id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                                 reply_markup=markup_reply)
            else:
                if user in [user1.user.username for user1 in admins]:
                    bot.send_message(message.chat.id, "You can't ban the administrator", reply_markup=markup_reply)
                else:
                    try:
                        bot.ban_chat_member(message.chat.id, int(dict_of_name_and_id[user]))
                        bot.send_message(message.chat.id,
                                         f'Well done, {user} in ban',
                                         reply_markup=markup_reply)
                        in_ban[message.chat.id].add(user)
                        if user in users[message.chat.id]:
                            users[message.chat.id].remove(user)
                    except telebot.apihelper.ApiTelegramException:
                        bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)

        elif command == "unban" and user in in_ban[message.chat.id]:
            if bot.user.id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)
            elif message.from_user.id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                                 reply_markup=markup_reply)
            else:
                bot.unban_chat_member(message.chat.id, int(dict_of_name_and_id[user]))
                bot.send_message(message.chat.id, f'{user} unban',
                                 reply_markup=markup_reply)
                if user in in_ban[message.chat.id]:
                    in_ban[message.chat.id].remove(user)

        elif command == "admin" and user in users[message.chat.id]:
            wish_user_id = message.from_user.id
            if user in [user1.user.username for user1 in admins]:
                bot.send_message(message.chat.id,
                                 f'{user} already administrator',
                                 reply_markup=markup_reply)
            elif bot.user.id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "I'm not the administrator",
                                 reply_markup=markup_reply)
            elif wish_user_id not in [user.user.id for user in admins]:
                bot.send_message(message.chat.id, "You don't have such rights. You need to become an administrator",
                                 reply_markup=markup_reply)
            else:
                try:
                    bot.promote_chat_member(chat_id=message.chat.id,
                                            user_id=dict_of_name_and_id[user],
                                            can_promote_members=True, can_change_info=True, can_invite_users=True)
                    bot.send_message(message.chat.id,
                                     f'Well done, {user} is administrator ',
                                     reply_markup=markup_reply)
                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)
    else:
        if message.from_user.username not in users[message.chat.id]:
            dict_of_name_and_id[message.from_user.username] = message.from_user.id
            users[message.chat.id].add(message.from_user.username)
        if message.from_user.username in in_ban[message.chat.id]:
            in_ban[message.chat.id].remove(message.from_user.username)


bot.polling(none_stop=True, interval=0)
