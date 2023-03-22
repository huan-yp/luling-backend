
import yaml
import os
import openai

from server.localServer import main
from global_attributes import G
from constants import C


def load_config(path):
    with open(path, mode="r", encoding="utf-8") as f:
        G.config = yaml.load(f, yaml.FullLoader)
        G.qq = G.config["qq"]
        G.name = G.config["name"]
        G.port = G.config["port"]
        G.host = G.config["host"]


def config_env():
    load_config(C.CONFIG_PATH)
    proxy = G.config['proxy']
    if(proxy['enable']):
        os.environ['http_proxy'] = f"{proxy['host']}:{proxy['port']}"
        os.environ['https_proxy'] = f"{proxy['host']}:{proxy['port']}"  
 
    
if __name__ == '__main__':
    config_env()
    main()