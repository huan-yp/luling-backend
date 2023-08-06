
import yaml
import os
import sys
import openai

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "src"))

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
        G.__dict__.update(G.config["global_attributes_defaults"])


def config_env():
    load_config(C.CONFIG_PATH)
    proxy = G.config['proxy']
    if(proxy['enable']):
        G.proxy = f"{G.config['proxy']['host']}:{G.config['proxy']['port']}"
        # os.environ['http_proxy'] = f"{proxy['host']}:{proxy['port']}"
        # os.environ['https_proxy'] = f"{proxy['host']}:{proxy['port']}"  
 
    
if __name__ == '__main__':
    config_env()
    main()