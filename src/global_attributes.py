import yaml

from constants import C
from threading import Lock


class GlobalAttr():
    statu = 'waiting' # 语言模型状态
    lock = Lock() # 语言模型锁
    access_processor = None # 权限处理实例
    bot_online = True # 机器人是否在线
    main_processor = None 
    translator = None
    chatgpt_config = None # chatgpt 配置实例
    config = None
    language_model = None # 语言模型名称
    main_bot = None # 机器人实例
    name = "" # 机器人名称
    db = None
    qq = "" # 机器人 qq 号
    host = "" # 后端地址
    port = 0 # 后端端口
    SERVER_DEBUG = False # 是否是调试模式
    PREFIX_NAME = True # 是否添加前缀
    
    def __init__(self) -> None:
        pass
    
    


G = GlobalAttr()

