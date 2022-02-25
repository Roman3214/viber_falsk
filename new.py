from config import BOT_TOKEN
import os
import sys
from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
#import logger 

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

#from pyngrok import ngrok
#from ngrok_ import ngrok_started
#from pyngrok import ngrok 

#from flask_ngrok import run_with_ngrok
'''
def ngrok_started():
        
    # Open a HTTP tunnel on the default port 80
    # <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">
    http_tunnel = ngrok.connect(5001)

    begin = str(http_tunnel).find('http:')
    enD = str(http_tunnel).find('.io')

    URL = str(http_tunnel)[begin : enD+3]
    sTr = ['{\n"url": "', '"\n}']
    file_json_viber = URL.join(sTr)
    #file_json_viber = '{"url":f'{URL}' }'


    with open('viber2\\viber.json', 'w') as file:
        file.write(file_json_viber)
    #ngrok.disconnect(http_tunnel.public_url)
    return  file_json_viber
'''
def init_webhooks(base_url):
    viber.set_webhook('https://viber.com/botforimportantnotifications')
    pass


app = Flask(__name__)
'''app.config.from_mapping(
        BASE_URL="http://localhost:5001",
        USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
    )'''
#ngrok_started()
'''
http_tunnel = ngrok.connect(5000)

begin = str(http_tunnel).find('http:')
enD = str(http_tunnel).find('.io')

URL = str(http_tunnel)[begin : enD+3]
sTr = ['{"url": "', '"}']
file_json_viber = URL.join(sTr)
    #file_json_viber = '{"url":f'{URL}' }'


with open('viber\\viber.json', 'w') as file:
    file.write(file_json_viber)
'''
viber = Api(BotConfiguration(
    name='InformationBot',
    avatar='http://site.com/avatar.jpg',
    auth_token= BOT_TOKEN
))

#run_with_ngrok(app)
'''
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
    USE_NGROK=os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("WERKZEUG_RUN_MAIN") != "true"
    )
#run_with_ngrok(app)
if app.config.get("ENV") == "development" and app.config["USE_NGROK"]:
        # pyngrok will only be installed, and should only ever be initialized, in a dev environment
        from pyngrok import ngrok

        # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

        # Update any base URLs or webhooks to use the public ngrok URL
        app.config["BASE_URL"] = public_url
        init_webhooks(public_url)
'''

@app.route('/', methods=['POST'])
def incoming():
    #logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())
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



# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">


#os.system('cd /D E:/diplom/viber')
#subprocess.run('cd /D E:/diplom/Fast_api')
#os.system('curl -# -i -g -H "X-Viber-Auth-Token: 4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')



if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    #ngrok_started()
    #os.system( 'curl -# -i -g -H "X-Viber-Auth-Token: 4ebcf06bb7a7dc35-660577619c3cc428-b4d38da3cd44b45" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')

    app.run( debug=True) 
    #ngrok.kill()
    