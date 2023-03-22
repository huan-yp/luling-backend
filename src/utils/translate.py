import http.client
import hashlib
import urllib
import random
import json
import time

from constants import C
from global_attributes import G
from utils.logger import logger
from logging import ERROR, INFO
 
class Translator():
    
    # 手动录入翻译内容，q存放
    
    def process_translation_list(self, list):
        res = ""
        for line in list:
            res += f"{line['dst']}\n"
        return res
    
    def translate(self, text):
        salt = random.randint(32768, 65536)
        httpClient = None
        sign = C.APP_ID + text + str(salt) + C.SECRET_KEY
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = C.TRANSLATE_URL + "?action=1" + '&appid=' + C.APP_ID + '&q=' + urllib.parse.quote(text) + '&from=auto' + \
                '&to=zh' + '&salt=' + str(salt) + '&sign=' + sign
        
        # 建立会话，返回结果
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            return self.process_translation_list(result['trans_result'])
        except Exception as e:
            logger.error(str(e))
        finally:
            if httpClient:
                httpClient.close()
                

if __name__ == "__main__":
    print(Translator().translate("""
        (✧σ´д`σ)
        Oh.
        Well of course!
        Well,I still remember you,dear cyber beggar friend!
        Well,dear friend, what's your question at the moment?
        Well,I really want to know about your opinions and personality,dear friend!
        Well,do you want to ask me anything?
        As your friend,please tell me about yourself!
        What do you think about me? Do you want to know about something about me?
        I really want to know about your opinion about me,dear friend!"""
    ))
                
                
                