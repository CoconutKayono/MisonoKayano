public bool SetOwner(DouyinPlayer player)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 将对象的主权所有者设置为player |
# 返回
bool
true：设置成功，
false：设置失败（没有主权）
# 描述
把该对象的主权转移给指定的 DouyinPlayer。只有主权者可以对对象进行操作。
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
        SetOwnerSample()
    end
end

function OnPlayerJoined(player, evt)
    if player and not player.isLocal then
        anotherPlayerID = player.playerID
        print("--DouyinNetSample:UID=" .. anotherPlayerID)
    end
end

function SetOwnerSample()
    local player = DouyinPlayerService.GetPlayer(anotherPlayerID)
    if not player then
        print("获取player失败" .. anotherPlayerID)
        return
    end
    local success = self:SetOwner(player)
    if success then
        print(string.format("--DouyinNetSample:SetOwner:设置%s成为主权方成功", player.playerOpenID))
    else
        print(string.format("--DouyinNetSample:SetOwner:设置%s成为主权方失败", player.playerOpenID))
    end
end
```


