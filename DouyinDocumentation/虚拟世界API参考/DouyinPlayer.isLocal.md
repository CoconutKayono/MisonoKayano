public bool isLocal
# 描述
是否是本地玩家；true 表示本地玩家，false 表示房间内其他玩家。
# 代码示例

```Lua
-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
-- 注意:evt在Lua侧输出是:CreateRoom:0 JoinRoom:1 ReJoinRoom:2
function OnPlayerJoined(player, evt)
    IsLocalPlayerSample(player)
end
-- 玩家离开世界会触发OnPlayerLeft
-- player:DouyinPlayer 离开世界的玩家
-- evt:PlayerJoinEvent 玩家离开世界类型
-- 注意:evt在Lua侧输出是:Disconnect:0 ExitRoom:1
function OnPlayerLeft(player, evt)
    IsLocalPlayerSample(player)
end

function IsLocalPlayerSample(player)
    if not player then return end
    print("--DouyinPlayerSample--" .. "isLocal=" .. tostring(player.isLocal))
    return player.isLocal
end
```


