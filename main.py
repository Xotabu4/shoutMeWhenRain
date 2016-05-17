from urllib import request, response, parse
import json

import collections

import mocks
import config
import pyowm
import logging

import telebot
from telebot import types

__doc__ = '''
Basic experiments with weather api, and telegram bot library.

API help and docs:

Telegram = https://www.gitbook.com/book/kondra007/telegram-bot-lessons/details
WeatherAPI = http://openweathermap.org/forecast5
WeatherLIBRARY = https://github.com/csparpa/pyowm/wiki/Usage-examples

Config.py contains apikeys, not included in project.
'''

owm = pyowm.OWM(config.OPENWEATHER['appid'], language='ru')

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
BOT = telebot.TeleBot(config.TELEGRAM['token'])


@BOT.message_handler(commands=['start'])
def echo_msg(message):
    BOT.reply_to(message, 'Начинаем!')
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Сейчас')
    itembtn2 = types.KeyboardButton('Завтра')
    markup.add(itembtn1, itembtn2)
    BOT.send_message(chat_id=message.chat.id, text="На когда погоду?", reply_markup=markup)


@BOT.message_handler(regexp="Сейчас")
def now(message):
    # Hide keyboard, if visible
    markup = types.ReplyKeyboardHide(selective=False)
    BOT.send_message(chat_id=message.chat.id, text='Ломлюсь за данными...', reply_markup=markup)

    w = owm.weather_at_place('Kiev,ua').get_weather()
    logger.info('Получил - ', w.to_JSON())
    resp = collections.OrderedDict({
        "Как вообще?": w.get_status(),
        'Температура:': w.get_temperature(unit='celsius')['temp'],
        'Дождь?': 'Льет!' if w.get_rain() else 'Неа'
    })

    for key, value in resp.items():
        BOT.send_message(chat_id=message.chat.id, text='{0} {1}'.format(key, value))

@BOT.message_handler(regexp="Завтра")
def tomorrow(message):
    # Hide keyboard, if visible
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Сейчас')
    markup.add(itembtn1)
    BOT.send_message(chat_id=message.chat.id, text='Погоды нет. Еще не реализовано', reply_markup=markup)


if __name__ == '__main__':
    BOT.polling(none_stop=True)