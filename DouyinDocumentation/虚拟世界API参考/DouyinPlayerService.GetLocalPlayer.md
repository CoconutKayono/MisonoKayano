public static DouyinPlayer GetLocalPlayer()
# 参数
无。
# 返回
DouyinPlayer
当前本地玩家的实例化对象。
# 描述
获取本地玩家。
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("space") then
        GetLocalPlayerSample()
    end
end

function GetLocalPlayerSample()
    local player = DouyinPlayerService.GetLocalPlayer()
    if player then
        print("--GetLocalPlayer:playerName=" .. player.playerName)
    end
    return player
end
```


