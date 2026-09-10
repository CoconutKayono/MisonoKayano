public static bool allowEmotion
# 描述
是否允许使用合养精灵表情功能，默认设置true
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        AllowEmotionSample(true)
    elseif Input.GetKeyDown("1") then
        AllowEmotionSample(false)
    end
end

function AllowEmotionSample(isAllow)
    DouyinPlayerSettings.allowEmotion = isAllow
end
```


