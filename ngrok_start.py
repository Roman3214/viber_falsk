import os
import subprocess
import time

files = [ "new2test.py","url.py", "lol.py"]  # файлы, которые нужно запустить
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)
    time.sleep(5)

os.system ('curl -# -i -g -H "X-Viber-Auth-Token: <you_auto_token>" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v')
