ok, value, info = UpdateData(key, updateFunction)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| key | string | 要更新的数据的键 |
| updateFunction | function | 用于更新数据的函数 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为0，则操作成功。 |
| value | number | 如果操作成功，则返回更新后的值。否则，返回错误消息。 |
| info | DouyinOrderedDataInfo | 如果操作成功，则返回详细信息（例如版本和元数据） |
# 描述
使用函数更新数据。
通过回调函数更新与键对应的数据。回调函数获取当前值，并根据定义的逻辑返回新值。回调函数一旦执行就不能暂停。
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

function GoldDataManager:UpdateGoldOrdered(addNum, callback)
    if not addNum then
        return
    end
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
            if addNum < 0 and math.abs(addNum) > self.golds then
                print("---GoldDataManager:金币不足")
                if callback then callback(false) end
                return
            end
            local ok, value, info = self.goldOrderedStore:UpdateData(player.playerOpenID, function(curVal, info)
                return curVal + addNum
            end)
            if ok ~= 0 then
                print("---GoldDataManager:UpdateGoldOrdered Fail:" .. ok .. value)
                if callback then callback(false) end
                return
            end
            print("---GoldDataManager:UpdateGoldOrdered Success:" .. ok .. value)
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

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--网络未准备好")
        return
    end
    if Input.GetKeyDown("0") then
        GoldDataManager:UpdateGoldOrdered(GoldDataManager:GetCoin(), function(success)
            if success then
                DouyinUtility.Toast("保存金币排序数据成功")
            else
                DouyinUtility.Toast("保存金币排序数据失败")
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

