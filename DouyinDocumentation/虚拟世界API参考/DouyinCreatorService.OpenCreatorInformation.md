public static void OpenCreatorInformation(string secUid)
# 描述
用于打开创作者信息
# 代码示例
```Lua
---@var Btn_1:UnityEngine.UI.Button
---@var Btn_2:UnityEngine.UI.Button
---@var Btn_3:UnityEngine.UI.Button
---@end

local secUID

function Start()
    Btn_1.onClick:AddListener(GetCreatorInfoSample)
    Btn_3.onClick:AddListener(OpenCreatorInformationSample)
end

function GetCreatorInfoSample()
    DouyinCreatorService.GetCreatorInfo(function (creatorInfo)
        DouyinUtility.Toast("获取创建者信息成功:"..creatorInfo.name)
        secUID = creatorInfo.secUID
    end)
end

function OpenCreatorInformationSample()
    if secUID == nil then
        DouyinUtility.Toast("secUID is nil")
        return
    end
    DouyinCreatorService.OpenCreatorInformation(secUID)
    DouyinUtility.Toast("打开创作者信息")
end
```


