ok,value,info = GetData(key)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| key | string | 要获取的数据的键 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为0，则操作成功。后续字段为获取的值和详细信息 |
| value | number,boolean,string，或包含这些类型的表 | 如果操作成功，则返回获取的值。否则，返回错误信息 |
| info  | DouyinDataInfo | 如果操作成功，则返回详细信息 |
# 描述
获取存储数据
每个DataStore实例的键值对存储设计**容量上限为1000个**独立键值（key）单元，当单个DataStore实例存储的键数量达到1000个时，系统将自动触发写入保护机制，后续所有**新增键值的操作将返回错误**。**已存在键的更新操作不受此限制影响**。很多开发者喜欢以playerOpenID或petOpenID作为key，存储玩家数据，但是当用户超过1000人，就会出现存储失败的情况。正确做法是使用playerOpenID或petOpenID作为scope，在GetData()和SetData()时，使用相同的Key。


* 错误示范：使用pet.petOpenID作为key，当用户数量突破1000，会导致数据处理延迟

```Lua
local ok, ScoreBeanData= DouyinDataService.GetDataStore("Common", "ScoreBeanData")
ScoreBeanData:SetData(pet.petOpenID,progress)
```


* 正确示范：使用"progress"作为key，以pet.petOpenID作为scope。所有的key都是一样的，不会出现key值超过1000的情况。

```Lua
local ok, ScoreBeanData= DouyinDataService.GetDataStore("Common", pet.petOpenID.."ScoreBeanData")
ScoreBeanData:SetData("progress",progress)
```

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


