import json
import os
#os.system('ngrok http 8887')

def get_ngrok_address():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)
    with open('tunnels.json', 'r') as file_json:
        respone_dict = file_json.read()

    begin = str(respone_dict).find('https:')
    enD = str(respone_dict).find('.io","proto"')
    URL = str(respone_dict)[begin : enD+3]

    with open('viber.json', 'w') as file:
        file.write(str(URL))
    return dict(zip(['http', 'https'], [i['public_url'] for i in datajson['tunnels']]))
get_ngrok_address()