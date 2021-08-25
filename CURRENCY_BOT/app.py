import telebot
from extensions import CryptoConverter, APIException
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
    \n<в какую валюту перевести> \
    \n<колличество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) > 3:
            raise APIException('Слишком много параметров')
        elif len(val) < 3:
            raise APIException('Недостаточно параметров')
        quote, base, amount = val

        total_base_scaled = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        text = f'Цена {amount} {quote.capitalize()} в {base.capitalize()} - {total_base_scaled}'
        bot.send_message(message.chat.id, text)


bot.polling()
