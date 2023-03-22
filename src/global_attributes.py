import yaml

from constants import C
from threading import Lock


class GlobalAttr():
    statu = 'waiting'
    lock = Lock()
    access_processor = None
    bot_online = True
    main_processor = None
    translator = None
    chatgpt_config = None
    config = None
    language_model = None
    main_bot = None
    name = ""
    db = None
    qq = ""
    host = ""
    port = 0
    
    def __init__(self) -> None:
        pass
    
    


G = GlobalAttr()

