import os

import subprocess
import logging

import json
def get_ngrok_address():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)
        
    with open('tunnels.json', 'r') as file_json:
        respone_dict = file_json.read()

    begin = str(respone_dict).find('https:')
    enD = str(respone_dict).find('.io","proto"')
    URL = str(respone_dict)[begin : enD+3]
    sTr = ['{\n\t"url": "', '"\n}']
    file_json_viber = URL.join(sTr)
    
    with open('viber.json', 'w') as file:
        file.write(str(file_json_viber))
    return dict(zip(['http', 'https'], [i['public_url'] for i in datajson['tunnels']])) 


print(logging.debug("This is a debug message"))
print(logging.info("Informational message"))
logging.error("An error has happened!")




files = ["new2test.py", "new.py"]  # файлы, которые нужно запустить
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)


get_ngrok_address()

os.system ('curl -# -i -g -H "X-Viber-Auth-Token: "<you_auto_token>" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')
