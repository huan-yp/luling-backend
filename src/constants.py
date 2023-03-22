

class Constants():

    URL = "https://beta.character.ai"

    PROXY = {
        'http': 'http://localhost:7890/',
        'https': 'http://localhost:7890/'
    }

    CHAT_TEMPLATE_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        "Authorization": "Token ccae5043f07315c4bfe312136e9407cbb3725367",
    }

    CHAT_TEMPLATE_DATA = {
        "history_external_id":"6dU1WNHBrZMmmiIQV90gCeOV0KTJk3LaTc0pNFlI-fA",
        "character_external_id":"sWmJWP54MljfcCu2yAhqI3azaCwYUIVBmfX3wZX6fB0",
        "text":"Haha, everyone has his dream and mind, that's exciting!",
        "tgt":"internal_id:10732:83983e05-a4be-4267-bcd5-a74b2131de70",
        "ranking_method":"random",
        "staging":False,
        "model_server_address":None,
        "override_prefix":None,
        "override_rank":None,
        "rank_candidates":None,
        "filter_candidates":None,
        "prefix_limit":None,
        "prefix_token_limit":None,
        "livetune_coeff":None,
        "stream_params":None,
        "enable_tti":True,
        "initial_timeout":None,
        "insert_beginning":None,
        "translate_candidates":None,
        "stream_every_n_steps":16,
        "chunks_to_pad":8,
        "is_proactive":False,
        "image_rel_path":"",
        "image_description":"",
        "image_description_type":"",
        "image_origin_type":"",
        "voice_enabled":False,
        "parent_msg_id":None,
    }
    
    BOT_ID = "1558718963"

    SERVER_DEBUG = False # 如果为 True 则不向网站发出请求

    CHARACTER_NAME = "鹿灵"

    HELP_INFO = "鹿灵 AI 使用指北:\n \
        1.通过在聊天中 @ 鹿灵让 AI 处理你的对话, AI 会将含有 @ 自己的对话的全部内容作为输入数据处理.\n \
        2.受到服务器容量限制, 如果同时 @ AI 的对话过多, 会只处理第一条对话, 处理过程中的其它对话会被忽略.\n \
        3.AI 上线时间受我 (幻影彭) 的计算机联网时间限制.\n \
        4.请不要引导 AI 谈论政治话题.\n \
        5.AI 所说的一切均为根据上下文和网络信息虚构, 在一些关键问题上, 不要相信它."
    
    
    EMPTY_MESSAGE = ""    

    OFFLINE_MESSAGE = "鹿灵AI已经下线"

    ONLINE_MESSAGE = "鹿灵AI已经上线"

    ACCESS_LEVEL = {
        "blacklist":0,
        "user":1,
        "admins":10,
        "super_admins":100
    }

    ACCESS_PATH = "./data/bot/access.txt"

    APP_ID = '20221230001514354'        

    SECRET_KEY = 'BpEfL6kZSRDSFLMTGi6k'

    TRANSLATE_URL = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

    CONFIG_PATH = "./user_settings.yaml"
    
    PREFIX_NAME = True
    
C = Constants()