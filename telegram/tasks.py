import json
import datetime
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater,CommandHandler
from twitter import Twitter


Token = "API_KEY"
updater = Updater(token=Token)
job = updater.job_queue
dispatcher = updater.dispatcher


#Fonksiyon
def callback_alarm(bot, job):
    name = job.context[1] + " " + job.context[2]
    reply_markup = ReplyKeyboardMarkup([["/Yes "+ name, "/No "+ name, "/Never "+name]],
                                       one_time_keyboard=True)
    bot.send_message(chat_id=job.context[0].message.chat_id, text='?',
                     reply_markup=reply_markup)



def Yes(bot, update):
    send = Twitter()
    msg = update.message.text.replace("/Yes", " ").split(" ")
    msg = msg[2:]
    speaker = "".join(msg)
    url = "http://ictconf.net/api/event/?format=json"
    params = dict()
    resp = requests.get(url, params=params)
    json_response = json.loads(resp.text)
    num = 0
    for data in json_response:
        full_name = str(data["speaker"]["name"] + data["speaker"]["last_name"])
        if full_name.replace(" ", "") == speaker:
            num = 1
            print("yolladı")
            send.send_tweet("content")
            
    if num == 0:
        bot.send_message(chat_id=update.message.chat_id, text="Kullanıcı Yok")



def No(bot, update, job_queue):
    msg = update.message.text.replace("/No", " ").split(" ")
    job_queue.run_once(callback_alarm, 300, context=[update,
                                                    msg[1],
                                                     msg[2]])
    bot.send_message(chat_id=update.message.chat_id, text=msg[1]+ " "+ msg[2] +
                                                          " 5 dakika sonra tekrar sorulacak")



def callback_timer(bot, update, job_queue):
    url = "http://ictconf.net/api/event/?format=json"
    params = dict()
    resp = requests.get(url, params=params)
    json_response = json.loads(resp.text)
    for data in json_response:
        date = int((datetime.datetime.strptime(data["start_date"], '%Y-%m-%dT%H:%M:%SZ') - datetime.datetime.now()).seconds)
        try:
            job_queue.run_once(callback_alarm, date, context=[update,
                                                          data["speaker"]["name"],
                                                          data["speaker"]["last_name"]])
            bot.send_message(chat_id=update.message.chat_id,
                             text=data["speaker"]["name"] + " " + data["speaker"]["last_name"] +
                                  " ayarlandı.")

        except:
            bot.send_message(chat_id=update.message.chat_id, text=data["speaker"]["name"]+" "+data["speaker"]["last_name"]+
                                                                  " ayarlanamadı.")



# Handler

timer_handler = CommandHandler('Ayarla', callback_timer, pass_job_queue=True)
yes_handler = CommandHandler('Yes', Yes)
no_handler = CommandHandler('No', No, pass_job_queue=True)



# dispatcher

dispatcher.add_handler(timer_handler)
dispatcher.add_handler(yes_handler)
dispatcher.add_handler(no_handler)


updater.start_polling()
job.start()


