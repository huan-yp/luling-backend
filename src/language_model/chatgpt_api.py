import openai
import os
import tiktoken
import traceback
import time
import copy
import datetime

from logging import INFO, WARNING, ERROR, DEBUG
from language_model.general import Bot, RequestError
from global_attributes import G
from constants import C
from utils.tools import read_file, yaml2dict, get_timestamp_from_string
from utils.logger import logger
from database.data_structure import Message


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def num_tokens_from_text(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def num_tokens_from_message(message:Message):
    return num_tokens_from_text(message.content)


def repharse_message(message_chain):
    """将 yaml 文件中用路径描述的部分替换为对应的文字
    """
    for message in message_chain:
        content = message["content"]
        if os.path.isfile(content):
            message["content"] = read_file(content)
    return message_chain 


class ChatGPTConfig():
    
    def __init__(self, config) -> None:
        chatgpt_config = config["chatgpt"]
        self.__dict__.update(chatgpt_config)
    
    def load(self):
        openai.api_key = self.api_key
        self.preset_message = yaml2dict(self.preset_message_path)
        self.preset_message = repharse_message(self.preset_message)


class ChatGPTBot(Bot):
    
    def __init__(self, name) -> None:
        self.message_list = []
        super().__init__(name)
    
    def message2prompt(self, message:Message):
        return message.content
        
    def make_message(self, role, text):
        return {"role":role, "content":text}
    
    def get_max_token(self, message:Message):
        return G.chatgpt_config.max_tokens
        
    def get_temperature(self, message:Message):
        return G.chatgpt_config.temperature
    
    def request(self, messages, t, max_tokens, retry=True):
        """向 api.openai.com 请求
        Args:
            messages (list): 消息文本列表
            t (float): 温度
            max_tokens (int): 响应最大 tokens
            retry (bool, optional): 是否重试. Defaults to True.
        Raises:
            RequestError: 请求失败且重试后仍然失败
        Returns:
            str: 表示回复
        """
        try:
            logger.debug("start request")
            start_time = time.time()
            if retry:
                timeout = G.chatgpt_config.timeout
            else:
                timeout = G.chatgpt_config.retry_timeout
            response = openai.ChatCompletion.create(
                model=G.chatgpt_config.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=t,
                timeout=timeout,
                request_timeout=timeout,
            )
            logger.debug("response time:" + str(time.time() - start_time))
            logger.debug(response)
        except BaseException as e:
            if(retry):
                logger.log(WARNING, "Request Failed, see log for stack details")
                logger.log(WARNING, e)
                logger.debug(traceback.format_exc() + "\n--------------------------\n")
                time.sleep(3)
                return self.request(messages, t, max_tokens, retry=False)
            else:
                logger.log(ERROR, "Request Failed, see log for stack details")
                logger.log(ERROR, e)
                logger.log(DEBUG, traceback.format_exc()  + "\n--------------------------\n")
                raise RequestError("GPT3.5 Request Failed")
            
        choice = response["choices"][0]
        if choice["finish_reason"] == "length":
            logger.info("unfinished chat, increase length to compelete")
            return self.request(messages=messages, t=t, max_tokens=int(max_tokens*2))
        message = response["choices"][0]["message"]["content"]
        return message
        
    def build_related_message(self, message:Message) -> list:
        
        def process_message(message:Message):
            while num_tokens_from_text(message.content) > G.chatgpt_config.fold_token_limit:
                message.content = message.content[:len(message.content) // 2]
                message.content += "..."
        
        def get_reply(message:Message) -> Message:
            return G.db.get_message_by_id(message.reply)
        
        preset_messages = G.chatgpt_config.preset_message
        logger.debug("searhing messages")
        related_messages = G.db.search_related(message)
        final_messages = []
        for msg in related_messages:
            process_message(msg)
            final_messages.append(msg)
                
        final_messages = list(set(final_messages))
        related_messages = sorted(final_messages, reverse=True)
        
        final_messages = []
        timenow = time.time()
        tl1, tl2, tl3, limit = 0, 0, 0, G.chatgpt_config.prompt_token_limit // 3
        for msg in related_messages:
            msg_time = get_timestamp_from_string(msg.date)
            if  (timenow - msg_time < G.chatgpt_config.message_expire and tl1 < limit) or \
                (tl2 + num_tokens_from_message(msg) < limit and msg.reply > 0) or \
                (tl3 + num_tokens_from_message(msg) < limit and msg.sender == message.sender and msg.reply > 0): 
                
                final_messages.append(msg)
                tokens = num_tokens_from_message(msg)
                if msg.reply != 0:
                    try:
                        nmsg = get_reply(msg)
                        process_message(msg)
                        final_messages.append(nmsg)
                        tokens += num_tokens_from_message(nmsg)
                    except (Exception, BaseException) as e:
                        logger.error("Error, reply message query error:" + str(e))
                        logger.info("see log for details")
                        logger.debug(traceback.format_exc())
                    
                if (timenow - msg_time < G.chatgpt_config.message_expire and tl1 < limit):
                    tl1 += tokens
                elif (tl2 + num_tokens_from_message(msg) < limit and msg.reply > 0):
                    tl2 += tokens
                elif (tl3 + num_tokens_from_message(msg) < limit and msg.sender == message.sender and msg.reply > 0):
                    tl3 += tokens
        
        logger.debug("Building Request Messages")            
        final_messages = sorted(final_messages)
        time_inserted = False
        message_list = [] + preset_messages
        for msg in final_messages:
            self.process_message(msg)
            if timenow - get_timestamp_from_string(msg.date) < G.chatgpt_config.message_expire and time_inserted == False:
                message_list.append({
                    "role":"system",
                    "content": f"""Message Above is before {msg.date}.\nMessage Below are recent messages."""
                })
                time_inserted = True 
            if msg.sender == G.qq:
                 
                message_list.append({
                    "role":"assistant",
                    "content": msg.content,
                })
            else:
                if message_list[-1]["role"] == "user":
                    message_list[-1]["content"] += f"\n{msg.content}"
                else:
                    message_list.append({
                        "role": "user",
                        "content": msg.content,
                    })
        
        this_user_messages = [
            {"role":"system", "content":f"Time:{message.date}."},
            # {"role":"system", "content":f"Time:{message.date}.\n请注意，你不是 AI 助手，不应该询问对方是否需要帮助"},
            {"role":"user", "content":message.content},
        ]
        return message_list + this_user_messages
    
    def process_message(self, message:Message) -> bool:
        """处理消息, 判断消息是否应该被发送给语言模型, 会改变 message 的 content
        Args:
            message (Message):
        Returns:
            bool: 处理后的消息是否应该被处理
        """
        at_bot = f"@{G.qq}"
        if at_bot not in message.content:
            return False
        message.content = message.content.replace(at_bot, "")
        return True
    
    def _chat(self, message:Message):
        """实际上的对话方法
        Args:
            message (Message): _description_
        Returns:
            None: 不处理该对话
            Message: 回复消息类
        """
        statu = self.process_message(message)
        if statu == False:
            return None
        
        logger.debug("Building Related Messages")
        request_messages = self.build_related_message(message)
        logger.debug("Getting Max tokens")
        max_token = self.get_max_token(message)
        temperature = self.get_temperature(message)
        logger.log(DEBUG, request_messages)
        try:
            response_text = self.request(
                messages=request_messages, 
                t=temperature, 
                max_tokens=max_token
            )
            response = Message({
                "sender": G.qq,
                "group": message.group,
                "content": response_text
            })
            id = G.db.insert_message(response)
            G.db.label_reply(message, id)
            return response
        except BaseException as e:
            return "An Request Error Encountered When making Request, see log for details"
        
    def clear_context(self):
        self.message_list.clear()