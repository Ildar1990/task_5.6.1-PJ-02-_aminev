import telebot
from config import TOKEN, keys
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def instruction(message: telebot.types.Message):
    text = 'Этот бот создан для конвертации валют. Чтобы узнать курс валют, введите команду в следующем формате:\n\
<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>.\nНапример: доллар рубль 1.\nЧтобы узнать список доступных валют, введите команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')

        if len(parameters) != 3:
            raise APIException('вы ввели неправильное количество параметров.')

        base, quote, amount = parameters
        rate = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.reply_to(message, f'Возникла ошибка: {e}')
    else:
        text = round(rate, 3)
        bot.send_message(message.chat.id, text)


bot.polling()
