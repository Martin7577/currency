import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Чтобы начать работу введите команду боту в следующем формате: 
<имя валюты> <в какую валюту перевсти> <количество переводимой валюты>
Увидеть список доступных валют можно командой: /values''')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, f'- {key}',))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
        t = float(total_base)
        a = float(amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = (f'Цена {amount} {quote} в {base} - {t * a}')
        bot.send_message(message.chat.id, text)

bot.polling()
