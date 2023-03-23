## 鹿灵 AI 后端

一个基于 GPT 的 AI 聊天后端，可以通过计算信息关联度生成合适的 prompt 以改进 AI 回复，能够保存所有历史聊天信息。

主要用于 qq 群聊。

### 配置
将 `user_settings_example.yaml` 复制一份，重命名为 `user_settings.yaml`，并在里面填写自己的配置信息。

AI 本身相关的配置在 `user_settings_example.yaml` 里都有注释，可以参照 `./data/example` 下的文件写。

将 `./src` 写入环境变量 `PYTHONPATH`。
```
conda env config vars set PYTHONPATH="./src"
```

安装并配置好 `mysql`。

用一下命令创建一个表：
```
create table if not exists main(
    `id` int not null auto_increment,
    `sender` varchar(64) not null,
    `group` varchar(64) not null,
    `content` varchar(4096) not null,
    `date` datetime(3),
    `reply` int unsigned default 0,
    primary key(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 使用

建议使用本项目对应的前端，如有需求也可以自行编写前端，可以参考 `./documentation` 中的文档编写前端。 

