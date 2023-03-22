
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