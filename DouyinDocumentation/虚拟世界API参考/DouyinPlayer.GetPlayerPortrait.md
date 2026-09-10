public void GetPlayerPortrait(Action<Sprite> callback)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| callback | 回调函数，承载着获取到的 Sprite 类型的头像数据 |
# 描述
获取玩家的抖音头像。
注意：本地调试阶段无法获取到玩家的抖音头像，在扫码测试阶段可以获取到，你可以先将世界上传，然后使用手机进行扫码调试。
# 代码示例
```Lua
---@var portraitImg:UnityEngine.UI.Image
---@end

-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
-- 注意:evt在Lua侧输出是:CreateRoom:0 JoinRoom:1 ReJoinRoom:2
function OnPlayerJoined(player, evt)
    GetPlayerPortraitSample(player)
end

function GetPlayerPortraitSample(player)
    if not player then return end
    print("开始加载头像")
    player:GetPlayerPortrait(function(portrait)
        if portrait then
            portraitImg.sprite = portrait
            print("头像加载完成")
        else
            print("portrait is nil")
        end
    end)
end
```


