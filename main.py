from urllib import request, response, parse
import json
import mocks
import config
import telebot

__doc__ = '''
Basic experiments with weather api, and telegram bot library.

API help and docs:

Telegram = https://www.gitbook.com/book/kondra007/telegram-bot-lessons/details
Weather = http://openweathermap.org/forecast5

Config.py contains apikeys, not included in project.
'''

weather_params = {
    'q': 'Kiev,ua',
    'mode': 'json',
    'appid': config.OPENWEATHER['appid']
}

encoded_params = parse.urlencode(weather_params)

with request.urlopen('http://api.openweathermap.org/data/2.5/forecast?' + encoded_params) as resp:
    data = resp.read().decode('utf-8')
    parsed_json = json.loads(data)
    print(parsed_json)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            bot.send_message(m.chat.id, m.text)

if __name__ == '__main__':
     bot = telebot.TeleBot(config.TELEGRAM['token'])
     bot.set_update_listener(listener)
     bot.polling(none_stop=True)