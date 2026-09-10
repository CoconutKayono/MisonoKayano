public void TargetCall(string method, DouyinPlayer target, LuaFunction onFinish, params object[] args)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| method | DouyinScript 的 Lua 文件中定义的函数名称 |
| target | 接收调用的目标玩家 |
| onFinish | 远程调用完成时的回调通知 |
| args | 可变参数 |
# 描述
调用任意人的函数。
* 使用该方法发送消息，是不能保证对方能接收到的，且对方接收到，回调函数onFinish也不一定能执行。当执行回调函数onFinish时，该消息确实发送成功了，但是没有执行回调，对方可能也收到消息了。所以使用该方法通知对方执行逻辑时，拥有一定的不确定性。建议使用同步变量的方式代替该方法。
* 在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
```Lua
local Input = UnityEngine.Input
local anotherPlayerID

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--DouyinNetSample:网络未准备好")
        return
    end
    if Input.GetKeyDown("1") then
        TargetCallSample()
    end
end

function OnPlayerJoined(player, evt)
    if player and not player.isLocal then
        anotherPlayerID = player.playerID
        print("--DouyinNetSample:UID=" .. anotherPlayerID)
    end
end

function TargetCallSample()
    print("--DouyinNetSample:调用某个玩家的某个函数")
    local player = DouyinPlayerService.GetPlayer(anotherPlayerID)
    if not player then
        print("获取player失败" .. anotherPlayerID)
        return
    end
    self:TargetCall("Method6", player, function()
        print(string.format("--DouyinNetSample:调用%s的Method6成功", player.playerOpenID))
    end, 6)
end

function Method6(index)
    print("--DouyinNetSample:收到TargetCall消息" .. index)
end
```


