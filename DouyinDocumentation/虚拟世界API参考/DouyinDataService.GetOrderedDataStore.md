ok, store = GetOrderedDataStore(name,scope = “global”，asc)
# 参数 
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| name  | string | 数据存储的名称，这是一个唯一标识符。具有相同名称的数据存储中的数据将保存在同一数据空间中。 |
| scope | string | 数据存储的域名，其中数据根据范围独立存储。如果将 all_scope 设置为 false，数据存储中的所有数据键默认都会带有范围前缀。 |
| asc | bool | * 不设置（默认）：超过 5000 条上限后写入直接失败。 <br> * true：保留较小值，超过上限时淘汰 value 最大的条目 <br> * false：保留较大值，超过上限时淘汰 value 最小的条目 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为 0，则操作成功。后续字段为获取到的数据存储。 |
| store | string 或 DouyinDataStore | 如果操作成功，则返回获取到的 DouyinDataStore。否则，返回错误信息。 |
# 描述
获取一个可排序的数据存储对象。数据以键值格式存储，值只能是数字。
新增参数asc，可开启自动淘汰，默认关闭。开启自动淘汰后，无需在客户端编写"先删再写"的淘汰逻辑，也避免并发下的竞态问题。
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

function GoldDataManager:GetGoldOrdered(callback)
    DATASTORE(
        function()
            local player = DouyinPlayerService.GetLocalPlayer()
            if not player then
                print("---GoldDataManager:player is nil")
                return
            end
            self:InitGoldOrderedStore(callback)
            if self.goldOrderedStore == nil then
                return
            end
            local ok, value = self.goldOrderedStore:GetData(player.playerOpenID)
            if ok ~= 0 then
                print("---GoldDataManager:GetGoldOrdered Fail:" .. ok .. value)
                if callback then callback(false) end
                return
            end
            print("---GoldDataManager:GetGoldOrdered Success:" .. value)
            if callback then
                callback(true)
            end
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

