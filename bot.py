import telebot
import telebot.types as types
import copy

token = "878614712:AAFL9rmzD0--WyFavIxikk9LX3zk_rTyfoY"

bot = telebot.TeleBot(token)

welcome_text = "helno"
welcome_markup = ["add me to queue", "delete me from queue", "show queue"]
normal_murkup = ["add me to queue", "delete me from queue", "show queue"]

queue = []


@bot.message_handler(func=lambda message: message.content_type != "text")
def sticker(message):
    pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Sends welcome message on start command.
    :param message: telebot message object
    """
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for i in welcome_markup:
        markup.add(i)

    print(markup)
    text = welcome_text

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "clear queue")
def clear(message):
    queue = []


@bot.message_handler(func=lambda message: message.text == "add me to queue")
def add_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for i in normal_murkup:
        markup.add(i)

    if message.from_user.username is not None:
        user = [message.from_user.username, message.chat.id]
        if user in queue:
            text = "you are already in"
        else:
            queue.append(user)
            text = "you'r in"
    else:
        text = "you need a username to participate"
    print(queue)

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "delete me from queue")
def delete_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for i in normal_murkup:
        markup.add(i)

    first = copy.copy(queue[0])
    user = [message.from_user.username, message.chat.id]
    if message.from_user.username is not None:
        if user in queue:
            queue.pop(queue.index(user))
            text = "done"
            if queue[0] != first:
                markup2 = types.InlineKeyboardMarkup(row_width=1)
                btn = telebot.types.InlineKeyboardButton(text="i want to be next",
                                                         callback_data=str(user))
                markup2.add(btn)
                bot.send_message(queue[0][1], "your turn", reply_markup=markup2)
        else:
            text = "you are not in queue"
    else:
        text = "you need a username to participate"

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "show queue")
def show_queue_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for i in normal_murkup:
        markup.add(i)

    q = ""
    if queue:
        for i in range(len(queue)):
            q += str(i + 1) + ": " + queue[i][0] + "\n"
    else:
        q = "there is no queue, you can start it"

    text = q

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text[0:len("give space to")] == "give space to")
def give_space_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for i in normal_murkup:
        markup.add(i)
    # skip some users
    first = copy.copy(queue[0])

    user = [message.from_user.username, message.chat.id]

    queue.insert(queue.index(user) + message.text[-1], queue.pop(user))

    if queue[0] != first and len(queue) > 1:
        markup2 = types.InlineKeyboardMarkup(row_width=1)
        btn = telebot.types.InlineKeyboardButton(text="i want to be next",
                                                 callback_data=user)
        markup2.add(btn)
        bot.send_message(queue[0][1], "your turn", reply_markup=markup2)

    text = "done"

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Handel's callback query
    :param call: telebot message object
    """
    message = call.message

    markup2 = types.InlineKeyboardMarkup(row_width=1)
    btn = telebot.types.InlineKeyboardButton(text="i want to be next",
                                             callback_data=queue[0])
    markup2.add(btn)
    bot.send_message(queue[0][1], "your turn", reply_markup=markup2)

    queue.insert(queue.index(call.data) + 1, queue.pop(call.data))

    bot.delete_message(message.chat.id, message.message_id)


bot.polling()

if __name__ == "__main__":
    bot.polling(none_stop=True)
