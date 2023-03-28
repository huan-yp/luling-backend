## 鹿灵 AI 后端

一个基于 GPT 的 AI 聊天后端，可以通过计算信息关联度生成合适的 prompt 以改进 AI 回复，能够保存所有历史聊天信息。

主要用于 qq 群聊。

### 配置

#### 配置文件

配置文件名为, `user_settings.yaml`, **需要自行创建.**

将 `user_settings_example.yaml` 复制一份，重命名为 `user_settings.yaml`，并在里面填写自己的配置信息。

AI 本身相关的配置在 `user_settings_example.yaml` 里都有注释，可以参照 `./data/example` 下的文件写。

#### 使用 docker

前端还没写文档, 建议使用该方式.

已经创建了一个整合了前后端的 docker, 安装好了所有依赖. 只需要配置好 `user_settings.yaml` 和 `mirai-console-loader` 相关的内容.

0. [安装 docker](https://zhuanlan.zhihu.com/p/441965046)

1. 从 dockerhub 拉取本项目的 docker image
`docker pull huanyp/luling`

2. 以该镜像创建一个容器
`docker run -it huanyp/luling`

#### 手动配置

安装并配置好 `mysql`。

用以下命令创建一个表：
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

咕咕咕.

### 使用

本项目默认前端为 `mirai-console` 插件, 请参考 [mirai 项目文档](https://github.com/mamoe/mirai) 使用.

`src/test/localClient.py` 是一个本地命令行前端, 可以用于测试后端是否正确配置.

**强烈建议中国大陆用户配置好代理.**

