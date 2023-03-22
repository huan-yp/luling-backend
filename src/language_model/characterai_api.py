import requests
import os
import re
import time

from language_model.general import CheckNetWork, Bot, RequestError
from constants import C
from global_attributes import G


def decode_message(message_string:str):
    """将获取到的 HTTPS body 解码为 ResponseChain
    Returns:
        [{"text":"t1", id: "123"}, {"text":"t2", id: "124"}, ]
    """
    re_pattern = re.compile("\"speech\": \"[\s\S]+?\"")
    message_string = message_string.replace("false", "False")
    message_string = message_string.replace("true", "True")
    message_string = f"({message_string})"
    message_string = message_string.replace("\n", ",")
    message_string = message_string.replace("{\"text\":\"", "{\"text\":u\"")
    message_string = re_pattern.sub("\"speech\": \"hhh\"", message_string)
    message_string = re.sub(" {100,}", " ", message_string)
    message_string = message_string.replace(",,", ",")
    reponse = eval(message_string)
    messages = []
    for reply in reponse:
        if reply["is_final_chunk"]:
            messages += reply['replies']
    return messages


class MessageChain():
    """交流消息链, 顺序重要
    """
    def __init__(self, response_chain):
        """
            response_chain (回应链): [{"text":"t1", id: "123"}, {"text":"t2", id: "124"}, ]
        """
        self.current_message = 0
        self.messages = []
        for response in response_chain:
            response["text"] = response["text"].replace("\\", "")
            self.messages.append((response["text"], response["id"]))
    
    def get_text_by_id():
        pass
    
    def merge(self, response_chain):
        for response in response_chain:
            self.messages.append((response["text"], response["id"]))
        
    def rate_current(self, score):
        pass
    
    def rate_id(self, id, score):
        pass
    
    @property
    def current_text(self):
        return self.messages[self.current_message][0]
      
    
class BetaAIBot(Bot):
    
    def __init__(self, his, char, tgt, name="") -> None:
        super().__init__(name)
        self.history = his # history_external_id
        self.character = char # character_external_id
        self.tgt = tgt # tgt
        self.current_interaction = None # MessageChain
        pass
    
    def _chat(self, text):
        data = C.CHAT_TEMPLATE_DATA
        data["history_external_id"] = self.history
        data["character"] = self.character
        data["tgt"] = self.tgt
        data["text"] = text
        try:
            response = requests.post(f"{C.URL}/chat/streaming/", headers=C.CHAT_TEMPLATE_HEADERS, data=data, proxies=C.PROXY)
        except (Exception, BaseException) as e:
            if CheckNetWork():
                statu_text = "临时网络波动, 请重试"
            else:
                statu_text = "当前网络状态异常, 请等待 5 分钟后重试"
            return f"{statu_text}\n\n Exception {str(e)}, occurred.\n" 
        if response.status_code == 200:
            self.current_interaction = MessageChain(decode_message(response.text))
            return self.current_interaction.current_text
        else:
            return f"An Http Error Encountered,{str(response.status_code)}, {str(response.headers)}"
    
    def change(self):
        pass
    
    def rate(self, score):
        pass


        
        