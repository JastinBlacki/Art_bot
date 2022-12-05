import telebot
import sqlite3
from sqlite3 import Error

from telebot.types import InlineKeyboardButton

bot = telebot.TeleBot('5709988932:AAFJFqPWnQuj5VJD-qavOcpIgjGQU2eKfgA')

#TODO: реализовать отлов ошибок

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я Александр Николаевич, и я обожаю искусство!")
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn3 = telebot.types.InlineKeyboardButton('Музыка', callback_data='muuusic_all')
    btn4 = telebot.types.InlineKeyboardButton('Живопись', callback_data="piiiicture_all")
    btn5 = telebot.types.InlineKeyboardButton('Поэзия', callback_data='poooem_all')
    btn6 = telebot.types.InlineKeyboardButton('Легенды', callback_data='leegend_all')
    btn7 = telebot.types.InlineKeyboardButton('Темы', callback_data='theme')
    markup.add(btn3, btn4, btn5, btn6, btn7)
    bot.send_message(m.chat.id,
                     "Живопись, литература, легенды и мифы - все эти творения человеческого гения поистине поражают меня. "
                     "Я знаю много интересного, и с радостью поделюсь своими знаниями с тобой! Если ты хочешь окунуться в удивительный мир творчества и искусства, то приготовься - мы отправляемся с тобой в страну Ars Semper!")
    bot.send_message(m.chat.id,
                     "Итак, мы на месте. Сейчас ты можешь выбрать тему, которая наиболее тебе интересна. Если ты хочешь найти какой-либо определенный шедевр искусства, то воспользуйся функцией поиск. Ты всегда сможешь вернуться назад и изменить свой выбор! Для взаимодействия с чат-ботом пользуйся кнопками снизу ⬇️. Желаю тебе удачи на твоем творческом пути! Вперед!",
                     reply_markup=markup)


@bot.message_handler(commands=['command'])
def _command_(message):
    bot.send_message(message.chat.id, "Напиши свои впечатления ниже :)")

    return message


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    def create_connection(path="list_of_all.db"):
        connection = None
        try:
            connection = sqlite3.connect(path)
            if_connect = 1
        except Error as e:
            if_connect = 0
        return connection, if_connect

    def excute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print("Подключение прервано")

    if call.data == "home":
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn3 = telebot.types.InlineKeyboardButton('Музыка', callback_data='muuusic_all')
        btn4 = telebot.types.InlineKeyboardButton('Живопись', callback_data='piiiicture_all')
        btn5 = telebot.types.InlineKeyboardButton('Поэзия', callback_data='poooem_all')
        btn6 = telebot.types.InlineKeyboardButton('Легенды', callback_data='leegend_all')
        btn7 = telebot.types.InlineKeyboardButton('Темы', callback_data='theme')
        markup.add(btn3, btn4, btn5, btn6, btn7)
        bot.send_message(call.message.chat.id,
                         "Выбери тему, которая тебе интересна :)", reply_markup=markup)

    elif call.data == "muuusic_all":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        for i in bd:
            btn1 = telebot.types.InlineKeyboardButton(i[5], callback_data="music_" + str(i[0]))
            markup.add(btn1)
        bot.send_message(call.message.chat.id,
                         text="Выбери интересующее тебя произведение".format(
                             call.from_user), reply_markup=markup)

    elif call.data[:6] == "music_":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information;"""
        bd = excute_query(bd_connect, query1)
        id_ = call.data[6:]
        for i in bd:
            if id_ == str(i[0]):
                musician = i[4]
                music_name = i[5]
                music_text_path = i[7]
                music_path = i[6]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1_1 = telebot.types.InlineKeyboardButton("Все муз.произведения",
                                                  callback_data="muuusic_all")
        btn1_2 = telebot.types.InlineKeyboardButton("Картина по этой же теме",
                                                    callback_data="pict" + id_)
        btn1_3 = telebot.types.InlineKeyboardButton("Поэзия по этой же теме",
                                                    callback_data="poem" + id_)
        btn1_4 = telebot.types.InlineKeyboardButton("Легенда по этой же теме",
                                                    callback_data="leg" + id_)
        btn3 = telebot.types.InlineKeyboardButton("Картина + муз.произведение",
                                                  callback_data="tog" + id_)
        btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup2 = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn4 = telebot.types.InlineKeyboardButton("Читать дальше",
                                                  callback_data="nxt1" + id_)
        markup2.add(btn4)
        markup.add(btn1_1, btn1_2, btn1_3, btn1_4, btn2, btn3)
        bot.send_message(call.message.chat.id,
                         text=musician + " '" + music_name + "'".format(
                             call.from_user))
        bot.send_audio(call.message.chat.id, audio=open(music_path, 'rb'), title=music_name, performer=musician)
        text = open(music_text_path, 'r', encoding="utf-8").read()
        if len(text) > 1000:
            global count
            count = 1000
            while text[count] != ' ':
                count += 1
            text = text[:count]
            bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user), reply_markup=markup2)
        else:
            bot.send_message(call.message.chat.id,
                             text=text.format(
                                 call.from_user), reply_markup=markup)

    elif call.data[:4] == "nxt1":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        id_ = call.data[4:]
        for i in bd:
            if str(i[0]) == id_:
                music_text_path = i[7]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1 = telebot.types.InlineKeyboardButton("Другие муз.произведения",
                                                  callback_data="muuusic_all")
        btn1_2 = telebot.types.InlineKeyboardButton("Картина по этой же теме",
                                                    callback_data="pict" + id_)
        btn1_3 = telebot.types.InlineKeyboardButton("Поэзия по этой же теме",
                                                    callback_data="poem" + id_)
        btn1_4 = telebot.types.InlineKeyboardButton("Легенда по этой же теме",
                                                    callback_data="leg" + id_)
        btn4 = telebot.types.InlineKeyboardButton("Картина + муз.произведение",
                                                  callback_data="tog" + id_)
        btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup.add(btn1_4, btn1_3, btn1_2, btn1, btn4, btn2)
        text = open(music_text_path, 'r', encoding="utf-8").read()
        bot.send_message(call.message.chat.id,
                         text=text[count:].format(
                             call.from_user), reply_markup=markup)

    elif call.data[:4] == "pict":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        id_ = call.data[4:]
        for i in bd:
            if str(i[0]) == id_:
                artist = i[1]
                picture_path = i[2]
                picture_name = i[15]
                picture_text_path = i[3]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1_2 = telebot.types.InlineKeyboardButton("Музыка по этой же теме",
                                                    callback_data="music_" + id_)
        btn1_3 = telebot.types.InlineKeyboardButton("Поэзия по этой же теме",
                                                    callback_data="poem" + id_)
        btn1_4 = telebot.types.InlineKeyboardButton("Легенда по этой же теме",
                                                    callback_data="leg" + id_)
        btn3 = telebot.types.InlineKeyboardButton("Все картины",
                                                  callback_data="piiiicture_all")
        btn4 = telebot.types.InlineKeyboardButton("Картина + муз.произведение",
                                                  callback_data="tog" + id_)
        btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup.add(btn1_2, btn1_3, btn1_4, btn4, btn2, btn3)
        text = open(picture_text_path, 'r', encoding='utf-8').read()
        bot.send_photo(call.message.chat.id, open(picture_path, 'rb'), caption=artist + " '" + picture_name + "'")
        bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user), reply_markup=markup)

    elif call.data[:3] == "tog":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        id_ = call.data[3:]
        for i in bd:
            if str(i[0]) == id_:
                file_path = i[17]
                music_name = i[5]
                picture_name = i[15]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1 = telebot.types.InlineKeyboardButton("Все музыкальные произведения",
                                                  callback_data="muuusic_all")
        btn2 = telebot.types.InlineKeyboardButton("Все картины",
                                                  callback_data="piiiicture_all")
        btn1_2 = telebot.types.InlineKeyboardButton("Картина по этой же теме",
                                                    callback_data="pict" + id_)
        btn1_3 = telebot.types.InlineKeyboardButton("Поэзия по этой же теме",
                                                    callback_data="poem" + id_)
        btn1_4 = telebot.types.InlineKeyboardButton("Музыка по этой же теме",
                                                    callback_data="music_" + id_)
        btn1_5 = telebot.types.InlineKeyboardButton("Легенда по этой же теме",
                                                    callback_data="leg" + id_)
        btn3 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup.add(btn1, btn2, btn1_2, btn1_3, btn1_4, btn3, btn1_5)
        text = open(file_path, 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id,
                         text=music_name + " + " + picture_name.format(
                             call.from_user))
        bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user), reply_markup=markup)

    elif call.data[:3] == "leg":
        id_ = call.data[3:]
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        for i in bd:
            if str(i[0]) == id_:
                story_name = i[8]
                story_country = i[9]
                story_path = i[10]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1_4 = telebot.types.InlineKeyboardButton("Картина по этой же теме",
                                                    callback_data="pict" + id_)
        btn1_3 = telebot.types.InlineKeyboardButton("Поэзия по этой же теме",
                                                    callback_data="poem" + id_)
        btn1_2 = telebot.types.InlineKeyboardButton("Музыка по этой же теме",
                                                    callback_data="music_" + id_)
        btn1 = telebot.types.InlineKeyboardButton("Все легенды",
                                                  callback_data="leegend_all")
        btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup.add(btn1_2, btn1_3, btn1_4, btn2, btn1)
        text = open(story_path, 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id,
                         text=story_country + " '" + story_name + "'".format(
                             call.from_user))
        bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user), reply_markup=markup)

    elif call.data[:4] == "poem":
        id_ = call.data[4:]
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        for i in bd:
            if str(i[0]) == id_:
                writer = i[11]
                poem_name = i[12]
                poem_path = i[13]
                poem_text_path = i[14]
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn1_2 = telebot.types.InlineKeyboardButton("Музыка по этой же теме",
                                                    callback_data="music_" + id_)
        btn1_4 = telebot.types.InlineKeyboardButton("Легенда по этой же теме",
                                                    callback_data="leg" + id_)
        btn1 = telebot.types.InlineKeyboardButton("Картина по этой же теме",
                                                    callback_data="pict" + id_)
        btn3 = telebot.types.InlineKeyboardButton("Все стихи", callback_data="poooem_all")
        btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="home")
        markup.add(btn1, btn2, btn1_2, btn1_4, btn3)
        text = open(poem_path, 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id,
                         text=writer + " '" + poem_name + "'".format(
                             call.from_user))
        bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user))
        text = open(poem_text_path, 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id,
                         text=text.format(
                             call.from_user), reply_markup=markup)

    elif call.data == "piiiicture_all":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for i in bd:
            btn1 = telebot.types.InlineKeyboardButton(i[15], callback_data="pict" + str(i[0]))
            markup.add(btn1)
        bot.send_message(call.message.chat.id,
                         text="Выбери интересующую картину".format(
                             call.from_user), reply_markup=markup)

    elif call.data == "poooem_all":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for i in bd:
            btn1 = telebot.types.InlineKeyboardButton(i[12], callback_data="poem" + str(i[0]))
            markup.add(btn1)
        bot.send_message(call.message.chat.id,
                         text="Выбери интересующее тебя произведение".format(
                             call.from_user), reply_markup=markup)

    elif call.data == "leegend_all":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for i in bd:
            text = "leg" + str(i[0])
            btn1 = telebot.types.InlineKeyboardButton(i[8], callback_data=text)
            markup.add(btn1)
        bot.send_message(call.message.chat.id,
                         text="Выбери интересующее тебя произведение".format(
                             call.from_user), reply_markup=markup)

    elif call.data == "theme":
        bd_connect, if_conn = create_connection()
        query1 = """SELECT * FROM information"""
        bd = excute_query(bd_connect, query1)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for i in bd:
            text = "music_"+str(i[0])
            btn1 = telebot.types.InlineKeyboardButton(i[18], callback_data=text)
            markup.add(btn1)
        bot.send_message(call.message.chat.id,
                         text="Выбери интересующую тебя тему".format(
                             call.from_user), reply_markup=markup)

    else:
        bot.send_message(call.message.chat.id,
                         text="Подключение к базе данных было прервано. Вы можете написать свою жалобу администратору данного "
                              "бота в Telegram @Veronichka".format(
                             call.from_user))


bot.polling(non_stop=True)