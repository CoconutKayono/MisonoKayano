# 重载1
public GameObject NetSpawn(string key,Vector3 position, out int id, Action<GameObject, int> onSpawn = null)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| position | 生成网络对象的位置 |
| id | 生成的网络对象的唯一标识符 |
| onSpawn | 回调函数，承载着创建出来的网络对象的GameObject和它的id |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成特定坐标位置的网络对象。
# 代码示例
```Lua
---@var bloodTextKeyname :string
---@var bloodTextY :float  = 1.5
---@end

local bloodView

function OnActorSpawned(actor)
    if not actor.isLocal then
        return
    else
        local targetPos = Vector3(actor.position.x, actor.position.y + bloodTextY, actor.position.z)
        actor:NetSpawn(bloodTextKeyname, targetPos, function(go, id)
            bloodView = go:GetDouyinScript("BloodView")
            bloodView.script.SetTargetActorId(actor.actorID)
        end)
    end
end
```

示例Demo如下：
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4615603d87f349e3875bce315986315d~tplv-goo7wpa0wc-image.image" filename="PlayerBloodController.lua" download>PlayerBloodController.lua</a>
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/2423bf7560f74f2f9b7e77589b83f19e~tplv-goo7wpa0wc-image.image" filename="BloodView.lua" download>BloodView.lua</a>
具体处理流程如下：
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ca763d288cf74bc9a660c1aec3a3e86e~tplv-goo7wpa0wc-image.image)
# 重载2
public GameObject NetSpawn(string key, out int id, Action<GameObject, int> onSpawn = null)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 通过 prefab 创建的网络对象的 prefab 资源名称 |
| id | 生成的网络对象的唯一标识符 |
| onSpawn | 回调函数，承载着创建出来的网络对象的GameObject和它的id |
## 返回
GameObject
生成的网络对象。
## 描述
动态生成网络对象。
# 代码示例
```Lua
---@var bloodTextKeyname :string
---@var bloodTextY :float  = 1.5
---@end

local bloodView
local Vector3 = UnityEngine.Vector3

function OnActorSpawned(actor)
    if not actor.isLocal then
        return
    else
        actor:NetSpawn(bloodTextKeyname, function(go, id)
            bloodView = go:GetDouyinScript("BloodView")
            bloodView.script.SetTargetActorId(actor.actorID)
        end)
    end
end
```

# 重载3
public GameObject NetSpawn(string key, Vector3 position, Vector3 rotation, out int id, Action<GameObject, int> onSpawn = null)
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
---@var bloodTextKeyname :string
---@var bloodTextY :float  = 1.5
---@end

local bloodView
local Vector3 = UnityEngine.Vector3

function OnActorSpawned(actor)
    if not actor.isLocal then
        return
    else
        local targetPos = Vector3(actor.position.x, actor.position.y + bloodTextY, actor.position.z)
        actor:NetSpawn(bloodTextKeyname, targetPos, Vector3(10, 0, 0),function(go, id)
            bloodView = go:GetDouyinScript("BloodView")
            bloodView.script.SetTargetActorId(actor.actorID)
        end)
    end
end
```

# 重载 4
public GameObject NetSpawn(string key, Vector3 position, Quaternion rotation, out int id, Action<GameObject, int> onSpawn = null)
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
---@var bloodTextKeyname :string
---@var bloodTextY :float  = 1.5
---@end

local bloodView
local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion

function OnActorSpawned(actor)
    if not actor.isLocal then
        return
    else
        local targetPos = Vector3(actor.position.x, actor.position.y + bloodTextY, actor.position.z)
        local targetRot = Quaternion.Euler(Vector3(10, 0, 0))
        actor:NetSpawn(bloodTextKeyname, targetPos, targetRot,function(go, id)
            bloodView = go:GetDouyinScript("BloodView")
            bloodView.script.SetTargetActorId(actor.actorID)
        end)
    end
end
```


