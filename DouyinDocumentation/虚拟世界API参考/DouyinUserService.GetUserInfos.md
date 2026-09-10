public void GetUserInfos(List<string> playerOpenIDs, Action<List<DouyinUserInfo>> callback)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| playerOpenIDs | 玩家的openID列表 |
| callback | 回调函数，承载着获取到的用户信息列表 |
# 描述
通过openID列表获取抖音多个用户的信息，批量查询阈值。
# 代码示例
```Lua
---@var Btn_1:UnityEngine.UI.Button
---@var Btn_2:UnityEngine.UI.Button
---@end

function Start()
    Btn_2.onClick:AddListener(GetUserInfosSample)
end

function GetUserInfosSample()
    local openIDList = {}
    local players = DouyinPlayerService.GetPlayers()
    if players then
        for i = 0, players.Length - 1 do
            if players[i] then
                openIDList[i+1] = players[i].playerOpenID
            end
        end
    end
    DouyinUserService.GetUserInfos(openIDList,function (userInfoList)
        if userInfoList == nil or userInfoList.Count == 0 then
            DouyinUtility.Toast("用户信息列表为空")
            return
        end
        for i = 0, userInfoList.Count - 1 do
            print(string.format("---DouyinUserService:openID=%s__name=%s__portraitUrl=%s", userInfoList[i].openID,userInfoList[i].name,userInfoList[i].portraitUrl))
        end
    end)
end
```


