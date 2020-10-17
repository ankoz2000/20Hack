import telebot
import config
import COVID19Py
import requests
from telebot import types
from geopy.geocoders import Nominatim, ArcGIS
from analyze import countDistance, countTimeDiff, countIllDist
from user import User, UserInSafety, UserVar
import res.strings as S

def txt_reader():
    result = ''
    f = open(S.RECOMENDATIONS, 'r', encoding='utf-8')
    for line in f:
        result += line
    return result


bot = telebot.TeleBot(config.token)
#covid19 = COVID19Py.COVID19()

btn_show         = types.KeyboardButton(text=S.COMMAND_SHOW)
btn_sos          = types.KeyboardButton(text=S.COMMAND_SOS)
btn_return       = types.KeyboardButton(text=S.GO_TO_MAIN_MENU)
button_police    = types.InlineKeyboardButton(text="Полиция", url="https://ya.ru")
button_emergency = types.InlineKeyboardButton(text="Скорая", url="https://ya.ru")
button_fire      = types.InlineKeyboardButton(text="Противопожарная служба", url="https://ya.ru")
button_geo       = types.KeyboardButton(text=S.SEND_LOCATION, request_location=True)
btn_rules        = types.KeyboardButton(text=S.RULES)

key          = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard1    = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard2    = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard3    = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard4    = types.InlineKeyboardMarkup()
keyboard_geo = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)


key.add(btn_show, btn_sos)

keyboard_geo.add(button_geo)
keyboard_geo.add(btn_return)

keyboard1.row(S.YES, S.QUESTION_SAFETY)
keyboard1.row(S.GO_TO_MAIN_MENU)

keyboard2.row(S.OF_COURSE, S.GO_TO_MAIN_MENU)

keyboard3.add(btn_rules)
keyboard3.add(btn_return)

keyboard4.row(button_police, button_emergency)
keyboard4.row(button_fire)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, S.MAIN_MENU, reply_markup=key)


@bot.message_handler(commands=['sos'])
def safety(message):
    bot.send_message(message.chat.id, "Список экстренных служб: ", reply_markup=keyboard4)


@bot.message_handler(commands=['show'])
def show(message):
    bot.send_message(message.chat.id, S.QUESTION_SICK, reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def show(message):
    bot.send_message(message.chat.id, S.MAIN_MENU, reply_markup=key)


#   @bot.message_handler(commands=['stat'])
#   def get_stat(message):
#       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#       btn1 = types.KeyboardButton('Во всём мире')
#       btn2 = types.KeyboardButton('Украина')
#       btn3 = types.KeyboardButton('Россия')
#       btn4 = types.KeyboardButton('Беларусь')
#       markup.add(btn1, btn2, btn3, btn4)


@bot.message_handler(content_types=['text'])
def geophone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, S.SHARE_LOCATION, reply_markup=keyboard_geo)

    elif message.text.lower() == S.GO_TO_MAIN_MENU.lower():
        start_message(message)

    elif message.text.lower().replace('?', '') == S.QUESTION_SAFETY.lower().replace('?', ''):
        s = S.WHERE_IS_LOCATION
        bot.send_message(message.chat.id, s, reply_markup=keyboard_geo)

    elif message.text.lower() == S.RULES.lower():
        s = txt_reader()
        bot.send_message(message.chat.id, s, reply_markup=key)

    elif message.text.lower().replace('!', '') == S.OF_COURSE.lower().replace('!', ''):
        bot.send_message(message.chat.id, S.RECEIVING_INFO)
        illUser = User()
        healthUser = UserInSafety()
        varUser = UserVar(17, 18, 30)

        #[delta, dateString] = countTimeDiff(illUser)
        [delta, dateString, sickQuantity] = countTimeDiff(varUser)

        mills = countIllDist((healthUser.lt, healthUser.lg), (illUser.lt, illUser.lg))
        s = "Последний раз заболевшие были рядом %s. " % dateString
        quantity = "В радиусе 3 км от Вас %d заболевших" % sickQuantity
        diff = delta.total_seconds()
        if diff <= 1800:  # 1800 секунд = 30 минут
            s += quantity + S.GO_AWAY
            s += "Сейчас в этом районе держится высокий коэффициент заражаемости: %d", 2.28705882352941
        if (diff >= 1800) & (diff <= 39600):
            s += S.TAKE_MASK
            s += S.AT_THAT_MOMENT + quantity
            s += S.CHECK_RULES
        if diff > 39600:
            s += S.DONT_WORRY
        bot.send_message(message.chat.id, s, reply_markup=keyboard3)
    else:
        bot.send_message(message.chat.id, S.MISUNDERSTANDING, reply_markup=key)


@bot.message_handler(content_types=['location'])
def getLocation(message):
    Fails = []
    if message.location is not None:
        bot.send_message(message.chat.id, S.COUNTING_DISTANCE)
        km = countDistance((message.location.latitude, message.location.longitude))
        distance = km
        string = "Ближайший заболевший находится в %d километров от Вас" % distance
        bot.send_message(message.chat.id, string)
        question = S.NEED_MORE_INFO
        bot.send_message(message.chat.id, question, reply_markup=keyboard2)


bot.polling()
