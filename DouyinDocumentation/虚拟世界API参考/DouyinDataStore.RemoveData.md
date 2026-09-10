ok, value, info = RemoveData(key)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| key | string | 要删除的数据的键 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为0，则操作成功。 |
| value | number,boolean,string，或包含这些类型的表 | 如果操作成功，则返回删除的值。否则，返回错误信息 |
| info  | DouyinDataInfo | 如果操作成功，则返回详细信息。 |
# 描述
删除数据
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

function GoldDataManager:DeleteRecord(callback)
    self:GoldsChange(0)
    DATASTORE(
        function()
            self:InitGoldStore(callback)
            if self.goldStore == nil then
                return
            end
            local ok, value, info = self.goldStore:RemoveData("Golds")
            if ok ~= 0 then
                print("---GoldDataManager:RemoveData Fail:" .. ok .. value)
                if callback then callback(false) end
                return
            end
            print("---GoldDataManager:RemoveData Success:" .. value .. "_" .. value)
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
        GoldDataManager:DeleteRecord(function(success)
            if success then
                DouyinUtility.Toast("删除用户金币数据成功")
            else
                DouyinUtility.Toast("删除用户金币数据失败")
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

