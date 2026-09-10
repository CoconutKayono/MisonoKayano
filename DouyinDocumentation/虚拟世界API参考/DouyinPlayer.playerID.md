public int playerID
# 描述
房间内玩家实例 ID，每次进房都会重新生成，客户端可以用该 ID 来标识玩家。
# 代码示例

```Lua
-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
function OnPlayerJoined(player, evt)
    GetPlayerIDSample(player)
end
-- 玩家离开世界会触发OnPlayerLeft
-- player:DouyinPlayer 离开世界的玩家
-- evt:PlayerJoinEvent 玩家离开世界类型
function OnPlayerLeft(player, evt)
    GetPlayerIDSample(player)
end

function GetPlayerIDSample(player)
    if not player then return end
    print("--DouyinPlayerSample--" .. "PlayerID=" .. player.playerID)
end
```


