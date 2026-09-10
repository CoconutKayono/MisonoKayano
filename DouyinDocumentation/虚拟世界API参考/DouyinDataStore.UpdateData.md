ok, ret_value, info = UpdateData(key, updateFunction)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| key | string | 要更新数据的键 |
| updateFunction | updateFunction(currentValue, DouyinDataInfo info) <br> {return newValue, new_options} | 用于更新数据的函数。 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为0，则操作成功。后续字段为更新后的值和详细信息。 |
| ret_value | number,boolean,string，或包含这些类型的表 | 如果操作成功，则返回更新后的值。否则，返回错误信息 |
| info  | DouyinDataInfo | 如果操作成功，则返回详细信息。 |
# 描述
通过回调函数更新与键对应的数据。回调函数获取当前值，并根据定义的逻辑返回新值。回调函数一旦执行便不能暂停。
未查询到该键对应的值，会返回错误码-10001

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

function GoldDataManager:InitGoldStore(callback)
    if self.goldStore ~= nil then
        return
    end
    local player = DouyinPlayerService.GetLocalPlayer()
    if not player then
        print("---GoldDataManager:player is nil")
        if callback then callback(false) end
        return
    end

    local ok, store = DouyinDataService.GetDataStore("playerData", "GoldData" .. player.playerOpenID)
    if ok ~= 0 then
        print("---GoldDataManager:GetDataSotre Fail:" .. ok .. tostring(store))
        if callback then callback(false) end
        return
    end
    self.goldStore = store
end

function GoldDataManager:LoadGoldData(callback)
    DATASTORE(
        function()
            if isInit then
                return
            end
            self:InitGoldStore(callback)
            if self.goldStore == nil then
                return
            end
            local ok, value, info = self.goldStore:GetData("Golds")
            if ok ~= 0 then
                print("---GoldDataManager:GetData Fail:" .. ok .. value)
                return
            end
            self:GoldsChange(value)
            isInit = true
            if callback then
                callback(true)
            end
        end
    )
end

function GoldDataManager:UpdateGoldData(addNum, callback)
    if not addNum then
        return
    end
    DATASTORE(
        function()
            self:InitGoldStore(callback)
            if self.goldStore == nil then
                return
            end
            if addNum < 0 and math.abs(addNum) > self.golds then
                print("---GoldDataManager:金币不足")
                if callback then callback(false) end
                return
            end
            local ok, value, info = self.goldStore:UpdateData("Golds", function(curVal, info)
                return curVal + addNum
            end)
            if ok ~= 0 then
                --没有这条数据
                if ok == -10001 then
                    ok, value, info = self.goldStore:SetData("Golds", self.golds + addNum)
                    if ok ~= 0 then
                        print("---GoldDataManager:SetData Fail:" .. ok .. value)
                        if callback then callback(false) end
                        return
                    end
                else
                    print("---GoldDataManager:UpdateData Fail:" .. ok .. value)
                    if callback then callback(false) end
                    return
                end
            end
            self:GoldsChange(value)
            if callback then
                callback(true)
            end
        end
    )
end

function GoldDataManager:GoldsChange(value)
    self.golds = value
    OnGoldsChange(self.golds)
end

function GoldDataManager:AddCoinByUpdateData(goldNum, callback)
    if not goldNum then
        return
    end
    self:UpdateGoldData(goldNum, callback)
end

function GoldDataManager:ReduceCoinByUpdateData(goldNum, callback)
    if not goldNum then
        return
    end
    self:UpdateGoldData(goldNum, callback)
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
        GoldDataManager:AddCoinByUpdateData(1, function(success)
            if success then
                DouyinUtility.Toast("金币+1")
            else
                DouyinUtility.Toast("增加金币失败")
            end
        end)
    elseif Input.GetKeyDown("1") then
        GoldDataManager:ReduceCoinByUpdateData(-1, function(success)
            if success then
                DouyinUtility.Toast("金币-1")
            else
                DouyinUtility.Toast("减少金币失败")
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

