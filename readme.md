## 鹿灵 AI

一个基于 GPT 的 AI 聊天框架，可以通过计算信息关联度生成合适的 prompt 以改进 AI 回复，能够保存所有历史聊天信息。

本项目为后端项目, 前端结构比较简单, 可以自行编写, 本项目的示例前端使用 `mirai-console`.

### 配置

#### 硬件要求
内存要求较高, 最低内存 16GB, 推荐内存 32GB 及以上, 因此不建议部署于云服务器.
#### 使用 docker

前端还没写文档, 建议使用该方式, 以下步骤默认操作系统为 Windows10.

已经创建了一个整合了前后端的 docker, 安装好了所有依赖. 只需要配置好 `user_settings.yaml` 和 `mirai-console-loader` 相关的内容.

0. [安装 docker](https://zhuanlan.zhihu.com/p/441965046)

1. 打开命令行, 从 dockerhub 拉取本项目的 docker image

  ```shell
  docker pull huanyp/luling
  ```

2. 以该镜像创建一个容器

  ```sh
  docker run -it huanyp/luling
  ```

  此时你已经进入了容器, 命令行显示 `root@d3c0f54adf2a:/#`, `@` 后面的字符串每个人都不同.

3. 拉取最新版本的后端

  ```
  cd /home/luling-backend/ && git pull && cd /
  ```

4. 进入容器测试一下有没有问题, 然后配置好 `user_settings.yaml`

  ```
  python3 /home/luling-backend/main.py
  ```

  如果看到 `INFO - Server Start`, 那么启动成功.
  接下来 `Ctrl+C` 退出, 继续下面的配置。

  ```
  vim /home/luling-backend/user_settings.yaml
  ```

  填好 `api_key`, api_key 在 OpenAI 官网生成, 然后是机器人名称 `name`,  机器人账号 `qq`.
  *vim 是一个文本编辑器, 不会用可以上网搜.*

5. 配置好代理
  中国大陆使用一般要配置代理，建议使用 clash，用以下命令安装 clash

  ```shell
  mkdir /home/clash
  cd /home/clash
  wget https://github.com/Dreamacro/clash/releases/download/v1.14.0/clash-linux-amd64-v1.14.0.gz -O clash.gz
  gzip -d clash.gz
  chmod 777 clash
  ./clash
  ```

  出现提示 `INFO[0058] Mixed(http+socks) proxy listening at: 127.0.0.1:7890` 后 `Ctrl+C` 退出准备填写代理配置。

  - 如果你知道怎么填就自己填。
  - 如果你不知道怎么填，按照以下步骤：
    - 拿到你的节点订阅链接，形如 `https://www.example.com/exmaple_suffix`。
    - 执行 `wget https://www.example.com/exmaple_suffix -O ~/.config/clash/config.yaml `

  

  然后测试一下代理是否能正常用：

  ```sh
  ./clash &
  cd /
  curl -x localhost:7890 http://www.google.com/
  ```

  如果输出了一大堆东西，说明成功了，`Ctrl+C` 返回。

  后端的代理默认开启 7890 端口，所以可以直接下一步了。

6. 测试运行

   ```sh
   python3 /home/luling-backend/src/test/localClient.py
   ```

   尝试对话，如果回复正常，则后端工作正常。

0. [配置登录 mirai-console](https://mirai-docs.doomteam.fun/docs/noob)
   其它部分全部封装好了, 只需要看登录. **mirai 登录是本项目最大门槛.**

1. 正式启动

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

### 未来功能

- 改进记忆库算法.
- 尝试计算感情倾向引导词语.
- 支持 GPT4 以及多媒体.
- 降低硬件要求.

