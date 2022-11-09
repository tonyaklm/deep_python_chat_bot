import telebot
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = '5670066727:AAFxJ2yBvPC_xTedxP3nfryPwTXOJbjkgfA'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, "Привет ✌️")


@bot.message_handler(commands=['button', 'info', 'get_info'])
def button_message(message):
    markup = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton(text="leave chat", callback_data="leave chat")
    item_2 = types.InlineKeyboardButton(text="get statistics", callback_data="get statistics")
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, 'I can:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "leave chat":
        markup_reply = types.InlineKeyboardMarkup()
        bot.send_message(call.message.chat.id, 'bye', reply_markup=markup_reply)
        bot.leave_chat(call.message.chat.id)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Success")
    elif call.data == "get statistics":
        markup_reply = types.InlineKeyboardMarkup()
        bot.send_message(call.message.chat.id,
                         f'In this chat {bot.get_chat_members_count(call.message.chat.id)} members '
                         f', {len(bot.get_chat_administrators(call.message.chat.id))} admins',
                         reply_markup=markup_reply)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Success")


@bot.message_handler(commands=['ban'])
def ban(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        if message.reply_to_message and message.from_user.id in [user.user.id for user in admins] and not (
                message.reply_to_message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, f'Sorry, {message.reply_to_message.from_user.first_name}',
                             reply_markup=markup_reply)
            bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        elif message.reply_to_message and message.from_user.id in [user.user.id for user in
                                                                   admins] and message.reply_to_message.from_user.id in [
            user.user.id for user in admins]:

            markup_reply = types.InlineKeyboardMarkup()
            try:
                bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.send_message(message.chat.id, f'Sorry, {message.reply_to_message.from_user.first_name}',
                                 reply_markup=markup_reply)
            except:
                bot.send_message(message.chat.id, "You can't ban the administrator", reply_markup=markup_reply)
        elif message.reply_to_message and not (message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You don't have such rights, become an administrator",
                             reply_markup=markup_reply)
        else:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)
    except:
        markup_reply = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)


@bot.message_handler(commands=['unban'])
def unban(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        if message.reply_to_message and message.from_user.id in [user.user.id for user in admins] and not (
                message.reply_to_message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, f'{message.reply_to_message.from_user.first_name} unban',
                             reply_markup=markup_reply)
        elif message.reply_to_message and not (message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You don't have such rights, become an administrator",
                             reply_markup=markup_reply)
        elif not (message.reply_to_message):
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)
        else:
            pass
    except:
        markup_reply = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        if message.reply_to_message and message.from_user.id in [user.user.id for user in admins] and not (
                message.reply_to_message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.promote_chat_member(chat_id=message.reply_to_message.chat.id,
                                    user_id=message.reply_to_message.from_user.id,
                                    can_promote_members=True, can_change_info=True, can_invite_users=True)
            bot.send_message(message.reply_to_message.chat.id,
                             f'well done, {message.reply_to_message.from_user.first_name} is administrator ',
                             reply_markup=markup_reply)

        elif message.reply_to_message and message.from_user.id in [user.user.id for user in
                                                                   admins] and message.reply_to_message.from_user.id in [
            user.user.id for user in admins]:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, f'{message.reply_to_message.from_user.first_name} already administrator',
                             reply_markup=markup_reply)
        elif message.reply_to_message and not (message.from_user.id in [user.user.id for user in admins]):
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You don't have such rights, become an administrator",
                             reply_markup=markup_reply)
        else:
            markup_reply = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, "You need to reply to the message", reply_markup=markup_reply)
    except:
        markup_reply = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, "I don't have such rights", reply_markup=markup_reply)


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    user_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, "Какой твой любимый попуг, {0}?".format(user_name))


bot.polling(none_stop=True, interval=0)  # запускаем нашего бота
