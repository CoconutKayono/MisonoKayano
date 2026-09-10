opt = CreateDataSetOptions()
# 返回值
| 变量 | 类型 | 描述· |
| --- | --- | --- |
| opt | DouyinDataSetOptions | 返回新创建的DouyinDataSetOptions对象 |
# 描述
创建一个 DouyinDataSetOptions 对象
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

function GetMetadataFromInfo(info, callback)
    if info == nil then
        return
    end
    local format = "yyyy-MM-dd HH:mm:ss"
    local createdTime = info.createdTime:ToString(format)
    local updatedTime = info.updatedTime:ToString(format)
    local version = info.version
    print(string.format("---GoldDataManager:GetMetadataFromInfo_createdTime=%s_updatedTime=%s_version=%s", createdTime,
        updatedTime, version))
    local meta_data = info:GetMetadata()
    if meta_data then
        for k, v in pairs(meta_data) do
            print("---GoldDataManager:GetMetadataFromInfo=" .. k .. v)
            if callback then callback(k, v) end
        end
    end
end

function GoldDataManager:SaveGoldDataSample(endgolds, callback, metaTable)
    DATASTORE(
        function()
            self:InitGoldStore(callback)
            if self.goldStore == nil then
                return
            end
            local options = self:GetSetOptionsSample(metaTable)
            local ok, value, info = self.goldStore:SetData("Golds", endgolds, options)
            if ok ~= 0 then
                print("---GoldDataManager:SetData Fail:" .. ok .. value)
                if callback then callback(false) end
                return
            end
            GetMetadataFromInfo(info)
            self:GoldsChange(value)
            if callback then
                callback(true)
            end
        end
    )
end

function GoldDataManager:GetSetOptionsSample(metaTable)
    if self.goldStore == nil then
        return
    end
    local ok, value, info = self.goldStore:GetData("Golds")
    if ok ~= 0 then
        print("---GoldDataManager:GetData Fail:" .. ok .. value)
        return
    end
    local options = DouyinDataService.CreateDataSetOptions()
    GetMetadataFromInfo(info, function(k, v)
        options:SetMetadata(k, v)
    end)
    for k, v in pairs(metaTable) do
        options:SetMetadata(k, v)
    end


    local dict = options:GetMetadata()
    for k, v in pairs(dict) do
        print("---GoldDataManager:GetMetadata=" .. "Key:", k, "Value:", v)
    end
    return options
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

function Start()
    onGoldsChangeListener = OnGoldsChange:CreateListener(function(value)
        GoldText.text = value
    end)
    OnGoldsChange:AddListener(onGoldsChangeListener)
end

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--网络未准备好")
        return
    end
    if Input.GetKeyDown("0") then
        SetDataWithOptionsSample()
    end
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

function SetDataWithOptionsSample()
    local dt = DouyinUtility.GetServerTime()
    local key = dt:ToString()
    local value = GoldDataManager:GetCoin() + 1
    local metaTable = {}
    metaTable[key] = value
    GoldDataManager:SaveGoldDataSample(value, function(success)
        if success then
            DouyinUtility.Toast("设置元数据成功")
        else
            DouyinUtility.Toast("设置元数据失败")
        end
    end, metaTable)
end

function OnDestroy()
    OnGoldsChange:RemoveListener(onGoldsChangeListener)
end
```


