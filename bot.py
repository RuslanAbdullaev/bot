from re import sub, match
import os
from time import asctime
import telebot
from telebot import types
from config import *
from pars import parsing

bot = telebot.TeleBot(token)


def keyboard(data, mes, message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(*data)
    bot.send_message(message.chat.id, mes, reply_markup=key)


def buttom(data):
    for i in range(len(data)):
        data[i] = types.KeyboardButton(data[i])
    return data


def grr():
    file = open(patt_to_groop, 'r')
    data = file.readlines()
    file.close()
    for i in range(len(data)):
        data[i] = sub('\n', '', data[i])
        data[i] = types.KeyboardButton(data[i])
    return data


def regul(share, mes):
    file = []
    for i in range(len(share)):
        if bool(match(mes, share[i])):
            share[i] = sub('_', ' ', share[i])
            share[i] = sub('.txt', '', share[i])
            file.append(share[i])
    return file


def are_you_admin_or_no(admin_id):
    file = open(path_to_admin_id, 'r')
    ids = file.readlines()
    file.close()
    ids = [sub('\n', '', ids[i]) for i in range(len(ids))]
    for i in ids:
        if i == str(admin_id):
            return True
    return False


def admin(message):
    txt = message.text
    try:
        if not txt.split(' ')[1] == '08021989':
            bot.send_message(message.chat.id, 'неверный пароль')
        elif txt.split(' ')[1] == '08021989' and txt.split(' ')[0] == 'Password':
            file = open(path_to_admin_id, 'a')
            file.write(str(message.chat.id) + '\n')
            file.close()
            bot.send_message(message.chat.id, 'регестрация пройдена, теперь вы администратор')
    except:
        bot.send_message(message.chat.id, 'ошибка')


def cabinet(message):
    sh = os.listdir(path_to_rasp)
    shares = []
    for i in sh:
        name = sub('.txt', '', i)
        name = sub('^....', '', name)
        if name not in shares:
            shares.append(name)
    for n in range(len(shares)):
        shares[n] = types.KeyboardButton("Кабинет " + message.text + ' на ' + shares[n])
    if len(shares) == 0:
        keyboard([types.KeyboardButton('назад')], 'извините, расписание не загруженно на сервер', message)
        return None
    keyboard(shares, 'выберите день', message)


def send_groop(message):
    tex = message.text.split(' ')
    dat = tex[3]
    cab = tex[1]
    retr = [str(i) + '. ----' for i in range(1, 7)]
    share = os.listdir(path_to_rasp)
    for name in share:
        if dat not in name:
            continue
        file = open(path_to_rasp + name, 'r')
        data = file.readlines()
        file.close()
        for i in range(len(data)):
            if cab in data[i]:
                retr[i - 1] = sub('----', sub((((len(name) - 3)) * '.') + '$', '', name), retr[i - 1])
    keyboard(grr(), '\n'.join(retr), message)


def clean_server(auth, userid, mes):
    if not auth:
        bot.send_message(userid, 'доступ запрещен')
        return None
    mes = mes.split(' ')
    if not len(mes) == 3:
        bot.send_message(userid, 'ошибка')
        return None
    if mes[2] == 'admin':
        file = open(path_to_admin_id, 'w')
        file.close()
    elif mes[2] == 'log':
        file = open(path_to_log, 'w')
        file.close()
    elif mes[2] == 'data':
        opt = [os.remove(path_to_rasp + name) for name in os.listdir(path_to_rasp)],
        opt = [os.remove(path_to_parsing + names) for names in os.listdir(path_to_parsing)]
    bot.send_message(userid, 'сервер очищен в данной конфигурации')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    keyboard(grr(), 'выбери группу, либо напиши номер кабинета', message)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not are_you_admin_or_no(message.chat.id):
        bot.send_message(message.chat.id, 'у вас нет прав на отправку файлов на сервер')
        return None
    file_info = bot.get_file(message.document.file_id)
    path = file_info.file_path.split('/')
    dats = [date(i) + '.xlsx' for i in range(7)]
    sos = True
    for n in dats:
        if n == message.document.file_name:
            sos = False
    if sos:
        bot.send_message(message.chat.id, 'неверное название файла либо неверный тип файла')
        return None
    try:
        downloaded_file = bot.download_file(file_info.file_path)
        file = open(path_to_parsing + message.document.file_name, 'wb')
        file.write(downloaded_file)
        file.close()
    except Exception as e:
        bot.send_message(message.chat.id, 'ошибка (' + str(e) + '), попробуйте позже')
        return None
    otvet = parsing(message.document.file_name)
    if otvet[0]:
        bot.send_message(message.chat.id, 'ошибка в структуре файла')
        return None
    if not len(otvet[1]) == 0:
        mes_user = ', если они находятся в загруженном файле то проверте структуру файла и загрузите файл повторно'
        bot.send_message(message.chat.id, 'отсутствуют группы ' + ', '.join(otvet[1]) + mes_user)
        return None
    bot.send_message(message.chat.id, 'загрузка прошла успешно')


@bot.message_handler(content_types=['text'])
def user(message):
    tex = message.text
    tex2 = tex.split(' ')
    if len(tex) < 3:
        keyboard(grr(), 'error', message)
    elif bool(match('clean server', tex)):
        clean_server(are_you_admin_or_no(message.chat.id), message.chat.id, tex)
    elif "Password" in tex:
        admin(message)
    elif (message.text[1] == '.' or message.text[1] == ',') and (len(message.text) == 3 or len(message.text) == 4):
        cabinet(message)
    elif len(tex2) == 4 and tex2[0] == 'Кабинет' and tex2[2] == 'на' and len(tex2[3]) == 10:
        send_groop(message)
    elif len(tex) == 3:
        mes = os.listdir(path_to_rasp)
        if len(mes) > 0:
            mes = regul(mes, message.text)
            mes = buttom(mes)
            keyboard(mes, 'выбери день', message)
        else:
            mes = buttom(['назад'])
            keyboard(mes, 'расписание не готово', message)
    else:
        if message.text == 'назад':
            keyboard(grr(), 'выбери группу', message)
        else:
            try:
                f = open(path_to_rasp + sub(' ', '_', message.text) + '.txt', 'r')
                rasp = f.read()
                f.close()
                keyboard(grr(), rasp, message)
            except:
                keyboard(grr(), 'ошибка', message)


while True:
    try:
        bot.polling()
    except Exception as error:
        print('error: ', str(error), ' time=', asctime())
        file = open(path_to_log, 'a')
        file.write(str(asctime()) + str(error) + '\n')
        file.close()
