import json
import requests
import telebot

TOKEN = '6651900304:AAFIYiVJQK_BJ7lfHTpVQM8JmhwHjahtzqI'

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'рубль': 'RUB',
    'доллар': 'USD',
    'бат': 'THB',
    'евро': 'EUR'
}

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote_lower = quote.lower()
        base_lower = base.lower()

        if quote_lower == base_lower:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote_lower]
        except KeyError:
            try:
                quote_ticker = keys[quote_lower.capitalize()] # пробуем с заглавной буквой
            except KeyError:
                raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base_lower]
        except KeyError:
            try:
                base_ticker = keys[base_lower.capitalize()] # пробуем с заглавной буквой
            except:
                raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base_lower]]

        return total_base * amount


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следущем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводной валюты>\nУвидить список всех доступных валют:/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)


    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
