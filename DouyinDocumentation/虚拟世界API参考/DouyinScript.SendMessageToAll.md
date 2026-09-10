public void SendMessageToAll(string method, params object[] args)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| method | DouyinScript 的 Lua 文件中定义的函数名称 |
| args | 变量参数 |
# 描述
发送网络事件给所有人，包括自己。
* 使用SendMessageXXX发送消息时，是不能保证对方能接收到的，如果发送的消息，对方接收不到也不影响正常逻辑，则可以使用该方法。如果需要同步数据，可以使用同步变量的方式代替该方法。
* 在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--DouyinNetSample:网络未准备好")
        return
    end
    if Input.GetKeyDown("1") then
        SendMessageToAllSample()
    end
end

function SendMessageToAllSample()
    print("--DouyinNetSample:发送消息给所有玩家")
    self:SendMessageToAll("Method2", 2)
end

function Method2(index)
    print("--DouyinNetSample:收到SendMessageToAll消息" .. index)
end
```


