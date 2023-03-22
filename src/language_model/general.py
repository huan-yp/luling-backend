import requests
import os
import re
import time

from threading import Lock

from constants import C
from global_attributes import G


def CheckNetWork():
        """检查网络状况, 网络正常返回 True, 否则返回 False
        """
        time.sleep(.5)
        return os.system("ping beta.character.ai") == False


class RequestError(BaseException):
    
    def __init__(self, response:requests.Response) -> None:
        self.response = response
        super().__init__(f"StatuCode:{response.status_code}")
      
    
class Bot():
    lock = Lock()
    statu = True # 机器人状态, 为 True 表示可以处理信息
    def __init__(self, name) -> None:
        self.name = name
    
    def _chat(self, message):
        """实际的对话函数, 需要重写
        """
        pass
    
    def chat(self, message):
        """对话函数接口
        """
        if not G.bot_online:
            return C.OFFLINE_MESSAGE
        
        self.lock.acquire()
        if not self.statu:
            self.lock.release()
            return None    
        self.statu = False
        self.lock.release()
        
        if C.SERVER_DEBUG:
            time.sleep(10)
            return """
                Test Message:
                first line: "\\'
                
                second line: 😊
                Test Ok
            """
            
        msg = self._chat(message)
        self.lock.acquire()
        self.statu = True
        self.lock.release()
        return msg
    
