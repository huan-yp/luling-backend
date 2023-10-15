
from flask import Flask, request, render_template
import os
import sys
from os.path import dirname

os.chdir(dirname(dirname(__file__)))
sys.path.append(os.path.join(os.getcwd(), 'src'))

from json import dumps, loads
from utils.tools import yaml2dict
import socket
import random

ALLOW_LIST = {"3051561876":"幻影彭", "1202101":"高三一班(全体同学)", "120210139":"周楚"}
SETTINGS_PATH = "user_settings.yaml"
GROUP = "1202101"
# GROUP = "".join(random.sample('1234567890' * 12, 12))
# QQ = "".join(random.sample('1234567890' * 12, 12))
NICK_NAME = "小明"

settings = yaml2dict(SETTINGS_PATH)

def chat(text, user):
    try:
        if user not in ALLOW_LIST:
            return "You Are Not Allowed"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((settings['host'], settings['port']))
        data = {
            "user": user,
            "group": GROUP ,
            "content": f"{ALLOW_LIST[user]}:@{settings['qq']}{text}"
        }
        data = dumps(data)
        sock.send(data.encode('utf-8'))
        res = loads(sock.recv(65536).decode('utf-8'))
        sock.close()
    except:
        return "API NOT FOUND"
    return res["text"]

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    ai_response = ""  
    if request.method == 'POST':
        user_text = request.form.get('user_text') 
        user = request.form.get('user_id')
        print(user)
        print(user_text)
        if user_text:
            ai_response = chat(user_text, user) 
    return render_template("index.html", ai_response=ai_response)  

if __name__ == '__main__':
    app.run(debug=True)