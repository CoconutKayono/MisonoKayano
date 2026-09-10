# 描述
`DouyinRemoteEvent` 对象用于在客户端与服务器之间进行异步单向通信，调用方无需等待响应。
它支持以下几种通信方式：

* 从客户端发送至服务器
* 从服务器发送至单个客户端
* 从服务器广播至所有客户端

# 公开事件
| [onClientEvent](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=zke5fwhl) | 客户端的事件：服务器调用客户端，客户端需要侦听该事件，并处理业务逻辑 |
| --- | --- |
| [onServerEvent](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=b9577h7s) | 服务端的事件：客户端调用服务器，服务器需要侦听该事件，并处理业务逻辑 |
# 公开方法
| [FireClient](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=sv2ds9g6) | 服务器调用指定的客户端 |
| --- | --- |
| [FireAllClients](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wpgn0mnn) | 服务器广播给所有的客户端 |
| [FireServer](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=zymjqwep) | 客户端调用服务器 |

