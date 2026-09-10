public bool SetController(DouyinPlayer player)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 将物体的控制者设置为 player |
# 返回
bool
true：设置成功，
false：设置失败。
# 描述
设置物体的控制者。
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
        SetControllerSample()
    end
end

function OnPlayerJoined(player, evt)
    if player and not player.isLocal then
        anotherPlayerID = player.playerID
        print("--DouyinNetSample:UID=" .. anotherPlayerID)
    end
end

function SetControllerSample()
    local player = DouyinPlayerService.GetPlayer(anotherPlayerID)
    if not player then
        print("获取player失败" .. anotherPlayerID)
        return
    end
    self:SetController(player, function(success)
        if success then
            print(string.format("--DouyinNetSample:SetController:设置%s成为控制方成功", player.playerOpenID))
        else
            print(string.format("--DouyinNetSample:SetController:设置%s成为控制方失败", player.playerOpenID))
        end
    end)
end
```


