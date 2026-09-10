ok = AdvanceToNextPage()
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | bool | 跳转到下一页。值为 true 表示后续页面存在，值为 false 表示后续页面不存在。 |
# 描述
跳转到下一页
# 代码示例
该示例使用了Module相关功能，建议阅读[Module](https://vcreate.douyin.com/pet/wiki/s196aspp/xf4poi3d)相关文档。
**index.lua**
```Lua
GoldDataManager = require("DouyinDataScore/GoldDataManager")
--定义金币发生变化的事件，可在显示层监听该事件，在事件中更新UI。
OnGoldsChange = event("OnGoldsChange")
```

**GoldDataManager.lua**
金币数据管理器，封装了一些数据的存储和读取。
```Lua
local GoldDataManager = {}

local isInit = false
GoldDataManager.golds = 0
GoldDataManager.goldStore = nil
GoldDataManager.goldOrderedStore = nil

function GoldDataManager:InitGoldOrderedStore(callback)
    if self.goldOrderedStore ~= nil then
        return
    end
    local ok, store = DouyinDataService.GetOrderedDataStore("OrderedData", "GoldOrdered")
    if ok ~= 0 then
        print("---GoldDataManager:SetData Fail:" .. ok .. tostring(store))
        if callback then callback(false) end
        return
    end
    self.goldOrderedStore = store
end

function GoldDataManager:GetGoldSortedData(callback)
    DATASTORE(
        function()
            local page_size = 10
            self:InitGoldOrderedStore(callback)
            if self.goldOrderedStore == nil then
                return
            end
            local ok, pages = self.goldOrderedStore:GetSortedData(false, page_size)
            if ok ~= 0 then
                print("---GoldDataManager:GetSortedData Fail:" .. ok .. pages)
                if callback then callback(false) end
                return
            end
            local maxcount = 10
            local index = 0
            repeat
                index = index + 1
                if index > maxcount then
                    return
                end
                local success, page_values = pages:GetCurrentPage()
                if success == 0 then
                    for k, v in pairs(page_values) do
                        print("GoldDataManager:GoldRank_Key=" .. k .. "Value" .. v.value)
                        callback(true, k, v.value)
                    end
                end
            until not pages:AdvanceToNextPage()
        end
    )
end

return GoldDataManager
```

**GameManager.lua**
初始化金币数据。
```Lua
---@var GoldText:UnityEngine.UI.Text
---@end

local Input = UnityEngine.Input
local isInit = false
local onGoldsChangeListener

function OnPlayerJoined(player)
    if player.isLocal then
        GameInit()
    end
end

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--网络未准备好")
        return
    end
    if Input.GetKeyDown("0") then
        GoldDataManager:GetGoldSortedData(GoldDataManager:GetCoin(), function(success)
            if success then
                DouyinUtility.Toast("获取金币排序成功")
            else
                DouyinUtility.Toast("获取金币排序失败")
            end
        end)
    end
end

function Start()
    onGoldsChangeListener = OnGoldsChange:CreateListener(function(value)
        GoldText.text = value
    end)
    OnGoldsChange:AddListener(onGoldsChangeListener)
end

function GameInit()
    if isInit then
        return
    end
    GoldDataManager:LoadGoldData(function(success)
        if success then
            DouyinUtility.Toast("初始化金币数据成功")
        else
            DouyinUtility.Toast("初始化金币数据失败")
        end
    end)
    isInit = true
end

function OnDestroy()
    OnGoldsChange:RemoveListener(onGoldsChangeListener)
end
```

