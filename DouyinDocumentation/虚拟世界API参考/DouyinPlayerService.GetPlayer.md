public static DouyinPlayer GetPlayer(int playerID)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| playerID | 目标玩家的唯一标识符 |
# 返回
DouyinPlayer
与playerId对应的玩家对象实例
# 描述
通过playerID，获取指定DouyinPlayer
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("space") then
        local player = GetLocalPlayerSample()
        if player then
            GetPlayerSample(player.playerID)
        end
    end
end

function GetPlayerSample(playerID)
    local player = DouyinPlayerService.GetPlayer(playerID)
    if player then
        print("--GetPlayer:playerName=" .. player.playerName)
    end
    return player
end
```


