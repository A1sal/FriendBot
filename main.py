import telebot
import wikipedia, re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup
import logging
import requests
import config
from telegram.ext import *
from telebot import types

# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

wikipedia.set_lang("ru")
bot = telebot.TeleBot(config.TOKEN)


def clean_str(r):
    r = r.lower()
    r = [c for c in r if c in alphabet]
    return ''.join(r)


alphabet = ' 1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm?%.,()!:;'


def update():
    with open('dialogues.txt', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('\n')
    dataset = []

    for block in blocks:
        replicas = block.split('\\')[:2]
        if len(replicas) == 2:
            pair = [clean_str(replicas[0]), clean_str(replicas[1])]
            if pair[0] and pair[1]:
                dataset.append(pair)

    X_text = []
    y = []

    for question, answer in dataset[:10000]:
        X_text.append(question)
        y += [answer]

    global vectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)

    global clf
    clf = LogisticRegression()
    clf.fit(X, y)


update()


def get_generative_replica(text):
    text_vector = vectorizer.transform([text]).toarray()[0]
    question = clf.predict([text_vector])[0]
    return question


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'Не смог найти информации😅'


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton("Что ты обо мне думаешь?")
    button_2 = types.KeyboardButton("Скучно 🙄")
    markup.add(button_1, button_2)
    bot.send_message(message.chat.id, 'Привет, друг!', reply_markup=markup)


question = ""




@bot.message_handler(content_types=['text'])
def message_reply(message):
    command = message.text.lower()
    if message.text == "Что ты обо мне думаешь?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Еще хочу")
        button_2 = types.KeyboardButton("Хочу вернуться к началу 😋")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'С тобой интересно вести беседу', reply_markup=markup)
    elif message.text == "Еще хочу":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Еще один разок")
        button_2 = types.KeyboardButton("Хочу вернуться к началу 😋")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'У тебя отличное чувство юмора', reply_markup=markup)
    elif message.text == "Еще один разок":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("И последний")
        button_2 = types.KeyboardButton("Хочу вернуться к началу 😋")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'У тебя все получится!', reply_markup=markup)
    elif message.text == "И последний":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1)
        bot.send_message(message.chat.id, 'Я в тебе не сомневаюсь!', reply_markup=markup)
    elif message.text == "Возвращаюсь к началу 😋" or message.text == "Хочу вернуться к началу 😋":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Что ты обо мне думаешь?")
        button_2 = types.KeyboardButton("Скучно 🙄")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'Ты снова в начале!', reply_markup=markup)
    elif message.text == "Скучно 🙄":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Скажи мне приятное")
        button_2 = types.KeyboardButton("Кинь фоточку 🤩")
        button_3 = types.KeyboardButton("Скинь мне песенку 😋")
        markup.add(button_1, button_2, button_3)
        bot.send_message(message.chat.id, 'Как мне тебя развеселить? ', reply_markup=markup)
    elif message.text == "Кинь фоточку 🤩":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Котята")
        button_2 = types.KeyboardButton("Море")
        button_3 = types.KeyboardButton("Закат")
        button_4 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1, button_2, button_3, button_4)
        bot.send_message(message.chat.id, 'Какую хочешь?', reply_markup=markup)
    elif message.text == "Котята":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1)
        bot.send_message(message.chat.id, 'Лови фоточку 😇', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.Kittens, 'rb'), reply_markup=markup)
    elif message.text == "Море":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1)
        bot.send_message(message.chat.id, 'Лови фоточку 😇', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.More, 'rb'), reply_markup=markup)
    elif message.text == "Закат":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1)
        bot.send_message(message.chat.id, 'Лови фоточку 😇', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.Zakat, 'rb'), reply_markup=markup)
    elif message.text == "Скинь мне песенку 😋":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        button_2 = types.KeyboardButton("Другую")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'Лови песню 😇', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.Music, 'rb'), reply_markup=markup)
        bot.send_audio(message.chat.id, audio=open(config.Markul, 'rb'), reply_markup=markup)
    elif message.text == "Другую":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        button_2 = types.KeyboardButton("Еще одну")
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id, 'Лови другую песню 😇', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.Music_1, 'rb'), reply_markup=markup)
        bot.send_audio(message.chat.id, audio=open(config.Endsh, 'rb'), reply_markup=markup)
    elif message.text == "Еще одну":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Возвращаюсь к началу 😋")
        markup.add(button_1)
        bot.send_message(message.chat.id, 'Вот еще одна', reply_markup=markup)
        bot.send_photo(message.chat.id, photo=open(config.Music_2, 'rb'), reply_markup=markup)
        bot.send_audio(message.chat.id, audio=open(config.Other, 'rb'), reply_markup=markup)
    elif message.text == "Хотел другого ответа🥲":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton("Ответ из Википедии😌")
        markup.add(button_1)
        bot.send_message(message.chat.id, "Расскажи, пожалуйста, какого?😯", reply_markup=markup)
        bot.register_next_step_handler(message, wrong)
        button_1 = types.KeyboardButton("Хочу вернуться к началу 😋")
        markup.add(button_1)

    else:
        global question
        question = command
        reply = get_generative_replica(command)
        if reply == "ответ из википедии ":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_2 = types.KeyboardButton("Хотел другого ответа🥲")
            button_1 = types.KeyboardButton("Хочу вернуться к началу 😋")
            markup.add(button_1, button_2)
            bot.send_message(message.from_user.id, getwiki(command), reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_2 = types.KeyboardButton("Хотел другого ответа🥲")
            button_1 = types.KeyboardButton("Хочу вернуться к началу 😋")
            markup.add(button_1, button_2)
            bot.send_message(message.from_user.id, reply, reply_markup=markup)


def wrong(message):
    a = f"{question}\{message.text.lower()} \n"
    with open('dialogues.txt', "a", encoding='utf-8') as f:
        f.write(a)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton("Хочу вернуться к началу 😋")
    markup.add(button_1)
    bot.send_message(message.from_user.id, "Исправил!😁", reply_markup=markup)
    update()


bot.polling(none_stop=True)


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} cause error {context.error}')


if __name__ == '__main__':
    bot.infinity_polling()
