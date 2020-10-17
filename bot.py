import telebot
import config
import geopy
from telebot import types
from geopy.geocoders import Nominatim
from analyze import countDistance


bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Да', 'Нет')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, хочешь знать, есть ли рядом с тобой зараженные?)', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def geophone(message):
    if message.text.lower() == 'да':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def getLocation(message):
    Fails = []
    if message.location is not None:
        geolocator = Nominatim(user_agent="my-app")
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        bot.send_message(message.chat.id, "Считаю...")
        mills = countDistance((message.location.latitude, message.location.longitude))
        distance = mills * 1.609344  # Перевод в километры
        string = "Ближайший заболевший находится в %d километров от вас" % distance
        bot.send_message(message.chat.id, string)


bot.polling()