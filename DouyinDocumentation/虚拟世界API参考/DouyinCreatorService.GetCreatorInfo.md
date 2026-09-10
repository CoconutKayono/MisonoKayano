public static void GetCreatorInfo(Action<CreatorInfo> callback)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| callback | 回调函数，承载着获取到的创作者信息CreatorInfo |
# 描述
用于获取创作者信息，调试器模式下获取不到创作者信息。
# 代码示例
```Lua
---@var Btn_1:UnityEngine.UI.Button
---@var Btn_2:UnityEngine.UI.Button
---@var Btn_3:UnityEngine.UI.Button
---@end

local secUID

function Start()
    Btn_1.onClick:AddListener(GetCreatorInfoSample)
end

function GetCreatorInfoSample()
    DouyinCreatorService.GetCreatorInfo(function (creatorInfo)
        DouyinUtility.Toast("获取创建者信息成功:"..creatorInfo.name)
        secUID = creatorInfo.secUID
    end)
end
```


