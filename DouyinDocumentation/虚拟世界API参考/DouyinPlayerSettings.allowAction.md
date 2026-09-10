public static bool allowAction
# 描述
是否允许合养精灵动作功能，默认设置true
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        AllowActionSample(true)
    elseif Input.GetKeyDown("1") then
        AllowActionSample(false)
    end
end

function AllowActionSample(isAllow)
    DouyinPlayerSettings.allowAction = isAllow
end
```


