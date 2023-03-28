import os
import sys

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "src"))

from json import dumps, loads
from utils.tools import yaml2dict
import socket
import random

SETTINGS_PATH = "user_settings.yaml"
GROUP = "".join(random.sample('1234567890' * 12, 12))
QQ = "".join(random.sample('1234567890' * 12, 12))
NICK_NAME = "小明"

settings = yaml2dict(SETTINGS_PATH)

def chat(text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((settings['host'], settings['port']))
    data = {
        "user": QQ,
        "group": GROUP ,
        "content": f"{NICK_NAME}:@{settings['qq']}{text}"
    }
    data = dumps(data)
    sock.send(data.encode('utf-8'))
    res = loads(sock.recv(65536).decode('utf-8'))
    sock.close()
    return res["text"]


if __name__ == '__main__':
    while True:
        print("请输入你的消息")
        text = input()
        print("AI:", chat(text))