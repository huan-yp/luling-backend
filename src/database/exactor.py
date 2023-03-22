


from utils.tools import read_file, write_file, read_file_lines
from database.data_structure import Message
import jiagu
import math



def ignore_at(content:str):
    """删除消息中的 @ 部分
    Args:
        text (str): 原始文本
    Returns:
        str: 移除 @ 之后的消息   
    """
    at = re.compile(r"@.*?\s")
    mchs = at.finditer(content)
    for mch in mchs:
        content = content.replace(mch.group(), "")
    return content


def to_text(messages):
    """将消息转化为一整段长文本
    """
    idts = get_names(messages)
    text = ""
    
    for message in messages:
        content = message.content
        text += content
        text += '\n'
    
    for i, idt in enumerate(idts):
        text = text.replace(idt, "")
        if i % 10 == 0:
            print("Processing, Now", i)
    return text


def get_names(messages):
    idts = set()
    title = re.compile(r"【.*】")
    for message in messages:
        idt = message.sender_idt
        title_match = title.match(idt)
        if title_match:
            idt = idt.replace(title_match.group(), "")
        idts.add(idt)
        
    return idts
    

def split_text(text:str):
    """从 qq 导出的聊天记录中解析成列表
    Returns:
        list((str, str)...): 列表中第一个元素为头信息, 第二个元素为消息内容
    """
    messages = []
    lines = text.split('\n')
    i = 0
    time_re = re.compile(r"\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}")
    while i < len(lines) - 1:
        line = lines[i]
        if(time_re.match(line) is not None):
            h = line
            i += 1
            text = ""
            while len(lines[i]) != 0 and time_re.match(lines[i]) is None:
                text += lines[i]
                i += 1
            messages.append((h, text))
        else:
            i += 1    
        
    return messages


def exact(text):
    """从文本中解析聊天记录
    Args:
        text (str):
    Returns:
        list(Message): 消息列表
    """
    result = []
    cnt = 0
    messages = split_text(text)
    for message_origin in messages:
        cnt += 1
        result.append(Message(message_origin, cnt))
    return result


def find_key_word(messages):
    text = to_text(messages)
    idts = get_names(messages)
    write_file("./data/tmpi.txt", text)
    print("Finding")
    jiagu.findword("./data/tmpi.txt", "./data/tmpo.txt")
    with open("./data/tmpo.txt", mode="a+", encoding="utf-8") as f:
        for idt in idts:
            if len(idt) >= 2:
                f.write(idt + " 100\n")
         
    return read_file("./data/tmpo.txt")
    

def read_key_word(lines):
    key_word = {}
    for line in lines:
        rec = line.split()
        if len(rec) < 2:
            continue
        key_word["".join(rec[:-1])] = int(rec[-1])
    return key_word


def calc_weight(words:dict, messages:list, output_file="result.txt"):
    """计算昵称权重

    Args:
        words list(str): 所有关键词
        messages list(Message): 消息列表
    Returns:
        dict(qq,): _description_
    """
    jiagu.load_userdict(list(words.keys()))
    T = min(len(messages), 10 ** 7)
    members = {}
    word_val = {}
    word_max = {}
    normal = []
    members_name = {}
    for word in words:
        word_val[word] = {}
    
    for i in range(T):
        message = messages[i]
        swords = jiagu.seg(message.content)
        wt = (1 - math.log(T - message.id + 10) / math.log(T)) * .8 + 0.2
        for word in swords:
            
            def calc_exist_w(word1, word2):
                e = 0
                for c in word1:
                    e += word2.find(c) != -1
                if e == 0:
                    return .5
                elif e == 1:
                    return .66
                else:
                    return 1 - 1 / (e ** 2 + 1)

            def add_weight(tar, key, w, name):
                if tar not in word_val[key]:
                    word_val[key][tar] = 0   
                word_val[key][tar] += w
                if tar not in members:
                    members[tar] = {}
                    members_name[tar] = name
                dst = members[tar]
                if key not in dst:
                    dst[key] = 0
                dst[key] += w
                
            def walk_range(start, end, gap):
                d = 0
                for j in range(start, end, gap):
                    p_message = messages[j]
                    # if p_message.sender_qq == message.sender_qq:
                        # continue
                    wd = max(1 - d / 6, 0)
                    wc = calc_exist_w(word, message.sender_idt)
                    w = wc * wd * wt
                    # print(w)
                    d += 1
                   
                    add_weight(p_message.sender_qq, word, w, p_message.sender_idt)
            
            if word not in words:
                continue
            
            walk_range(i, max(i - 10, 0), -1)
            walk_range(i + 1, min(T, i + 10), 1)
           
                
        if(i % 1000 == 0):
            # print(wt)
            print("Processing, Now:", i)
    
    for key, val in word_val.items():
        sm, mv = 0, 0
        w = sorted(val.values(), reverse=True)
        sm = sum(w)
        
        if sm < 10 or (sm > 2000 and w[0] / w[1] < 1.5):
        # if sm < 20 or w[0] / w[1] < 1.5:
            normal.append(key)
            continue
        
        word_val[key] = sorted(val.items(), key=lambda x:x[1], reverse=True)
        word_max[key] = word_val[key][0][0]
    
    # print(word_max)
    s = ""
    for key, val in list(members.items()):
        a = sorted(val.items(), key=lambda x:x[1], reverse=True)
        b = []
        for k, v in a:
            if k in normal:
                continue
            if v * 5 < word_val[k][0][1]:
                continue
            # print(k, word_val[k])
            b.append(k)
        # print()
        if len(b):
            s += str(members_name[key]) + ":" + str(key) + "\n"
            s += str(b[:100]) + "\n"
        
        # print(members_name[key], ":")
        # print(b[:5])
    
    write_file(output_file, s)
    

if __name__ == '__main__':
    import re
    messages = exact((read_file("./data/chat_his.txt")))
    # print(find_key_word(messages))
    words = read_key_word(read_file_lines("./data/keywords.txt"))
    calc_weight(words, messages, "./no_weight.txt")
    
