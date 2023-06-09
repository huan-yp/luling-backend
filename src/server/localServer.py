"""使用 Python-socketserver 搭建的微服务
使用 TCP 协议发送数据, 建议使用 socket 提供的接口
"""

import os
import time
import socketserver
import threading as th
import traceback


from logging import INFO, ERROR
from json import loads, dumps, load

from server.manager import AccessProcessor, MainProcessor
from utils.tools import yaml2dict, is_UTF_8
from language_model.chatgpt_api import ChatGPTConfig, ChatGPTBot
from constants import C
from global_attributes import G
from utils.translate import Translator
from utils.logger import logger
from database.data_structure import Message
from database.database_api import DataBaseMangeer
    
    
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request         # request里封装了所有请求的数据
        data = conn.recv(65536).decode('utf-8')
        if not data:
            conn.close()
            return 
        logger.log(INFO, "origin:" + str(data))
        request_dict = loads(data)
        request_chat = Message(request_dict)
        
        # 检查消息是否为 utf-8 字符串
        # if is_UTF_8(request_chat.content):
        response = get_response(request_chat)
        # else:
        #     logger.log(INFO, "content is not utf-8")
        #     if f"@{G.qq}" in request_chat.content:
        #         conn.sendall(dumps({"text":"喵喵, 暂时还无法处理非 utf-8 字符喵\n检查下你的 qq 昵称或者消息内容是不是包含了非 unicode 字符喵~", "user":request_chat.sender}).encode('utf-8'))
        #     else:
        #         conn.sendall(dumps({"text":"", "user":request_chat.sender}).encode('utf-8'))
        #     return 
        
        # 根据机器人的回复创建 qq 回复
        if response:
            logger.log(INFO, "response_overview:" + str(response))
            logger.log(INFO, "response_content:\n" + response.content)
            conn.sendall(dumps({"text":response.content, "user":request_chat.sender}).encode('utf-8'))
        else:
            logger.log(INFO, "message received")
            conn.sendall(dumps({"text":"", "user":request_chat.sender}).encode('utf-8'))
        conn.close()
            

def add_message(message:Message):
    logger.debug("Data Inserted:" + str(message))
    G.db.insert_message(message)

           
def get_response(request:Message) -> Message:
    """通过 Message 获取 Response
        Returns:
            Message: 回复的消息类
            None: 不处理该消息
    """
    try:
        statu, text = G.main_processor.process_cmd(text=request.content, user=request.sender)
        if statu:
            return Message({
                "sender": G.qq,
                "content": text,
                "group": request.group,
            })
    except (Exception, BaseException) as e:
        logger.error(traceback.format_exc())
        raise e
        
    p = th.Thread(target=lambda:add_message(request))
    p.start()
    
    try:
        logger.log(INFO, "request_overview:" + str(request))
        logger.log(INFO, "request_content:" + request.content)
        reply = G.main_processor.process(request)
        if isinstance(reply, str):
            reply = Message({
                "content": reply,
                "sender": G.qq,
                "group": request.group
            })
        return reply
    except (Exception, BaseException) as e:
        logger.log(ERROR, traceback.format_exc())
        reply_text = "Message With Error:\n" + str(e)
        return Message({
            "content": reply_text,
            "sender": G.qq,
            "group": request.group,  
        })


def set_language_model():
    G.language_model = G.config["language_model"]  
    if(G.language_model == "chatgpt"):
        G.chatgpt_config = ChatGPTConfig(G.config)
        G.chatgpt_config.load()


def set_database():
    database_config = G.config['database']
    G.db = DataBaseMangeer(database_config)


def load_class():
    G.access_processor = AccessProcessor()
    G.main_processor = MainProcessor()
    G.translator = Translator()
    G.main_processor.set_bot(ChatGPTBot("鹿灵"))


def load_note_messages():
    dict = yaml2dict(G.config["note_message_path"])
    C.__dict__.update(dict)


def main():
    set_language_model()
    set_database()
    load_note_messages()
    load_class()
    server = socketserver.ThreadingTCPServer((G.host, G.port), MyServer)
    logger.log(INFO, "Server Start")
    server.serve_forever()
    
    