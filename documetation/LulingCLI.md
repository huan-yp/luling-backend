## LuLing CLI

机器人的管理工具，虽然名字叫 CLI，实际上它不是 CLI。

### 描述格式

`[qq号]` 表示 qq 号字符串，其它描述依次类推。

### Luling CLI 语法：

#### 语法

形如 `[一些不知道是什么东西的内容] /cmd [命令名称] [一个参数] [另一个参数] [后面还可以跟很多参数] ` 是一条 Luling CLI 命令。

参数之间必须以空格隔开。

如果参数本身含空格, 那么需要用 `""` 括起命令, 如果命令参数中含有 `"`, 需要用 `\` 转义, 即 `\"` 表示字符 `"`, 而字符 `"` 表示括起命令的符号。

同样的, `\\` 表示字符 `\`, 而 `\` 表示转义符, 如果转义符后的字符未定义, 那么程序的行为不可预测。

每一个参数都不能为空串。

命令内容为 `[命令名称]` **及之后**的所有内容，也就是说 `/cmd` 只是一个标识符。

举例:

```
"@鹿灵 /cmd help" 是 Luling CLI 命令，命令内容为 "help"
"jdafhjkhfjkasf /cmd help" 是 Luling CLI 命令，命令内容为 "help"
"/cmd help" 是 Luling CLI 命令
"/cmd [命令名] [还是一个参数] [另一个参数]" 是 Luling CLI 命令
"@鹿灵 cmd help" 不是 Luling CLI 命令
"@鹿灵 /help" 不是 Luling CLI 命令
```
#### 所有有定义的转义符:

```
\": 表示字符 `"`
\\: 表示字符 `\`
```

### 命令参考手册

权限组和权限见 `./documentation/access.md`。

```
help: 展示帮助信息
show statu: 展示所有全局变量信息
show access: 展示所有权限信息
set_statu [key] [value]: 将全局变量 [key] 的值设置为 [value] 
online: 语言模型下线
offline: 语言模型上线
set_access [qq号] [权限组]: 将 [qq号] 设置为 [权限组] 用户
erase_access [qq号]: 将 [qq号] 设置为普通用户
```

#### 全局变量

**区分大小写。**

机器人是否上线的变量不是全局变量。

```
SERVER_DEBUG: 
	:是否为调试模式，如果为调试模式则不会真正向语言模型请求，部分其它流程也不会执行，只会返回测试信息。
	:`True` \ `False`
	:默认 False
PREFIX_NAME:
	:是否根据群昵称为消息添加前缀昵称
	:`True` \ `False`
	:默认 True
```



