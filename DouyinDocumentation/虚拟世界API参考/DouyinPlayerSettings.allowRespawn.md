public static bool allowRespawn
# 描述
启用/禁用重置出生点，默认设置true
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        AllowRespawnSample(true)
    elseif Input.GetKeyDown("1") then
        AllowRespawnSample(false)
    end
end

function AllowRespawnSample(isAllow)
    DouyinPlayerSettings.allowRespawn = isAllow
end
```


