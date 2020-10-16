import telebot
import config

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Как дела?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Бай')

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()