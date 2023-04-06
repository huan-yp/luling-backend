
import yaml
import os
import datetime

def write_file(path, text, encoding="utf-8"):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except BaseException as e:
        print(e)
    with open(path, mode="w+", encoding=encoding) as f:
        f.write(text)


def read_file_lines(path, encoding="utf-8"):
    with open(path, mode="r", encoding=encoding) as f:
        return f.readlines()


def read_file(path, encoding='utf-8'):
    with open(path, mode="r", encoding=encoding) as f:
        return f.read()
    
    
def yaml2dict(path, endcoding='utf-8'):
    with open(path, mode="r", encoding=endcoding) as f:
        return yaml.load(f, yaml.FullLoader)
    
    
def get_timestamp_from_string(date_string):
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    msg_time = datetime.datetime.strptime(date_string, DATE_FORMAT)
    msg_time += datetime.timedelta(microseconds=(msg_time.microsecond // 1000) * 1000)
    return msg_time.timestamp()


def is_UTF_8(str):
    remain = 0
    for x in range(len(str)):
        if remain == 0:
            if (ord(str[x]) & 0x80) == 0x00:
                remain = 0
            elif (ord(str[x]) & 0xE0) == 0xC0:
                remain = 1
            elif (ord(str[x]) & 0xF0) == 0xE0:
                remain = 2
            elif(ord(str[x]) & 0xF8) == 0xF0:
                remain = 3
            else:
                return False
        else:
            if not ((ord(str[x]) & 0xC0) == 0x80):
                return False
            remain = remain - 1
    if remain == 0:
        return True
    else:
        return False
