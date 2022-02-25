from pyngrok import ngrok, process
import os

http_tunnel = ngrok.connect(5000)

https_tunnel = http_tunnel.public_url.replace('http', 'https')
sTr = ['{\n\t"url": "', '"\n}']
file_json_viber = https_tunnel.join(sTr)

with open('viber.json', 'w') as file:
    file.write(str(file_json_viber))   
