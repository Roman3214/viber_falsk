
from config import BOT_TOKEN

import os
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
 
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from pyngrok import ngrok ,conf, process
from fastapi import FastAPI, Response ,Request
import uvicorn
import json

def init_webhooks(base_url):
    viber.set_webhook('https://viber.com/bot...')# you URL boting
    pass

app = FastAPI()

viber = Api(BotConfiguration(
    name='InformationBot',
    avatar='http://site.com/avatar.jpg',
    auth_token= BOT_TOKEN
))


@app.post('/', status_code=201)
def incoming():
    if not viber.verify_signature(Request.get_data(), Request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

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
    
    return Response(status=200)


if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    uvicorn.run(
        "main:app", 
        port=8887,
        #reload=True,
        log_level="info"    
    )



