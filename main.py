
from config import BOT_TOKEN
#import subprocess
import os
#import sys
#from flask import Flask, request, Response
#import nest_asyncio
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
#import logger 
import json
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest


#from ngrok_ import ngrok_started
from pyngrok import ngrok ,conf, process
from fastapi import FastAPI, Response ,Request
#from fastapi.middleware.cors import CORSMiddleware

import uvicorn
'''
import requests
import json
#from config import BOT_TOKEN
auth_token = "4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" # тут ваш токен полученный в начале #п.2
hook = 'https://chatapi.viber.com/pa/set_webhook'
headers = {'X-Viber-Auth-Token': auth_token}


sen = dict(url='https://yourdomain.ru/webhook2020',
           event_types = ['unsubscribed', 'conversation_started', 'message', 'seen', 'delivered'])
# sen - это body запроса для отправки к backend серверов viber
#seen, delivered - можно убрать, но иногда маркетологи хотят знать,
#сколько и кто именно  принял и почитал ваших сообщений,  можете оставить)

r = requests.post(hook, json.dumps(sen), headers=headers)
# r - это пост запрос составленный по требованиям viber 
print(r.json())
'''


#path_json= os.path.exists('viber.json')
#if path_json == True:
#    os.remove('viber.json')




    # Open a HTTP tunnel on the default port 80
    # <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">



#BOT_TOKEN = "4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45"


def init_webhooks(base_url):
    viber.set_webhook('https://viber.com/botforimportantnotifications')
    pass

app = FastAPI()

viber = Api(BotConfiguration(
    name='InformationBot',
    avatar='http://site.com/avatar.jpg',
    auth_token= BOT_TOKEN
))


@app.post('/', status_code=201)
def incoming():
    #logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(Request.get_data(), Request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(Request.get_data())
    print(viber_request)

    
    
    
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
        
        
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    #elif isinstance(viber_request, ViberFailedRequest):
    #    logger.warn("client failed receiving message. failure: {0}".format(viber_request))
 
    return Response(status=200)





#subprocess.run('cd /D E:/diplom/Fast_api')
#os.system('curl -# -i -g -H "X-Viber-Auth-Token: 4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')


    
#run_app = os.system('curl -# -i -g -H "X-Viber-Auth-Token: 4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    uvicorn.run(
        "main:app", 
        port=8887,
        #reload=True,
        log_level="info"    
    )

#get_ngrok_address()
    #os.system('uvicorn main:app --reload --port 8887') and 
    #ngrok.kill()
    #nest_asyncio.apply()   
    #uvicorn.run("main:app", port=8887, log_level="info") 
'''    
i = 0
if i < 1:
    http_tunnel = ngrok.connect(8887)
    i += 1

https_tunnel = http_tunnel.public_url.replace('http', 'https')
sTr = ['{\n\t"url": "', '"\n}']
file_json_viber = https_tunnel.join(sTr)

with open('viber.json', 'w') as file:
    file.write(str(file_json_viber)) 
    '''

 



#uvicorn.run("main:app", host='127.0.0.1', port=8887, log_level="info")
#ngrok.kill
#conf.get_default().log_event_callback = log_event_callback
#conf.get_default().monitor_thread = False
#ngrok.kill()

#subprocess.run('curl -# -i -g -H "X-Viber-Auth-Token: 4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')

#os.system('ngrok.py')    


