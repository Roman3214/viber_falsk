from config import BOT_TOKEN

from flask import Flask, request, Response
import sqlite3
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage


from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
#from .test_db import users_id_db


def init_webhooks(base_url):
    viber.set_webhook('https://viber.com/botforimportantnotifications')
    pass


app = Flask(__name__)

viber = Api(BotConfiguration(
    name='InformationBot',
    avatar='http://site.com/avatar.jpg',
    auth_token= BOT_TOKEN
))


@app.route('/', methods=['POST'])
def incoming():
    #logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)
    
    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())
    print(viber_request)
    if isinstance(viber_request, ViberConversationStartedRequest):
        name_user = viber_request.user.name
        #user_surname = ViberConversationStartedRequest.user.name format l: /fs:fat32 /q
        user_id = viber_request.user.id
        print(name_user, user_id)
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
        #cursor.execute("SELECT `user_id` FROM `users_telegram` WHERE `user_id` = ?", (f'{int(user_id)}',))
            
            cursor.execute('INSERT OR IGNORE INTO "users_viber" ("user_name" , "user_id") VALUES (?,?)', (f'{str(name_user)}',  f'{str(user_id)}', ))
            
            conn.commit()

        
        except sqlite3.Error as error:
            print('Error', error)
    
        finally:
            if(conn):
                conn.close()

    elif isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        print(message)
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberUnsubscribedRequest):
        
        #user_surname = ViberConversationStartedRequest.user.name format l: /fs:fat32 /q
        user_id = viber_request.user_id
        print(user_id)
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
        #cursor.execute("SELECT `user_id` FROM `users_telegram` WHERE `user_id` = ?", (f'{int(user_id)}',))
            
            cursor.execute('DELETE FROM "users_viber"  WHERE `user_id` = ? ', (  f'{str(user_id)}', ))
            
            conn.commit()

        
        except sqlite3.Error as error:
            print('Error', error)
    
        finally:
            if(conn):
                conn.close()
    return Response(status=200)
'''
elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
'''
    
    
    #elif isinstance(viber_request, ViberFailedRequest):
    #    logger.warn("client failed receiving message. failure: {0}".format(viber_request))
'''
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
       #cursor.execute("SELECT `user_id` FROM `users_telegram` WHERE `user_id` = ?", (f'{int(user_id)}',))
        
        cursor.execute('INSERT OR IGNORE INTO "users_viber" ("user_name", "user_surname" , "user_id") VALUES (?,?,?)', (f'{str(name)}', f'{str(first_name)}',  f'{int(user_id)}', ))
        
        conn.commit()

      
    except sqlite3.Error as error:
        print('Error', error)
 
    finally:
        if(conn):
           conn.close()
'''

    



if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(port=8887,  debug=True) 
