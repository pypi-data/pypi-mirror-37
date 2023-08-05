## applehttp2push
```
一个基于python2和http2的苹果推送SDK，基于yubang的修改。增加文件验证密码
```

### install
```
pip install applehttp2push

```

### use
```
from applehttp2push import AppleHttp2Push

apns = AppleHttp2Push('证书路径', 'bundle ID', '证书密码', '是否生产环境')
res = apns.push('苹果设备token', "推送内容")

```