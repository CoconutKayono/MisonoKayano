public void SetOwnership(int targetActorNr, Action<bool> onFinished)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| targetActorNr | 这里是一个 int，表示目标 Actor 的 ID |
| onFinished | 请求完成时的回调通知，如果回调函数中的布尔参数为 true，则请求成功 |
# 描述
把该对象的主权转移给指定的 Actor。只有该对象的**主权方**可以调用，非主权方调用会失败。
在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

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
        SetOwnershipSample()
    end
end

function OnPlayerJoined(player, evt)
    if player and not player.isLocal then
        anotherPlayerID = player.playerID
        print("--DouyinNetSample:UID=" .. anotherPlayerID)
    end
end

function SetOwnershipSample()
    local actor = DouyinActorService.GetActorById(anotherActorID)
    if not actor then return end
    self:SetOwnership(actor.actorID, function(success)
        if success then
            print(string.format("--DouyinNetSample:SetOwnership:设置%s成为主权方成功", actor.actorID))
        else
            print(string.format("--DouyinNetSample:SetOwnership:设置%s成为主权方失败", actor.actorID))
        end
    end)
end
```


