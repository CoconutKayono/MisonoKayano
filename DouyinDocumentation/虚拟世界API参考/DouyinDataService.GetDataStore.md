ok, store = GetDataStore(name,scope = “global”,all_scope = false)
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| name  | string | 数据存储的名称，这是一个唯一标识符。具有相同名称的数据存储中的数据将保存在同一数据空间中。 |
| scope | string | 数据存储的域名，其中数据根据范围独立存储。如果将 all_scope 设置为 false，数据存储中的所有数据键默认都会带有范围前缀。否则，您需要在数据键中指定范围。 |
| all_scope | bool | 指定所获取的数据存储是否可以跨范围访问域中的所有数据。如果值为 true，您需要在数据键中指定范围，例如，使用 scope:key 格式访问数据。 |
# 返回值
| 变量 | 类型 | 描述 |
| --- | --- | --- |
| ok | int | 如果值为 0，则操作成功。后续字段为获取到的数据存储。 |
| store | string 或 DouyinDataStore | 如果操作成功，则返回获取到的 DouyinDataStore。否则，返回错误信息。 |
# 描述
创建或获取数据存储对象。
数据以键值格式存储，值可以是任何数据类型，如数字、字符串、布尔值或表格。此外，支持跨范围搜索和前缀搜索。
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

