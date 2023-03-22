## 权限参考

一共四个权限组，权限组名同标题，区分大小写：

### blacklist

没有任何权限，所有请求将会被忽略。

### user

只能对话或者执行 `help` 命令。

### admins

除了不能操作 admins 及以上的权限之外拥有所有 CLI 权限。

### super_admins

拥有所有 CLI 权限，可以操作 admins 及以下的所有用户。

**只能在 `./data/access.txt` 中编辑 super_admins 用户。**