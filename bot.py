import vk
import re
import random
import requests
import time
import pickle
import wikipedia
import pymorphy2
import lxml.html as html
def auth_vk(id, login, passwd, scope):
    session = vk.AuthSession(app_id=id, user_login=login, user_password=passwd, scope=scope)
    return vk.API(session, v='5.50')

def send_mesg(who, text):
    attach=re.findall('{\w*\S*\w*}', text)
    if(len(attach) != 0):
        bot.messages.send(peer_id=who, message=re.sub('{\w*\S*\w*}', "", text), random_id=random.randint(0, 200000), attachment=attach[0][1:-1])
    else:
        bot.messages.send(peer_id=who, message=text, random_id=random.randint(0, 200000))
def forward_mesg(who, id):
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), forward_messages=str(id)+",")
def init_simple_command():
    file = open('simple_command.db', 'rb')
    simple_command = pickle.load(file)
    file.close()
    return simple_command
def init_collection():
    file = open('collection.db', 'rb')
    collection = pickle.load(file)
    file.close()
    return collection

def send_list(who):
    send_mesg(who, "Список команд:" + "\n" +"\n".join(simple_command.keys()))

def send_collection(who):
    send_mesg(who, "Список мемасиков с Дружко:" + "\n" +"\n".join(collection.keys()))


def send_wiki_info(who, text):
    answ=" ".join(text)
    if(answ[-1] == "?"): answ = answ[:-1]
    wikipedia.set_lang("ru")
    try:
        resp=wikipedia.summary(answ, sentences=6, chars=1, auto_suggest=False, redirect=True)
    except wikipedia.exceptions.DisambiguationError as error:
        resp=wikipedia.summary(error.options[0], sentences=6, chars=1, auto_suggest=False, redirect=True)
    except  wikipedia.exceptions.WikipediaException:
        resp=wikipedia.summary(answ, sentences=6, chars=0, auto_suggest=True, redirect=True)
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000),message=resp)

def make_choose(who, list):
    choose_list = []
    string_list=re.search(r'\[.+\]', list).group(0)
    string_list=string_list[1:-1]
    list = string_list.split(',')
    for obj in list:
        obj = obj.strip()
        choose_list.append(obj)
    choise = random.choice(choose_list)
    message = choise +", "+random.choice(['определенно', 'возможно', 'наверное', 'скорее всего', 'инфа сотка', 'зуб даю', 'поверь'])
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)

def add_simple_command(mesg):
   if(len(mesg) >= 3):
       simple_command[mesg[1]] = " ".join(mesg[2:])
       file = open('simple_command.db', 'wb')
       pickle.dump(simple_command, file)
       file.close()

def add_collection_mesg(mesg):
   if(len(mesg) == 3):
       collection[mesg[1]] = mesg[2]
       file = open('collection.db', 'wb')
       pickle.dump(collection, file)
       file.close()

def send_fuck(who, person, flag_self=0):
    if (person[2] != 'меня'):
        m = pymorphy2.MorphAnalyzer()
        name = m.parse(person[2])[0].normal_form
        name = name[0].upper() + name[1:]
        message = name + ", катись " + " ".join(person[3:])
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)
    elif (flag_self == 0):
        pers = bot.users.get(user_id = who)
        message = pers[0]['first_name'] + ", катись " + " ".join(person[3:])
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)
    else:
        pers = bot.users.get(user_id=flag_self['from'])
        message = pers[0]['first_name'] + ", катись " + " ".join(person[3:])
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)

def send_praise(who, person, flag_self=0):
    if (person[2] != 'меня'):
        m = pymorphy2.MorphAnalyzer()
        name = m.parse(person[2])[0].normal_form
        name = name[0].upper() + name[1:]
        message = name + ", ты " + random.choice(['молодец', 'умница', 'зайка', 'ваще огонь']) +'!'
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)
    elif (flag_self == 0):
        pers = bot.users.get(user_id = who)
        name = pers[0]['first_name']
        name = name[0].upper() + name[1:]
        message = name + ", ты " + random.choice(['молодец', 'умница', 'зайка', 'ваще огонь']) +'!'
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)
    else:
        pers = bot.users.get(user_id=flag_self['from'])
        name = pers[0]['first_name']
        name = name[0].upper() + name[1:]
        message = name + ", ты " + random.choice(['молодец', 'умница', 'зайка', 'ваще огонь']) +'!'
        bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=message)

def get_poem(who):
    poem = requests.request("GET","http://rzhunemogu.ru/RandJSON.aspx?CType=3", timeout=50)
    poem=poem.json()
    poem=poem['content']
    bot.messages.send(peer_id=who, random_id=random.randint(0, 200000), message=poem)

def send_private_mesg(from_who, who, mesg):
    id = 0
    m = pymorphy2.MorphAnalyzer()
    name = m.parse(who)[0].normal_form
    name = name[0].upper() + name[1:]

    if name not in users:
        bot.messages.send(peer_id=from_who, random_id=random.randint(0, 200000), message="Имя не найдено")
    else:
        id = users[name]
        bot.messages.send(peer_id=id, random_id=random.randint(0, 200000), message=mesg)
        bot.messages.send(peer_id=from_who, random_id=random.randint(0, 200000), message="Отправлено")

def main():
    global bot
    global users
    global simple_command
    global collection
    bot = auth_vk('5419077', "89851906212", "228dicks228", 'wall,messages,photos,audio')
    simple_command = {}
    simple_command = init_simple_command()
    collection = {}
    collection = init_collection()
    users ={"Паша": 222870201, "Артем": 26140945,
            "Кирилл": 274280666, "Саше": 36729611,
            "Ксюша": 100669972, "Лиза": 89286618,
            "Наст": 17513023, "Антон": 23398752,
            "Ян": 3582228, "Саша":36729611,
            "Настя": 17513023, "Яна": 3582228}
    error_message = "Упс! Что то пошло не так... Попробуйте повторить запрос. Если эта ошибка происходит постоянно, пожалуйста, свяжитесь с vk.com/id96494615 для устранения проблеммы"
    print("Ready!")
    while (True):
        try:
            poll = bot.messages.getLongPollServer()
            r = requests.request("GET","http://"+poll['server']+"?act=a_check&key="+poll['key']+"&ts="+str(poll['ts'])+"&wait=25&mode=2", timeout=50)
            mesg_poll=r.json()
        except Exception:
            print("Error")
            time.sleep(4)
            poll = bot.messages.getLongPollServer()
            continue
        for mesg in mesg_poll['updates']:
            if (mesg[0] != 4):
                continue

            if (mesg[6].split(" ")[0] == "/список"):
                try:
                    send_list(mesg[3])
                    continue
                except Exception:
                   print("Ошибка при отправке списка")
                   bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                   continue

            if (mesg[6] in simple_command):
                try:
                    send_mesg(mesg[3], simple_command[mesg[6]])
                    continue
                except Exception:
                    print("Ошибка при отправке команды")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue

            if (mesg[6].split(" ")[0] == "/добавить"):
                try:
                    add_simple_command(mesg[6].split(" "))
                    continue
                except Exception:
                    print("Ошибка при добавлении команды")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[:3] == ["Антошка,", "что", "такое"]):
              try:
                    send_wiki_info(mesg[3], mesg[6].split(" ")[3:])
                    continue
              except Exception:
                    print("Ошибка при запросе в вики")
                    bot.messages.send(peer_id=mesg[3], message="Что то тут не то... В википедии нет такой страницы, или произошла другая ошибка! Попробуйте еще раз!", random_id=random.randint(0, 200000))
                    continue

            if (mesg[6].split(" ")[:3] == ["Антошка,", "выбери", "из"]):
              try:
                    make_choose(mesg[3], mesg[6])
                    continue
              except Exception:
                    print("Ошибка при выборе из списка")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[:2] == ["Антошка,", "пошли"]):
              try:
                    if (len(mesg[7]) == 0):
                        send_fuck(mesg[3], mesg[6].split(" "))
                    else: send_fuck(mesg[3], mesg[6].split(" "), mesg[7])
                    continue
              except Exception:
                    print("Ошибка при посылании нахер")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[:2] == ["Антошка,", "похвали"]):
              try:
                    if (len(mesg[7]) == 0):
                        send_praise(mesg[3], mesg[6].split(" "))
                    else: send_praise(mesg[3], mesg[6].split(" "), mesg[7])
                    continue
              except Exception:
                    print("Ошибка при похвальбе")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[:3] == ["Антошка,", "расскажи", "стишок"]):
              try:
                    get_poem(mesg[3])
                    continue
              except Exception:
                    print("Ошибка при похвальбе")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6].split(" ")[0] == "/добавить_кол"):
                try:
                    add_collection_mesg(mesg[6].split(" "))
                    continue
                except Exception:
                    print("Ошибка при добавлении команды")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue
            if (mesg[6] in collection):
                try:
                    forward_mesg(mesg[3], collection[mesg[6]])
                    continue
                except Exception:
                    print("Ошибка при отправке видосика")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue

            if (mesg[6].split(" ")[0] == "/коллекция"):
                try:
                    send_collection(mesg[3])
                    continue
                except Exception:
                   print("Ошибка при отправке списка видосиков")
                   bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                   continue
            if (mesg[6].split(" ")[0] == "/отправить"):
                try:
                    send_private_mesg(mesg[3], mesg[6].split(" ")[1], " ".join(mesg[6].split(" ")[2:]))
                    continue
                except Exception:
                    print("Ошибка при отправке приватного сообщения")
                    bot.messages.send(peer_id=mesg[3], message=error_message, random_id=random.randint(0, 200000))
                    continue

if __name__ == '__main__':
    main()
