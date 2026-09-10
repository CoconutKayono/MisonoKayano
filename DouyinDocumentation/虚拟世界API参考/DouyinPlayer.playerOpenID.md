public string playerOpenID
# 描述
房间内玩家的抖音开放ID，玩家ID的唯一标识
# 代码示例
```Lua
-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
-- 注意:evt在Lua侧输出是:CreateRoom:0 JoinRoom:1 ReJoinRoom:2
function OnPlayerJoined(player, evt)
    GetPlayerOpenIDSample(player)
end
-- 玩家离开世界会触发OnPlayerLeft
-- player:DouyinPlayer 离开世界的玩家
-- evt:PlayerJoinEvent 玩家离开世界类型
-- 注意:evt在Lua侧输出是:Disconnect:0 ExitRoom:1
function OnPlayerLeft(player, evt)
    GetPlayerOpenIDSample(player)
end

function GetPlayerOpenIDSample(player)
    if not player then return end
    print("--DouyinPlayerSample--" .. "PlayerOpenID=" .. player.playerOpenID)
end
```


