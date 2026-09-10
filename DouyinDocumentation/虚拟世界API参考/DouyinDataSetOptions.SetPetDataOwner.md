SetPetDataOwner(string ownerID)
# 描述
设置数据关联的火人（仅用于检测），平台侧即可检测到该火人因多房间同时写入而导致的数据回档异常。
# 参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| ownerID | string | 数据所有者的火人 petOpenID |
# 代码示例
```Lua
ServerDataStoreManager = {}
_G["ServerDataStoreManager"] = ServerDataStoreManager

local stores = {}

local function CheckParam(name)
    if not name or type(name) ~= "string" or name == "" then
        return false
    end
    return true
end

local function GetStoreKey(storeName, scopeName)
    return storeName..scopeName
end

local function GetDataStore(storeName, scopeName)
    local storeKey = GetStoreKey(storeName, scopeName)
    if stores[storeKey] then
        return stores[storeKey]
    end
    local ok, store = DouyinDataService.GetDataStore(storeName, scopeName);
    if ok ~= 0 then
        ServerUtils.Log("[Data] GetDataStore Failed: " .. ok.." storeName:"..storeName.." scopeName:"..scopeName);
        return nil
    end
    stores[storeKey] = store
    return store
end

function ServerDataStoreManager.SetData(storeName, scopeName, dataKey, dataValue, callback, petOpenID)
    if not CheckParam(storeName) or not CheckParam(scopeName) or not CheckParam(dataKey) then
        callback(false, "Invalid parameter", nil)
        return
    end

    DATASTORE(function()
        local store = GetDataStore(storeName, scopeName)
        if not store then
            callback(false, "Failed to get data store", nil)
            return;
        end
        local options = DouyinDataService.CreateDataSetOptions()
        options:SetPetDataOwner(petOpenID)
        local ok, value = store:SetData(dataKey, dataValue，options)
        if ok ~= 0 then
            callback(false, ok, value)
            return
        end
        callback(true, "Success", value)
    end)
end
```


