public static bool allowActorChange
# 描述
是否允许切换合养精灵形象，设置为false后，世界内所有涉及切换合养精灵形象的入口会被禁用，默认为true。
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        AllowActorChangeSample(true)
    elseif Input.GetKeyDown("1") then
        AllowActorChangeSample(false)
    end
end

function AllowActorChangeSample(isAllow)
    DouyinPlayerSettings.allowActorChange = isAllow
end
```


