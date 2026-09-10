此小节将网络相关的 API 汇总介绍，方便大家查阅和学习。
# DouyinScript
| DouyinScript.HasOwnership | 判断自己是否拥有当前物体的主权 |
| --- | --- |
| DouyinScript.GetOwner | 直接获取主权方的玩家对象 |
| DouyinScript.IsOwner | 判断某个玩家是否是当前物体的主权方 |
| DouyinScript.RequestOwnership | 请求主权 |
| DouyinScript.SetOwner | 设置新的主权方，只有主权方可以调用 |
| DouyinScript.SendMessageToOwner | 向主权方发送消息 |
| DouyinScript.SendMessageToAll | 向所有人发送消息，包括自己 |
| DouyinScript.SendMessageToTarget | 向某个玩家发送消息 |
| DouyinScript.OwnerCall | 调用主权方的某个函数 |
| DouyinScript.TargetCall | 调用某个玩家的某个函数 |
| DouyinScript.OnNetSpawned | 网络对象生成时，所有人都会收到这个事件。   <br> 当要监听某个同步变量的变化时，可以在这个事件中处理。 |
| DouyinScript.OnOwnershipRequest | 收到主权被请求时，主权方会收到这个事件 |
| DouyinScript.OnOwnershipTransferred | 当主权被转移时，所有人都会收到这个事件 |
# DouyinNetService
| DouyinNetService.isNetisNetworkSettled | 房间的数据是否同步完成 |
| --- | --- |
| DouyinNetService.OnNetworkSettled | 当房间的数据同步完成时触发的事件，当要对客户端做初始化时，可以监听这个事件 |
# Synchronization Variable API（同步变量）
| SetValue | 设置同步变量的值 |
| --- | --- |
| GetValue | 获取同步变量的值 |
| OnValueChange | 当同步变量变化时，会触发这个事件 |

