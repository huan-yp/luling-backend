
import functools
import re
import argparse

from constants import C
from global_attributes import G
from language_model.general import Bot
from language_model.chatgpt_api import ChatGPTBot
from json import load, dump

main_bot = G.main_bot


class AccessProcessor():
    """权限管理
    """
    def __init__(self) -> None:
        self.super_admins = ["3051561876", "305399907"] # 权限等级为 100
        self.admins = [] # 权限等级为 10
        self.blacklist = [] # 权限等级为 0
        try:
            self.load_access()
        except:
            self.save_access()
        
    def load_access(self):
        with open(C.ACCESS_PATH, mode="r+") as f:
            self.__dict__.update(load(f))
        
    def save_access(self):
        with open(C.ACCESS_PATH, mode="w+") as f:
            dump(self.__dict__, f)
        
    def get_access_level_by_id(self, qq):
        if qq in self.super_admins:
            return 100
        if qq in self.admins:
            return 10
        if qq in self.blacklist:
            return 0
        return 1

    def set_access(self, qq, access):
        if access == 'blacklist':
            self.blacklist.append(qq)
        if access == 'admins':
            self.admins.append(qq)  
        self.save_access()  
    
    def erase_access(self, qq):
        if qq in self.blacklist:self.blacklist.remove(qq)
        if qq in self.admins:self.admins.remove(qq)
        self.save_access()
        

def authorization_decorator(level=1):
    """权限管理修饰器
    Info:
        函数必须传入命名参数 user
    Args:
        level: 该操作的需求权限等级.
    """
    def decorator(fun):
        @functools.wraps(fun)
        def warpped_function(*args, **kwargs):
            if 'user' not in kwargs:
                raise ValueError("named argument 'user' required")
            user = kwargs['user']
            if G.access_processor.get_access_level_by_id(user) < level:
                return f"User {user} has no access for this operation"
            return fun(*args, **kwargs)
        return warpped_function
    return decorator


def abstract_command(text:str):
    """识别是否是鹿灵CLI命令

    Args:
        text (_type_): _description_
    Returns:
        二元组
        (False, None): 不是鹿灵CLI命令
        (True, [arg1, arg1, ...]): 是鹿灵CLI命令, 参数为 arg1, arg2
        (True, "some info"): 是鹿灵CLI命令, 参数不合法
    """
    if f"@{G.qq}" not in text:
        return (False, None)
    
    escapes = "\"\\"
    match = re.search("/cmd[\s]", text)
    if match == None:
        return (False, None)
    start_index = match.span()[1]
    cmds = text[start_index:]
    i = 0
    exist = 0
    cmd = ""
    result = []
    while i < len(cmds):
        char = cmds[i]
        if char == '\\':
            if i + 1 == len(cmds):
                return (True, "Unmatched escape character")
            i += 1
            if cmds[i] not in escapes:
                return (True, f"Unmatched escape character \\{cmds[i]}")
            cmd += cmds[i]
        elif char == '\"':
            if exist:
                if len(cmd) == 0:
                    return (True, "empty argument")
                exist = 0
                result.append(cmd)
                cmd = ""
            else:
                exist = 1
        elif char == ' ':
            if exist:
                cmd += char
            else:
                if len(cmd):
                    result.append(cmd)
                cmd = ""
        else:
            cmd += char
        i += 1
    if len(cmd):
        result.append(cmd)
    return (True, result)
    

class CommandProcessor():
    """处理命令
    """
    def __init__(self) -> None:
        pass
        # self.parser = argparse.ArgumentParser(prog="LuLing CLI", description="CLI for LuLing AI management")
    
    def set_bot(self, bot:Bot):
        self.bot = bot
    
    def do_command(self, user, args):
        command = args[0]
        if command == "help":
            return self.help(user=user)
        if command == "offline":
            return self.offline(user=user)
        if command == 'online':
            return self.online(user=user)
        if command == 'set_access':
            if len(args) != 3:
                return "Incorrect command format. 'set_access [qq] [access_level]'"
            return self.set_access(user=user, target=args[1], access=args[2])
        if command == 'set_statu':
            if len(args) != 3:
                return "Incorrect command format. 'set_statu [key] [value]'"
            return self.set_statu(user=user, key=args[1], value=args[2])
        if command == "show":
            if len(args) < 2:
                return "Incorrect command format. 'show [key] [optional]'"
            return self.show(user=user, key=args[1], **args[2:])
        if command == "clear_context":
            if len(args) != 1:
                return "Incorrect command format. 'clear_context'"
            return self.clear_context(user=user)
        return None
        
    @authorization_decorator(level=1)
    def help(self, user):
        return C.HELP_INFO
        
    @authorization_decorator(level=10)
    def online(self, user):
        G.bot_online = True
        return C.ONLINE_MESSAGE
    
    @authorization_decorator(level=10)
    def offline(self, user):
        G.bot_online = False
        return C.OFFLINE_MESSAGE
    
    @authorization_decorator(level=10)
    def erase_access(self, user, target):
        if G.access_processor.get_access_level_by_id(user) <= G.access_processor.get_access_level_by_id(target):
            return "You have no access for this operation"
        G.access_processor.erase_access(target)
        return None
    
    @authorization_decorator(level=10)
    def set_access(self, user, target, access):
        erase_info = self.erase_access(user=user, target=target)
        if erase_info is not None:
            return erase_info
        if access not in C.ACCESS_LEVEL.keys():
            return f"access group '{access}' do not exist"
        if G.access_processor.get_access_level_by_id(user) <= C.ACCESS_LEVEL[access]:
            return "You have no access for this operation"
        G.access_processor.set_access(target, access)
        return f"User {target}'s access is set to '{access}'"

    @authorization_decorator(level=10)
    def clear_context(self, user):
        if isinstance(self.bot, ChatGPTBot):
            self.bot.clear_context()
            return f"Context cleared"
        return f"Only ChatGPT Bot Has This Operation"
    
    @authorization_decorator(level=10)
    def set_statu(self, user, key, value):
        if key not in ["SERVER_DEBUG", "PREFIX_NAME"]:
            return f"attribute {key} do not exist"
        if key == "SERVER_DEBUG" or key == "PREFIX_NAME":
            if value not in ["True", "False"]:
                return f"attribute {key} haven't got value {value}"
            exec(f"C.{key} = value == 'True'")

        return f"attribute {key} is set to '{value}'" 
        
    @authorization_decorator(level=1)
    def show(self, user, key, *args):
        if key == "access":
            return str(G.access_processor.__dict__)
        if key == "statu":
            return f"SERVER_DEBUG:{C.SERVER_DEBUG}\nPREFIX_NAME:{C.PREFIX_NAME}"
        if key == "log":
            return "No Supported Yet, Coming Soon"    
        return f"No such key {key} for show command"
            
        
class MainProcessor():
    """消息处理器
    """
    def __init__(self, ) -> None:
        self.command_processor = CommandProcessor() 
    
    def set_bot(self, bot:Bot):
        self.bot = bot
        self.command_processor.set_bot(bot)
    
    def process(self, message):
        """处理非命令信息
        Args:
            message (Message):
        Returns:
            Message: 回复
            None: 该信息不处理 
        """
        return self.bot.chat(message)
    
    def process_cmd(self, text, user):
        is_cmd, args = abstract_command(text)
        if isinstance(args, str):
            return args
        if is_cmd:
            cmd_res = self.command_processor.do_command(user, args)
            if cmd_res is None:
                return (True, f"command {text} do not exist")
            else:
                return (True, cmd_res)
        else:
            return (False, None)
            
    
if __name__ == "__main__":
    print(abstract_command("/cmd set access 13214342 2"))
