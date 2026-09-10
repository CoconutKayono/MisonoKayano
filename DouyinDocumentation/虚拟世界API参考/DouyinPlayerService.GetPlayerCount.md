public static int GetPlayerCount()
# 参数
无
# 返回
int
返回一个整数，表示当前房间内的DouyinPlayer数量
# 描述
获取当前房间DouyinPlayer的数量
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("space") then
        GetPlayerCountSample()
    end
end

function GetPlayerCountSample()
    local count = DouyinPlayerService.GetPlayerCount()
    print("--GetPlayerCount=" .. count)
    return count
end
```


