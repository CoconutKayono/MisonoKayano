# 描述
`DouyinRemoteFunction` 对象用于在客户端与服务器之间进行双向通信。您可以为 `DouyinRemoteFunction.onClientInvoke` 或 `DouyinRemoteFunction.onServerInvoke` 事件设置回调函数，来处理来自另一方的调用请求。
# 公开事件
| [onClientInvoke](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7topqqtk) | 客户端的事件：服务器调用客户端，客户端需要侦听该事件，处理业务逻辑并返回结果 |
| --- | --- |
| [onServerInvoke](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ygidu33o) | 服务端的事件：客户端调用服务器，服务器需要侦听该事件，处理业务逻辑并返回结果 |
# 公开方法
| [InvokeServer](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=isk0181a) | 客户端调用服务器，并处理服务器的响应 |
| --- | --- |
| [InvokeClient](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bdo5l1pb) | 服务器调用指定的客户端， 并处理客户端响应 |

