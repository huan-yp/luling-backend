import re
import time
import datetime

from global_attributes import G


class Member():

    def __init__(self, qq, name, nicknames) -> None:
        self.qq = qq
        self.name = name
        self.nicknames = nicknames
        

class NicknameMap():
    qq2name = {}
    nickname2qq = {}
    name2qq = {}
    def __init__(self) -> None:
        pass
    
    def insert(self, people:Member):
        self.qq2name[people.qq] = (people.name, people.nicknames)
        self.name2qq[people.name] = people.qq
        for nickname in people.nicknames:
            self.nickname2qq[nickname] = people.qq
    
    def get_name_by_qq(self, qq):
        if qq in self.qq2name:
            return self.qq2name[qq][0]
        return None
    
    def get_name_by_nickname(self, nickname):
        if(nickname in self.nickname2qq):
            return self.qq2name[self.nickname2qq[nickname]]
        return None
    
    def get_qq_by_name(self, name):
        if(name in self.name2qq):
            return self.name2qq[name]
        return None


"""
class Message():
    id = 0 # 消息 id
    content = "" # 消息内容
    sender_qq = "" # 消息发送者的 qq
    sender_idt = "" # 消息发送者的群昵称
    is_sys = False
    
    def __str__(self) -> str:
        return f"{self.sender_qq}({self.sender_idt}):{self.content}"
    
    def __init__(self, rec, id) -> None:
        self.id = id
        prefix = re.compile(r"[\d: -]{18,21}")
        qq = re.compile(r"\([\d]{7,11}\)")
        header = rec[0]
        time_match = prefix.match(header)
        if time_match is None:
            raise ValueError("Incorrect Rec Format:" + str(rec))
        
        header = header[time_match.span()[1]:]
        qq_match = qq.search(header)
        if qq_match == None:
            self.sender_qq = "10000"
            self.is_sys = True
            return 
        self.sender_qq = qq_match.group()[1:-1]
        self.sender_idt = header[:qq_match.span()[0]]
        self.content = rec[1]
"""
       
class Message():
    sender = "" # qq 号
    group = "" # 群号
    date = "" # 时间
    content = "" # 内容
    reply = 0 # 如果 AI 做出了回复, 那么为回复消息的 id 
    def __init__(self, dic:dict) -> None:
        """
        Args:
            dic (dict): mirai 发送的字典/数据库的字典
            :如果是数据库的字典中有 date, 如果没有则立即记录当前 date
        """
        if "user" in dic:
            self.sender = dic["user"]
        else:
            self.sender = dic["sender"]
        self.group = dic["group"]
        if "date" in dic:
            self.date = str(dic["date"])
            if self.date.find(".") == -1:
                self.date += ".000"
        else:
            self.date = datetime.datetime.now().__str__()[:-3]
        if "reply" in dic:
            self.reply = dic["reply"]
        self.content = dic["content"]    
    
    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, __o: object) -> bool:
        return self.date == __o.date
    
    def __hash__(self) -> int:
        return hash(self.date)
    
    def __lt__(self, __o: object):
        return self.date < __o.date