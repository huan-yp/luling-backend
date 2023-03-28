## API

鹿灵AI 后端使用传输层接口，端口和地址在 `user_settings.yaml` 中配置。

### Request

请求的数据应该为一个 JSON 字符串，二进制长度小于 $2^{16}$，应一次性发送完毕，格式如下：

```json
{
    "user": "123456",
    "content": "hello",
    "group": "12345"
}
```

`user` 为用户 qq 号，`content` 为聊天内容，`group` 为所属 qq 群号。

### Response

请求的响应也为一个 JSON 字符串，一次性发送完毕，发送完毕后会关闭 TCP 连接。

```json
{
    "text": "hi",
    "user": "123456"
}
```

`user` 为请求用户 qq 号，`text` 为响应文本。

### Test

可以使用 `./src/test/localClient.py` 测试后端是否正常工作。
