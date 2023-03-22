
import pymysql
import pymysql.cursors
import time

from threading import Lock
from global_attributes import G
from database.data_structure import Message

class DataBaseMangeer():
    lock = Lock()
    def __init__(self, config:dict):
        self.conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            passwd=config['password'],
            db=config['database']
        )
        self.table = config["table"]
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, sql) -> list:
        """只操作能够信任的输入
        Args:
            sql (_type_): _description_
        Returns:
            list: _description_
        """
        self.lock.acquire()
        self.cursor.execute(sql)
        self.lock.release()
        return self.cursor.fetchall()
    
    def exec(self, sql, *args, **kwargs):
        self.lock.acquire()
        self.cursor.execute(sql, *args, **kwargs)
        self.conn.commit()
        self.lock.release()

    def insert_message(self, message:Message) -> int:
        """插入消息, 并返回 id
        带 SQL 注入保护
        """
        sql = f"""
            insert into {self.table}(`sender`, `group`, `content`, `date`) 
            values("{message.sender}", "{message.group}", %s, "{message.date}");
        """
        # sql = f"insert into {self.table}(`sender`, `group`, `content`, `date`) values('%s', '%s', '%s', '%s')"
        # self.cursor.execute(sql, [message.sender, message.group, message.content, message.date])
        self.exec(sql, (message.content))
        return self.cursor.lastrowid
    
    def get_message_by_id(self, id) -> Message:
        return Message(self.query(f"""
            select * from {self.table}
            where `id`={str(id)};
        """)[0])    
    
    def get_id_by_message(self, message:Message) -> int:
        return self.query(f"""
            select * from {self.table}
            where `date`="{message.date}";
        """)[0]["id"]
    
    def label_reply(self, message:Message, id:int):
        """将 message 标记为被回复
            message (_type_): _description_
        """
        sql = f"""
            update {self.table}
            set `reply` = {str(id)}
            where date = "{message.date}";
        """
        self.exec(sql)
    
    def search_related(self, message:Message) -> list:
        """寻找关联消息, 不受 prompt token limit 限制
            : 消息会被分类, 每一类消息一个列表
            Returns:
                list(Message): 
        """
        messages = []
        group_related_message = self.query(f"""
            select * from {self.table}
            where `group` = {message.group} and `sender` != {G.qq}
            order by `date` desc
            limit 40;
        """)
        group_replyed_message = self.query(f"""
            select * from {self.table}
            where `group` = {message.group} and `reply` != 0
            order by `date` desc
            limit 40;
        """)
        person_related_message = self.query(f"""
            select * from {self.table}
            where `group` = {message.group} and `sender` = {message.sender}
            order by `date` desc
            limit 40;
        """)
        person_replyed_message = self.query(f"""
            select * from {self.table}
            where `reply` = true and `sender` = {message.sender}
            order by `date` desc
            limit 40;
        """)
        
        messages += list(map(Message, group_related_message))
        messages += list(map(Message, group_replyed_message))
        messages += list(map(Message, person_related_message))
        messages += list(map(Message, person_replyed_message))
        return messages
        
    def update(self, sql):
        pass

    def delete(self, sql):
        pass

    def close(self):
        self.cursor.close()
        self.conn.close()
    
