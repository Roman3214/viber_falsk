#Импорт всех необходимых библиотек
from flask import Flask, request, Response, session
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import (
    TextMessage,
    KeyboardMessage
)
from viberbot.api.viber_requests import ViberMessageRequest, ViberConversationStartedRequest
import sched
import threading
import time
import sqlite3

import os

import subprocess
import logging

import json
from config import BOT_TOKEN

def get_ngrok_address():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    global URL
    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)
        
    with open('tunnels.json', 'r') as file_json:
        respone_dict = file_json.read()

    begin = str(respone_dict).find('https:')
    enD = str(respone_dict).find('.io","proto"')
    URL = str(respone_dict)[begin : enD+3]
    
    return dict(zip(['http', 'https'], [i['public_url'] for i in datajson['tunnels']])) 


token = BOT_TOKEN

'''class UseDataBase:
#Менеджер контекста для подключения к базе данных
    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
'''
with open('viber.json', 'r') as file_json:
            URL = file_json.read()
class ViberSay():
#'''Чат-бот'''	
    def __init__(self, token):
    	#Инициализация чат-бота данными, полученными при регистрации на Admin Panel
        self.viber = Api(BotConfiguration(
            name='Test_Bot',
            avatar='http://viber.com/avatar.jpg',
            auth_token=token))
        self.app = Flask(__name__)	#Создание экземпляра приложения Flask
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(5, 1, self.set_webhook, ())
        self.t = threading.Thread(target=self.scheduler.run)
        self.t.start() #запуск потока
        self.app.secret_key = 'YouWillNeverGuess'
        #конфигурация базы данных
        self.app.config['dbconfig'] = {'host': '127.0.0.1',
                          				'user': 'ilya',
                          				'password': 'qwerty123',
                          				'database': 'siemens', }
        self.index = 0
        self.app.add_url_rule('/', 'home', self.poll, methods=['POST', 'GET'])
        self.app.run(host='0.0.0.0', port=8887, debug=True) #пуск приложения


    def set_webhook(self):
    	#установка вебхука
        
               
        self.viber.set_webhook(URL)#('https://5494-178-168-189-17.ngrok.io')

    def poll(self):
       # приём входящих сообщений, обработка и декодирование
        viber_request = self.viber.parse_request(request.get_data().decode('utf8'))  
        if isinstance(viber_request, ViberConversationStartedRequest):
            #Определяем начало диалога с ботом
            session['uid'] = viber_request.user.id

            self.viber.send_messages(session['uid'], [
                TextMessage(text='Добро пожаловать! Напиши команду: start. Затем выбери отделение в котором ты работаешь.')
            ])
            #отправляем кнопку с предложением получить данные
            self.send_buttons(uid=session['uid'])

        elif isinstance(viber_request, ViberMessageRequest):
        	#если не начало диалога, то ждём запроса данных
            session['uid'] = viber_request.sender.id
            if viber_request.message.text == 'start':
                

                
                self.send_buttons(uid=session['uid'])#, text=['start'], btns=3)

            if viber_request.message.text == 'Отделение пограничных состояний':
                name_user = viber_request.sender.name
                #user_surname = ViberConversationStartedRequest.user.name format l: /fs:fat32 /q
                user_id = viber_request.sender.id
                print(name_user, user_id)
                try:
                    conn = sqlite3.connect("users.db")
                    cursor = conn.cursor()
                #cursor.execute("SELECT `user_id` FROM `users_telegram` WHERE `user_id` = ?", (f'{int(user_id)}',))
                    
                    cursor.execute('INSERT OR IGNORE INTO "Pogr_sost_viber" ("user_id" , "user_name") VALUES (?,?)', (f'{str(user_id)}',  f'{str(name_user)}', ))
                    
                    conn.commit()

                
                except sqlite3.Error as error:
                    print('Error', error)
    
                finally:
                    if(conn):
                        conn.close()
                self.viber.send_messages(to=session['uid'], messages=[TextMessage(text="Ваша учетная запись добавлена. Уведомления получите в ближайшее время")])

            elif viber_request.message.text == 'Детское отделение':
                name_user = viber_request.sender.name
                #user_surname = ViberConversationStartedRequest.user.name format l: /fs:fat32 /q
                user_id = viber_request.sender.id
                print(name_user, user_id)
                try:
                    conn = sqlite3.connect("users.db")
                    cursor = conn.cursor()
                    cursor.execute('INSERT OR IGNORE INTO "childrens_department" ("user_id" , "user_name") VALUES (?,?)', (f'{str(user_id)}',  f'{str(name_user)}', ))
                    
                    conn.commit()

                
                except sqlite3.Error as error:
                    print('Error', error)
    
                finally:
                    if(conn):
                        conn.close() 
                self.viber.send_messages(to=session['uid'], messages=[TextMessage(text="Ваша учетная запись добавлена. Уведомления получите в ближайшее время")])
 
            else:
                viber_request.message.text == 'Отделение наркологии'
                name_user = viber_request.sender.name
                user_id = viber_request.sender.id
                print(name_user, user_id)
                try:
                    conn = sqlite3.connect("users.db")
                    cursor = conn.cursor()
                    cursor.execute('INSERT OR IGNORE INTO "narcology" ("user_id" , "user_name") VALUES (?,?)', (f'{str(user_id)}',  f'{str(name_user)}', ))
                    
                    conn.commit()

                
                except sqlite3.Error as error:
                    print('Error', error)
    
                finally:
                    if(conn):
                        conn.close()  
                self.viber.send_messages(to=session['uid'], messages=[TextMessage(text="Ваша учетная запись добавлена. Уведомления получите в ближайшее время")])

        return Response(status=200)

    def send_buttons(self, uid):
    	#метод формирует кнопку
        #if btns == 1:
        KEYBOARD = {"DefaultHeight": True,
            "BgColor": "#4169E1",
            "Type": "keyboard", "Buttons": [{
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": '#4169E1',
                    "BgMedia": None,
                "BgMediaType": None,
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "Отделение пограничных состояний",
                    "ReplyType": "message",
                    "Text": "Отделение пограничных состояний"
                    },
                {
                   "Columns": 6,
                    "Rows": 1,
                    "BgColor": '#4169E1',
                    "BgMedia": None,
                "BgMediaType": None,
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "Детское отделение",
                    "ReplyType": "message",
                    "Text": "Детское отделение" 
                },
                {
                   "Columns": 6,
                    "Rows": 1,
                    "BgColor": '#4169E1',
                    "BgMedia": None,
                "BgMediaType": None,
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "Отделение наркологии",
                    "ReplyType": "message",
                    "Text": "Отделение наркологии" 
                }]}

        message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
        self.viber.send_messages(session['uid'], [message])
        
  


if __name__ == "__main__":
    ViberSay(token)
