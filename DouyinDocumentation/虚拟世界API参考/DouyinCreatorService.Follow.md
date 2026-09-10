public static void Follow(string secUid, Action<bool> callback)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| secUid | 创作者的SecUID |
| callback | 回调函数，成功时回调函数传入的参数为true，失败时回调函数传入的参数为false |
# 描述
用于关注创作者
# 代码示例
```Lua
---@var Btn_1:UnityEngine.UI.Button
---@var Btn_2:UnityEngine.UI.Button
---@var Btn_3:UnityEngine.UI.Button
---@end

local secUID

function Start()
    Btn_1.onClick:AddListener(GetCreatorInfoSample)
    Btn_2.onClick:AddListener(FollowCreatorSample)
end

function GetCreatorInfoSample()
    DouyinCreatorService.GetCreatorInfo(function (creatorInfo)
        DouyinUtility.Toast("获取创建者信息成功:"..creatorInfo.name)
        secUID = creatorInfo.secUID
    end)
end

function FollowCreatorSample()
    if secUID == nil then
        DouyinUtility.Toast("secUID is nil")
        return
    end
    DouyinCreatorService.Follow(secUID,function (success)
        if success then
            DouyinUtility.Toast("关注创作者成功:"..secUID)
        else
            DouyinUtility.Toast("关注创作者失败:"..secUID)
        end
    end)
end
```


