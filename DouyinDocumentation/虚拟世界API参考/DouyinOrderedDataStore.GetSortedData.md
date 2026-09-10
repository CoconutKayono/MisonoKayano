ok, pages = GetSortedData(ascending, pagesize, minvalue = -1, maxvalue = -1)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| ascending | bool | 指定数据是否按升序排序。true 表示数据按升序排序，false 表示相反。 |
| pageSize | int | 单页上的数据条目数量，不能超过1024。 |
| minvalue | int | 查询范围的最小值（包含此值）。方法将返回所有值（value）大于或等于 `minValue` 的条目。如果省略或设为 `nil`，则从排行榜的起始位置开始查询。 |
| maxvalue | int | 查询范围的最大值（包含此值）。方法将返回所有值（value）小于或等于 `maxValue` 的条目。如果省略或设为 `nil`，则查询至排行榜的末尾位置。 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int  | 如果值为0，则操作成功。后续字段为获取的值和详细信息。 |
| pages  | string/DataStorePage | 如果操作成功，则以分页模式返回获取的信息。否则，返回错误消息。 |
# 描述
从 DataStore 中获取所有按值排序的数据集。
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

-- 初始化金币排行榜（从大到小：保留较大值）
function GoldDataManager:InitGoldOrderedStore(callback)
    if self.goldOrderedStore ~= nil then
        return
    end
    -- asc=false：保留较大值，适用于"金币 Top 榜"
    local ok, store = DouyinDataService.GetOrderedDataStore("OrderedData", "GoldOrdered", false)
    if ok ~= 0 then
        print("---GoldDataManager:SetData Fail:" .. ok .. tostring(store))
        if callback then callback(false) end
        return
    end
    self.goldOrderedStore = store
end

-- 获取金币排行榜（从大到小）
function GoldDataManager:GetGoldSortedData(callback)
    DATASTORE(
        function()
            local page_size = 10
            self:InitGoldOrderedStore(callback)
            if self.goldOrderedStore == nil then
                return
            end
            -- ascending=false：按值从大到小获取
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

