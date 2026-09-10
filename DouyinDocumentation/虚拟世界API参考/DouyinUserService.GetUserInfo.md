public void GetUserInfo(string playerOpenID, Action<DouyinUserInfo> callback)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| playerOpenID | 玩家的openID，可以通过DouyinPlayer.playerOpenID获取 |
| callback | 回调函数，承载着获取到的用户信息DouyinUserInfo |
# 描述
通过openID获取抖音用户的信息。
# 代码示例
```Lua
---@var Btn_1:UnityEngine.UI.Button
---@var Btn_2:UnityEngine.UI.Button
---@end

function Start()
    Btn_1.onClick:AddListener(GetUserInfoSample)
end

function GetUserInfoSample()
    local player = DouyinPlayerService.GetLocalPlayer()
    if player then
        DouyinUserService.GetUserInfo(player.playerOpenID,function (userInfo)
            if userInfo then
                DouyinUtility.Toast(string.format("openID=%s__name=%s__portraitUrl=%s", userInfo.openID,userInfo.name,userInfo.portraitUrl))
                print(string.format("---DouyinUserService:openID=%s__name=%s__portraitUrl=%s", userInfo.openID,userInfo.name,userInfo.portraitUrl))
            else
                DouyinUtility.Toast("GetUserInfo Fail")
                print("---DouyinUserService:userInfo is nil playerOpenID="..player.playerOpenID)
            end
        end)
    end
end
```


