# 重载 1
public static GameObject NetSpawn(string key, out int id)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| id | 生成的网络对象的唯一标识符 |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成网络对象。
# 代码示例
```Lua
local Input = UnityEngine.Input

local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion

-- Start is called before the first frame update
function Start()
end

function Update()
    if Input.GetKeyDown("1") then
        NetSpawnSample1()
    end
end

function NetSpawnSample1()
    local netObj, netid = DouyinObjectService.NetSpawn("NetObject_1", function(obj, id)
        if obj and id then
            print("--DouyinObjectServiceCallBack1:name=" .. obj.name .. "id=" .. id)
        end
    end)
    if netObj and netid then
        print("--DouyinObjectService1:name=" .. netObj.name .. "id=" .. netid)
    end
end
```

# 重载 2
public static GameObject NetSpawn(string key,Vector3 position, out int id)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| position | 指定要生成的网络对象的坐标 |
| id | 生成的网络对象的唯一标识符 |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成特定坐标位置的网络对象。
# 代码示例
```Lua
local Input = UnityEngine.Input

local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion

-- Start is called before the first frame update
function Start()
end

function Update()
    if Input.GetKeyDown("1") then
        NetSpawnSample2()
    end
end

function NetSpawnSample2()
    local netObj, netid = DouyinObjectService.NetSpawn("NetObject_1", Vector3(1, 1, 1),
    function(obj, id)
            if obj and id then
                print("--DouyinObjectServiceCallBack2:name=" .. obj.name .. "id=" .. id)
            end
        end)
    if netObj and netid then
        print("--DouyinObjectService2:name=" .. netObj.name .. "id=" .. netid)
    end
end
```

# 重载 3
public static GameObject NetSpawn(string key, Vector3 position, Vector3 rotation, out int id)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| position | 指定要生成的网络对象的坐标 |
| rotation | 指定要生成的网络对象的旋转 |
| id | 生成的网络对象的唯一标识符 |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成特定坐标位置，特定旋转的网络对象。
```Lua
local Input = UnityEngine.Input

local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion

-- Start is called before the first frame update
function Start()
end

function Update()
    if Input.GetKeyDown("1") then
        NetSpawnSample3()
    end
end

function NetSpawnSample3()
    local netObj, netid = DouyinObjectService.NetSpawn("NetObject_1", Vector3(1, 1, 1), Vector3(45, 45, 45),
        function(obj, id)
            if obj and id then
                print("--DouyinObjectServiceCallBack3:name=" .. obj.name .. "id=" .. id)
            end
        end)
    if netObj and netid then
        print("--DouyinObjectService3:name=" .. netObj.name .. "id=" .. netid)
    end
end
```

# 重载 4
public static GameObject NetSpawn(string key, Vector3 position, Quaternion rotation, out int id)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| position | 指定要生成的网络对象的坐标 |
| rotation | 指定要生成的网络对象的旋转 |
| id | 生成的网络对象的唯一标识符 |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成特定坐标位置，特定旋转的网络对象。
# 代码示例
```Lua
local Input = UnityEngine.Input

local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion

-- Start is called before the first frame update
function Start()
end

function Update()
    if Input.GetKeyDown("1") then
        NetSpawnSample4()
    end
end

function NetSpawnSample4()
    local targetRot = Quaternion.Euler(Vector3(45, 45, 45))
    local netObj, netid = DouyinObjectService.NetSpawn("NetObject_1", Vector3(2, 1, 2), targetRot,
        function(obj, id)
            if obj and id then
                print("--DouyinObjectServiceCallBack4:name=" .. obj.name .. "id=" .. id)
            end
        end)
    if netObj and netid then
        print("--DouyinObjectService4:name=" .. netObj.name .. "id=" .. netid)
    end
end
```


