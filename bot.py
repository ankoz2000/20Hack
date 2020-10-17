import telebot
import config
import geopy
from telebot import types
from geopy.geocoders import Nominatim, ArcGIS
from analyze import countDistance, countTimeDiff, countIllDist
from user import User, UserInSafety, UserVar
import datetime


bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Да', 'Я в безопасности?')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, хочешь знать, есть ли рядом с тобой зараженные?', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def geophone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    if message.text.lower() == 'да':
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)

    if message.text.lower().replace('?', '') == 'я в безопасности':
        keyboard.add(button_geo)
        s = "Для того, чтобы ответить на твой вопрос, я должен знать где ты находишься"
        bot.send_message(message.chat.id, s, reply_markup=keyboard)

    if message.text.lower().replace('!', '') == 'конечно':
        bot.send_message(message.chat.id, "Собираю информацию...")
        illUser = User()
        healthUser = UserInSafety()
        varUser = UserVar(17, 18, 30)
        #[delta, dateString] = countTimeDiff(illUser)
        [delta, dateString, sickQuantity] = countTimeDiff(varUser)
        mills = countIllDist((healthUser.lt, healthUser.lg), (illUser.lt, illUser.lg))
        s = "Последний раз заболевшие были рядом %s. " % dateString
        quantity = "В радиусе 3 км от тебя %d заболевших" % sickQuantity
        diff = delta.total_seconds()
        print(diff)
        if diff <= 1800:  # 1800 секунд = 30 минут
            s += quantity + "Тебе стоит покинуть это место, инфекция коварна. Не забудь маску!"
            s += "Сейчас в этом районе держится высокий коэффициент заражаемости: %d", 2.28705882352941
        if (diff >= 1800) & (diff <= 21600):
            s += "Обязательно надень маску! Инфекция держится здесь длительное время, но здесь по прежнему не безопасно."
            s += " На данный момент: " + quantity
        if diff > 21600:
            print("hello")
            s += "Это достаточно давно, поэтому не о чем волноваться"
        bot.send_message(message.chat.id, s)


@bot.message_handler(content_types=['location'])
def getLocation(message):
    Fails = []
    if message.location is not None:
        #geolocator = Nominatim(user_agent="my-app")
        geolocator =ArcGIS()
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        bot.send_message(message.chat.id, "Считаю дистанцию до ближайшего заболевшего...")
        km = countDistance((message.location.latitude, message.location.longitude))
        distance = km
        string = "Ближайший заболевший находится в %d километров от вас" % distance
        bot.send_message(message.chat.id, string)

        keyboard2 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard2.row('Конечно!', 'Никак нет!')

        question = "Нужно больше информации?"
        bot.send_message(message.chat.id, question, reply_markup=keyboard2)


bot.polling()