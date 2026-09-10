public static DouyinPlayer[] GetPlayers()
# 参数
无
# 返回
DouyinPlayer[]
包含房间内所有玩家的实例的数组，每个元素为DouyinPlayer实例
# 描述
获取当前房间内所有的DouyinPlayer
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("space") then
        GetPlayersSample()
    end
end

function GetPlayersSample()
    local players = DouyinPlayerService.GetPlayers()
    if players then
        for i = 0, players.Length - 1 do
            print("--GetPlayers:playerName=" .. players[i].playerName)
        end
    end
    return players
end
```


