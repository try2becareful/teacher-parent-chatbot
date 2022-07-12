import telebot
from telebot import types


import markup as nav
import config
from data import Database


bot = telebot.TeleBot(config.TOKEN)
db = Database('database_teacher.db')
profile_info = {}
info = []
profile_info['chat'] = 0
profile_info['ruk'] = 0


def tel(tg):
    tg = '@' + tg.lower()
    return 'telegram: ' + tg


def name(nm):
    n = nm.split()
    sur = n[0]
    nn = n[1]
    o = n[2]
    sur = sur[0] + sur[1:len(sur)].lower()
    nn = nn[0] + nn[1:len(nn)].lower()
    o = o[0] + o[1:len(o)].lower()
    return 'ФИО родителя: ' + sur + ' ' + nn + ' ' + o


def number(ph):
    return 'Номер телефона: ' + ph


@bot.message_handler(commands=['start'])
def start(msg: types.Message):
    if not db.user_exists(msg.from_user.id):
        message = bot.send_message(msg.from_user.id, "Укажите, кто вы: Учитель или Родитель", reply_markup=nav.wayMenu)
        bot.register_next_step_handler(message, person)
    else:
        message = bot.send_message(msg.from_user.id, "Вы уже зарегестрированы", reply_markup=nav.findMenu)
        bot.register_next_step_handler(message, text)


def person(msg):
    message = bot.send_message(msg.chat.id, "ФИО")
    if msg.text == "Учитель":
        profile_info['table'] = 'teachers'
        bot.register_next_step_handler(message, class_ruk)
    else:
        profile_info['table'] = 'parents'
        bot.register_next_step_handler(message, fio_parent)


def class_ruk(msg):
    message = bot.send_message(msg.from_user.id, "Являетесь ли вы классным руководителем?", reply_markup=nav.ansMenu)
    profile_info['fio'] = msg.text.upper()
    bot.register_next_step_handler(message, classnaya)


def classnaya(msg):
    profile_info['buf'] = msg.text.upper()
    if profile_info['buf'] == "ДА":
        message = bot.send_message(msg.from_user.id, "Введите номер класса", reply_markup=nav.classsMenu)
        bot.register_next_step_handler(message, classnaya_l)
    else:
        profile_info['buf'] = "НЕТ"
        num_classes(msg)


def classnaya_l(msg):
    profile_info['ruk'] = msg.text.upper()
    message = bot.send_message(msg.from_user.id, "Введите букву класса", reply_markup=nav.letterMenu)
    bot.register_next_step_handler(message, chat)


def chat(msg):
    profile_info['ruk'] += msg.text.upper()
    message = bot.send_message(msg.from_user.id, "Отправьте ссылку-приглашение в классный чат")
    bot.register_next_step_handler(message, num_classes)


def num_classes(msg):
    if profile_info['buf'] == "НЕТ":
        message = bot.send_message(msg.chat.id, "Введите количество классов у которых ведете")
        #profile_info['fio'] = msg.text.upper()
        bot.register_next_step_handler(message, fio_teacher)
    else:
        profile_info['chat'] = msg.text
        message = bot.send_message(msg.chat.id, "Введите количество классов у которых ведете")
        bot.register_next_step_handler(message, fio_teacher)


def fio_parent(msg):
    message = bot.send_message(msg.chat.id, "Введите номер класса", reply_markup=nav.classsMenu)
    profile_info['fio'] = msg.text.upper()
    bot.register_next_step_handler(message, classs)
    # print(profile_info)


def fio_teacher(msg):
    profile_info['n'] = int(msg.text)
    message = bot.send_message(msg.chat.id, "Введите номер и букву класса")
    profile_info['n'] -= 1
    bot.register_next_step_handler(message, tmp_classs)


def tmp_classs(msg):
    print(profile_info)
    if 'classs' in profile_info.keys():
        profile_info['classs'] += ' ' + msg.text
    else:
        profile_info['classs'] = msg.text

    if profile_info['n'] != 0:
        message = bot.send_message(msg.chat.id, "Введите номер и букву класса")
        profile_info['n'] -= 1
        bot.register_next_step_handler(message, fill_classes)
    else:
        message = bot.send_message(msg.chat.id, "Введите количество предметов, которые преподаете")
        bot.register_next_step_handler(message, classs_sub)


def fill_classes(msg):
    print(profile_info)
    if 'classs' in profile_info.keys():
        profile_info['classs'] += ' ' + msg.text
    else:
        profile_info['classs'] = msg.text

    if profile_info['n'] != 0:
        message = bot.send_message(msg.chat.id, "Введите номер и букву класса")
        profile_info['n'] -= 1
        bot.register_next_step_handler(message, tmp_classs)
    else:
        message = bot.send_message(msg.chat.id, "Введите количество предметов, которые преподаете")
        bot.register_next_step_handler(message, classs_sub)


def classs(msg):
    message = bot.send_message(msg.chat.id, "Введите букву класса", reply_markup=nav.letterMenu)
    profile_info['classs'] = msg.text.upper()
    bot.register_next_step_handler(message, classs_l)
    print(profile_info)


def classs_l(msg):
    profile_info['classs'] = profile_info['classs'] + msg.text
    message = bot.send_message(msg.chat.id, "ФИО ребёнка")
    profile_info['child_name'] = msg.text.upper()
    bot.register_next_step_handler(message, child_name)


def classs_sub(msg):
    profile_info['n'] = int(msg.text)
    message = bot.send_message(msg.chat.id, "Введите предмет", reply_markup=nav.subjectMenu)
    profile_info['n'] -= 1
    bot.register_next_step_handler(message, buf_subject)


def buf_subject(msg):
    print(profile_info)
    if 'subject' in profile_info.keys():
        profile_info['subject'] += ' ' + msg.text
    else:
        profile_info['subject'] = msg.text

    if profile_info['n'] != 0:
        message = bot.send_message(msg.chat.id, "Введите предмет")
        profile_info['n'] -= 1
        bot.register_next_step_handler(message, buf_subject2)
    else:
        message = bot.send_message(msg.chat.id, "Подтвердите", reply_markup=nav.checkMenu)
        bot.register_next_step_handler(message, subject)


def buf_subject2(msg):
    print(profile_info)
    if 'subject' in profile_info.keys():
        profile_info['subject'] += ' ' + msg.text
    else:
        profile_info['subject'] = msg.text

    if profile_info['n'] != 0:
        message = bot.send_message(msg.chat.id, "Введите предмет")
        profile_info['n'] -= 1
        bot.register_next_step_handler(message, buf_subject)
    else:
        message = bot.send_message(msg.chat.id, "Подтвердите", reply_markup=nav.checkMenu)
        bot.register_next_step_handler(message, subject)


def subject(msg):
    message = bot.send_message(msg.chat.id, "Ваш ник в телеграме (без @)")
    profile_info['subject'] = profile_info['subject'].upper()
    bot.register_next_step_handler(message, tg)


def child_name(msg):
    message = bot.send_message(msg.chat.id, "Ваш ник в телеграме (без @)")
    profile_info['child_name'] = msg.text.upper()
    bot.register_next_step_handler(message, tg)


def tg(msg):
    message = bot.send_message(msg.chat.id, "Телефон")
    profile_info['telegram'] = msg.text.upper()
    bot.register_next_step_handler(message, phone)


def phone(msg):
    profile_info['phone'] = msg.text.upper()
    message = bot.send_message(msg.chat.id, "Регестрация прошла успешно", reply_markup=nav.findMenu)
    if 'n' in profile_info.keys():
        del profile_info['n']
    if 'buf' in profile_info.keys():
        del profile_info['buf']
    print(profile_info)
    db.Set(msg.from_user.id, profile_info)
    profile_info.clear()
    try:
        bot.register_next_step_handler(message, text)
    except SyntaxError:
        bot.send_message(msg.chat.id, "Информация введена некорректно")


@bot.message_handler(commands=['help'])
def help(msg):
    bot.send_message(msg.chat.id, "/start - регестрация")
    bot.send_message(msg.chat.id, "Для поиска нажмите кнопку `Поиск`", reply_markup=nav.findMenu)


def find_classs(msg):
    if db.get_user(msg.from_user.id):
        message = bot.send_message(msg.chat.id, "Введите номер класса", reply_markup=nav.classsMenu)
    else:
        message = bot.send_message(msg.chat.id, "Введите номер класса", reply_markup=nav.classsMenu)
    try:
        bot.register_next_step_handler(message, find_classs_l)
    except SyntaxError:
        return


def find_classs_l(msg):
    info.append(msg.text)
    if db.get_user(msg.from_user.id):
        message = bot.send_message(msg.chat.id, "Введите букву класса", reply_markup=nav.letterMenu)
    else:
        message = bot.send_message(msg.chat.id, "Введите букву класса", reply_markup=nav.letterMenu)
    try:
        bot.register_next_step_handler(message, find_name)
    except SyntaxError:
        return


def find_name(msg):
    info.append(msg.text)
    if db.get_user(msg.from_user.id):
        message = bot.send_message(msg.chat.id, "Ввидите ФИО ученика", reply_markup=nav.findMenu)
    else:
        message = bot.send_message(msg.chat.id, "Введите предмет", reply_markup=nav.subjectMenu)
    try:
        bot.register_next_step_handler(message, find)
    except SyntaxError:
        return


def find(msg):
    info.append(msg.text)
    if len(info) != 3:
        return
    info[0] = info[0] + info[1]
    info[1] = info[2]
    if db.get_user(msg.from_user.id):
        initials, telegram, phone_number = db.find_puples(info[0].upper(), info[1].upper())
    else:
        initials, telegram, phone_number = db.find_teacher(info[0].upper(), info[1].upper())
    if initials is None:
        message = bot.send_message(msg.chat.id, "Такого пользователя не существует", reply_markup=nav.findMenu)
    else:
        textt = name(initials) + '\n' + tel(telegram) + '\n' + number(phone_number)
        message = bot.send_message(msg.chat.id, textt, reply_markup=nav.findMenu)
    info.clear()
    try:
        bot.register_next_step_handler(message, text)
    except SyntaxError:
        return


def class_chat(msg):
    ch = db.get_chat(db.get_class(msg.from_user.id))
    if ch is None:
        bot.send_message(msg.from_user.id, "Чата класса не существует", reply_markup=nav.findMenu)
    else:
        bot.send_message(msg.from_user.id, ch)


@bot.message_handler(content_types=['text'])
def text(msg):
    if msg.text == "Поиск":
        if db.user_exists(msg.from_user.id):
            find_classs(msg)
        else:
            bot.send_message(msg.chat.id, "Вы не зарегестрированы! Испульзуйте команду /start для регестрации")
    elif msg.text == "Помощь":
        help(msg)
    elif msg.text == "Чат класса":
        class_chat(msg)
    else:
        message = bot.send_message(msg.chat.id, "Непонятный ввод, нажмите кнопку `Помощь`", reply_markup=nav.findMenu)
        bot.register_next_step_handler(message, text)


bot.polling(none_stop=True)
