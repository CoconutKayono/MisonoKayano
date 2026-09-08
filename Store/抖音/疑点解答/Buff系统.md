# Buff 系统

本文档说明模板项目中的 Buff 系统，包括系统的作用、使用场景、目录结构、同步方式、生命周期和扩展方法。

> 本文档依据 `D:/Work Env/Projects/Hot Dance DS Alpha/Assets/DSTemplate` 中的实现整理。当前 `Hot Dance Only SDK` 项目中的 Buff 目录只有基础设施；如果在该项目中使用完整 Buff 能力，需要同步接入模板中的 Client、Server 和 Buff 网络对象资源。

## 目录

1. [Buff 系统是什么？](#1-buff-系统是什么)
2. [为什么要使用 Buff 系统？](#2-为什么要使用-buff-系统)
3. [如何使用 Buff 系统？](#3-如何使用-buff-系统)
4. [常见问题与限制](#4-常见问题与限制)

## 1、Buff 系统是什么？

### 1.1 基本概念

Buff 是附加在 Actor 上的一种状态或效果。例如：

- 悬浮、游泳、坐下、牵手等角色状态；
- 加速、禁止移动等临时效果；
- 飞行器、飞行伙伴等角色外观和玩法扩展；
- 进入关卡、注册远程玩家等流程状态。

Buff 系统把这些状态统一抽象为“添加、更新、移除”三个动作，并为每个 Buff 提供标准生命周期回调。业务代码只需要调用统一接口，不需要自行维护每个状态的同步、过期和清理逻辑。

### 1.2 系统组成

完整实现由以下部分组成：

| 模块             | 位置                                                                                                                               | 职责                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Buff 类型定义      | `Assets/DSTemplate/Scripts/Client/System/BuffSystem/BuffDefine.lua`、`Assets/DSTemplate/Scripts/Server/Logic/Buff/BuffDefine.lua` | 定义 `BuffType`，将 Buff 映射到具体类型            |
| Buff 配置        | `Assets/DSTemplate/Scripts/Client/System/BuffSystem/BuffConfig.lua`、`Assets/DSTemplate/Scripts/Server/Logic/Buff/BuffConfig.lua` | 定义 Buff ID、互斥组、优先级、持续时间和默认数据            |
| Client Buff 基类 | `Assets/DSTemplate/Scripts/Client/System/BuffSystem/Buff/Buff_Base.lua`                                                          | 处理客户端 Buff 实例的生命周期、过期和主权判断              |
| Server Buff 基类 | `Assets/DSTemplate/Scripts/Server/Logic/Buff/ServerBuffBase.lua`                                                                 | 提供服务端独立的 Buff 基类，避免依赖客户端模块              |
| 网络 Buff 对象     | `Assets/DSTemplate/Scripts/Client/System/BuffSystem/NetworkBuff.lua`                                                             | 保存并同步一个 Actor 的 Buff 列表                 |
| 网络 Buff 管理器    | `Assets/DSTemplate/Scripts/Client/System/BuffSystem/NetworkBuffManager.lua`                                                      | 为业务层提供增删改查接口，并管理 Actor 与网络 Buff 对象的对应关系 |
| 网络资源           | `Assets/DSTemplate/Prefabs/Buff/NetworkBuff.prefab`                                                                              | 作为每个 Actor 的 Buff 同步载体                  |
| 具体 Buff 类      | `.../Client/System/BuffSystem/Buff`、`.../Server/Logic/Buff`                                                                      | 在 `OnAdd`、`OnUpdate`、`OnRemove` 中实现具体效果 |

### 1.3 Client 和 Server 的职责

Buff 代码分散在 Client 和 Server，并不是重复实现同一份逻辑，而是分别承担不同职责：

| 运行端 | 主要职责 |
| --- | --- |
| Client | 维护网络 Buff 对象的本地表现；生成、销毁模型和特效；修改本地 Actor 的移动、动画、镜头等客户端效果；通过主权机制发起同步修改 |
| Server | 加载与客户端一致的 Buff 类型和配置；执行需要在 DS 侧完成的逻辑，例如玩法倍率、服务端状态和服务器侧对象处理；提供不依赖客户端 `Buff_Base` 的 `ServerBuffBase` |

网络数据本身存储在 `NetworkBuff` 的同步变量中：

```lua
---@varSync syncActorID:int=0
---@varSync syncBuffID:int=0
---@varSync syncBuffDic:Dictionary<long, string>
```

其中：

- `syncActorID`：当前网络 Buff 对象绑定的 Actor ID；
- `syncBuffID`：用于生成实例 ID 的递增序号；
- `syncBuffDic`：Buff 实例字典，key 是唯一 Buff 实例 ID，value 是 JSON 字符串。

每个字典值的结构如下：

```lua
{
    expiredTime = 1730000000,
    extData = {
        -- 当前 Buff 的业务扩展数据
    }
}
```

`syncBuffDic` 会随着网络同步自动触发客户端的 `OnBuffChange`。客户端根据 Buff 配置中的 `Type` 找到具体类，创建 Buff 实例，然后调用 `OnAdd`；字典值变化时调用 `OnDataUpdate`；字典项被删除时调用 `OnRemove`。

### 1.4 Buff 实例 ID 和 Buff 配置 ID

系统中有两个容易混淆的 ID：

- `buffID`：配置 ID，例如 `5` 表示速度加成，`100` 表示飞行器，`101` 表示飞行伙伴；
- `buffInstanceID`：某次添加产生的唯一实例 ID，用于精确删除一个实例。

实例 ID 由以下公式生成：

```lua
uniqueID = actorID * 1000000 + sequence * 1000 + buffID
```

使用 `RemoveBuff(actorID, buffID)` 会移除该 Actor 身上该 `buffID` 的所有实例；使用 `RemoveBuffInstance(actorID, buffInstanceID)` 只移除指定实例。

## 2、为什么要使用 Buff 系统？

### 2.1 统一管理角色状态

没有 Buff 系统时，业务代码通常会分别维护：

- 当前是否加速；
- 加速什么时候结束；
- 多个状态是否互斥；
- 主权切换后由谁修改状态；
- 其他客户端如何看到状态变化；
- 状态移除时如何恢复模型、动画和移动能力。

这些逻辑分散后很容易出现“效果已经结束但标记未清除”“模型已销毁但 Actor 仍处于飞行状态”等问题。Buff 系统把公共流程集中到网络对象、管理器和基类中，具体 Buff 只实现自己的业务效果。

### 2.2 自动同步到其他客户端

Buff 列表保存在 `NetworkBuff` 的 `varSync` 字典中。拥有 Actor 主权的客户端修改字典后，状态会通过网络同步给其他客户端。其他客户端无需再次调用业务接口，只需在同步回调中创建对应 Buff 实例即可看到相同状态。

以飞行器为例：

1. 本地客户端添加 Buff 100；
2. `NetworkBuff` 将飞行器配置 key 写入 `extData`；
3. 字典同步到其他客户端；
4. 每个客户端创建 `BuffAircraft`；
5. 各客户端在本地生成飞行器模型并挂载到对应 Actor。

### 2.3 统一处理主权切换

在 Shared Mod 网络模式下，Actor 的主权可能从一个玩家转移到另一个玩家。`NetworkBuff` 会在 Actor 主权变化时调用：

```lua
Buff_Base:OnControllershipLost()
Buff_Base:OnControllershipGain()
```

通过 `Buff_Base:HasOwnership()` 可以判断当前客户端是否拥有对应 Actor 的主权。非主权客户端调用添加、更新或移除接口时，操作会转发给主权方执行。

这样可以避免多个客户端同时修改同一个 Actor 的 Buff 数据，降低状态覆盖和不同步的概率。

### 2.4 统一处理持续时间和过期

Buff 配置通过 `Duration` 定义持续时间：

- `Duration > 0`：添加时计算服务器时间 `expiredTime`，基类在 `Update` 中检查是否过期；
- `Duration = 0`：表示永久 Buff，具体 Buff 通常需要重写 `OnUpdate`，不执行过期检查。

过期判断使用 `DouyinUtility.GetServerUnixTime()`，而不是各客户端本地时间，避免玩家设备时间不同造成过期时间不一致。

### 2.5 统一处理互斥和优先级

`BuffConfig` 中的 `MutexID` 和 `Priority` 用于控制 Buff 共存：

- 不同 `MutexID`：可以同时存在；
- 相同 `MutexID`：不能无条件同时存在；
- 新 Buff 优先级更高：移除相同互斥组中已有的低优先级 Buff；
- 新 Buff 优先级更低：添加失败；
- 优先级相同：当前实现会移除已有 Buff 后添加新 Buff，代码中仍保留了“相同优先级规则”的 TODO，新增玩法时应明确产品规则。

例如当前模板中：

| Buff | Buff ID | MutexID | Priority | Duration |
| --- | ---: | ---: | ---: | ---: |
| 速度加成 | 5 | 200 | 1 | 5 秒 |
| 禁止移动 | 6 | 200 | 1 | 6 秒 |
| 位移 | 7 | 100 | 10 | 永久，依赖业务移除 |
| 飞行器 | 100 | 1000 | 1 | 永久，依赖业务移除 |
| 飞行伙伴 | 101 | 1001 | 1 | 永久，依赖业务移除 |
| 进入关卡 | 200 | 2000 | 1 | 永久，依赖业务移除 |

因此 Buff 5 和 Buff 6 属于同一互斥组，不能同时生效；Buff 100 和 Buff 101 互不冲突，可以同时存在。

## 3、如何使用 Buff 系统？

### 3.1 接入前的目录和资源准备

完整接入至少需要以下内容：

```text
Assets/DSTemplate/
├─ Prefabs/Buff/NetworkBuff.prefab
├─ Scripts/Client/System/BuffSystem/
│  ├─ index.lua
│  ├─ BuffDefine.lua
│  ├─ BuffConfig.lua
│  ├─ NetworkBuff.lua
│  ├─ NetworkBuffManager.lua
│  └─ Buff/
│     └─ Buff_Base.lua 等具体 Buff 类
└─ Scripts/Server/Logic/Buff/
   ├─ BuffDefine.lua
   ├─ BuffConfig.lua
   ├─ ServerBuffBase.lua
   └─ 具体 Buff 类
```

确保：

1. `NetworkBuff.prefab` 已加入网络对象可生成配置；
2. `NetworkBuff.lua`、`NetworkBuffManager.lua` 和 `NetworkObject.lua` 由框架作为带生命周期函数的 Host Script 自动加载；
3. Client 的 `System/index.lua` 引用了 `BuffSystem.index`；
4. Client 的 `System/index.lua` 或其他模块引用了业务 Buff 类，例如 `BuffAircraft`、`BuffFlyingPartner`、`BuffGameEntry`；
5. Server 的 `Logic/index.lua` 同时引用了 Server Buff 基类、配置和具体 Buff 类；
6. Client 和 Server 使用一致的 Buff ID、`MutexID`、`Priority`、`Type` 和 `Duration`。

`BuffSystem/index.lua` 特别说明了：`NetworkBuff`、`NetworkBuffManager`、`NetworkObject` 和 `NetworkObjectManager` 是包含 `Awake`、`Start`、`Update` 等裸生命周期函数的 Host Script，不应在普通 `index.lua` 中重复 `require`。

### 3.2 添加一个 Buff 配置

先在两端的 `BuffDefine.lua` 中增加类型：

```lua
-- Client/System/BuffSystem/BuffDefine.lua
BuffType.CustomShield = 300
```

```lua
-- Server/Logic/Buff/BuffDefine.lua
BuffType.CustomShield = 300
```

再在两端的 `BuffConfig.lua` 添加同一条配置。配置表的 key 是实际传给 `AddBuff` 的 `buffID`：

```lua
local shieldBuffId = 300

BuffConfig[shieldBuffId] = {
    ID = shieldBuffId,
    MutexID = 3000,
    Priority = 1,
    Type = BuffType.CustomShield,
    Duration = 10,
    Data = {
        absorb = 100,
    },
    Description = "护盾",
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ID` | number | 配置中的 Buff ID，建议与表 key 保持一致 |
| `MutexID` | number | 互斥组 ID；相同值的 Buff 参与互斥判断 |
| `Priority` | number | 同一互斥组内的优先级 |
| `Type` | number | 对应 `BuffType` 的值，用于找到具体 Buff 类 |
| `Duration` | number | 持续秒数；`0` 表示永久 Buff |
| `Data` | table | 静态默认配置，具体运行时逻辑可按需读取 |
| `Description` | string | 用于说明该 Buff 的用途 |

### 3.3 实现 Client Buff

客户端具体 Buff 继承 `Buff_Base`，至少应实现 `__init`、`OnAdd` 和 `OnRemove`。有动态行为时再实现 `OnUpdate`、`OnLateUpdate` 或 `OnFixedUpdate`。

```lua
-- Client/System/BuffSystem/Buff/Buff_CustomShield.lua
Buff_CustomShield = BaseClass:DefineClass("Buff_CustomShield", Buff_Base)

function Buff_CustomShield:__init(actorID, buffId, buffInstanceID, jsonData)
    Buff_Base.__init(self, actorID, buffId, buffInstanceID, jsonData)
    self.runtimeData = self.runtimeData or {}
end

function Buff_CustomShield:OnAdd()
    Buff_Base.OnAdd(self)

    local actor = CS.DouyinActorService.GetActorById(self.actorID)
    if actor == nil then
        return
    end

    -- 创建护盾特效，或设置客户端表现
end

function Buff_CustomShield:OnRemove()
    Buff_Base.OnRemove(self)

    -- 销毁护盾特效，恢复被修改的客户端状态
end
```

然后在 `BuffSystem/index.lua` 中引用该类：

```lua
require "Buff.Buff_CustomShield"
```

最后在 `NetworkBuff.lua` 的类型映射中增加分支：

```lua
elseif buffType == BuffType.CustomShield then
    BuffTypeInstance = Buff_CustomShield
```

没有这一步时，配置虽然已经同步，但客户端无法创建具体 Buff 实例，会输出“未找到 BuffType”相关日志。

### 3.4 实现 Server Buff

服务端 Buff 继承独立的 `Buff_Base`。服务端基类的构造函数接收以下参数：

```lua
function Buff_Base:__init(actorID, buffId, buffInstanceID, jsonData)
```

示例：

```lua
-- Server/Logic/Buff/Buff_CustomShield.lua
Buff_CustomShield = BaseClass:DefineClass("Buff_CustomShield", Buff_Base)

function Buff_CustomShield:__init(actorID, buffId, buffInstanceID, jsonData)
    Buff_Base.__init(self, actorID, buffId, buffInstanceID, jsonData)
end

function Buff_CustomShield:OnAdd()
    Buff_Base.OnAdd(self)

    -- 在这里处理 DS 侧的状态、数值或安全校验
end

function Buff_CustomShield:OnRemove()
    Buff_Base.OnRemove(self)

    -- 清理 DS 侧状态
end
```

并在 `Server/Logic/index.lua` 中引用：

```lua
require "Buff.Buff_CustomShield"
```

Client 和 Server 的具体实现不要求代码完全相同，但必须对同一个 Buff ID 和同一种数据结构达成约定。涉及结算、倍率、权限和反作弊的逻辑，应放在服务端处理，客户端只负责表现和交互反馈。

### 3.5 添加 Buff

业务层通常使用 `NetworkBuffManager` 添加 Buff：

```lua
local actorID = actor.actorID
local buffID = 5

NetworkBuffManager.AddBuff(actorID, buffID)
```

带扩展数据时，将第三个参数传入 `extData`：

```lua
local aircraftKey = "aircraft_001"
NetworkBuffManager.AddBuff(actorID, 100, aircraftKey)
```

模板中的 `BuffAircraft` 会把 `extData` 当作飞行器资源 key；`BuffFlyingPartner` 则把 `extData` 当作飞行伙伴 key 列表。扩展数据类型由具体 Buff 自己约定，但添加、更新时必须保持一致。

添加流程如下：

```text
业务调用 AddBuff
    -> NetworkBuffManager 找到 actor 对应的 NetworkBuff
    -> 若当前客户端不是主权方，则 SendMessageToOwner 转发
    -> 主权方检查配置、互斥组和优先级
    -> 生成 buffInstanceID
    -> 写入 syncBuffDic
    -> 网络同步
    -> 各客户端根据 BuffType 创建具体 Buff
    -> 调用 OnAdd
```

如果 Actor 对应的 `NetworkBuff` 尚未完成生成，管理器会把添加请求暂存到缓存中，在网络对象生成后自动补发。因此业务可以在 Actor 刚生成时调用，但仍建议在 Actor 和相关系统初始化完成后再添加，以减少资源未准备好的情况。

### 3.6 查询 Buff

判断 Actor 是否拥有某个 Buff：

```lua
if NetworkBuffManager.HasBuff(actorID, 5) then
    print("Actor 当前拥有速度加成")
end
```

读取某个 Buff 的 `extData`：

```lua
local extData = NetworkBuffManager.GetBuffExtData(actorID, 100)
```

查询房间内拥有某 Buff 的 Actor 数量：

```lua
local count = NetworkBuffManager.GetBuffNumber(101)
```

查询房间内拥有某 Buff 的 Actor 及其同步数据：

```lua
local actorsData = NetworkBuffManager.GetBuffActorsData(101)
```

`GetBuffActorsData` 返回的 value 已经是 `syncBuffDic` 中的 JSON 字符串，调用方不要对 value 再次编码；需要读取时再进行 JSON 解码。

### 3.7 更新 Buff 数据

使用 `UpdateBuffData` 更新已有 Buff 的 `extData`：

```lua
NetworkBuffManager.UpdateBuffData(actorID, 100, "aircraft_002", false)
```

最后一个参数 `resetExpiredTime` 的含义：

- `false`：保留原来的过期时间，只更新扩展数据；
- `true`：根据当前时间和配置中的 `Duration` 重新计算过期时间。

更新只会修改已有 Buff。若当前 Actor 没有该 Buff，接口不会自动添加，应先调用 `AddBuff`。

### 3.8 移除 Buff

按 Buff ID 移除该 Actor 身上同 ID 的所有 Buff：

```lua
NetworkBuffManager.RemoveBuff(actorID, 5)
```

按实例 ID 精确移除：

```lua
NetworkBuffManager.RemoveBuffInstance(actorID, buffInstanceID)
```

在具体 Buff 内部，通常使用：

```lua
self:RemoveBuff()
```

该方法会检查当前客户端是否拥有 Actor 主权，并使用当前 Buff 的 `buffInstanceID` 精确删除自身。

### 3.9 处理生命周期

`Buff_Base` 提供的主要回调如下：

| 回调 | 调用时机 | 典型用途 |
| --- | --- | --- |
| `__init` | 创建 Buff 实例时 | 读取 Actor ID、Buff ID、实例 ID 和 JSON 数据 |
| `OnDataUpdate` | Buff 的同步数据变化时 | 读取新的 `expiredTime` 和 `extData`；热更新表现 |
| `OnAdd` | Buff 新增后 | 创建模型、特效、设置状态或注册事件 |
| `OnUpdate` | 每帧更新 | 处理过期、持续性逻辑和状态检查 |
| `OnLateUpdate` | 每帧 LateUpdate | 处理依赖其他对象完成更新后的逻辑 |
| `OnFixedUpdate` | 每次 FixedUpdate | 处理固定帧率逻辑 |
| `OnRemove` | Buff 被移除或网络对象销毁时 | 销毁对象、移除监听、恢复 Actor 状态 |
| `OnControllershipLost` | Actor 主权丢失时 | 停止只能由主权方执行的操作 |
| `OnControllershipGain` | Actor 获得主权时 | 重新接管需要主权的逻辑 |
| `OnActorRespawn` | Actor 重生时 | 重新绑定或恢复表现 |
| `OnActorLoaded` | Actor 模型加载完成时 | 重新绑定模型、骨骼和相机节点 |
| `OnActorOperationChanged` | Actor 可操作状态变化时 | 响应操作权限改变 |

`OnRemove` 必须是幂等的：重复执行时不能报错，也不能重复销毁已经销毁的对象。所有在 `OnAdd` 中创建的 GameObject、事件监听和状态引用，都应在 `OnRemove` 中清理。

### 3.10 编写有持续时间的 Buff

对于普通时效 Buff，直接使用基类的 `OnUpdate` 即可：

```lua
function Buff_CustomShield:OnUpdate()
    Buff_Base.OnUpdate(self)
end
```

基类会在拥有 Actor 主权时检查 `expiredTime`，到期后设置延迟移除标记，并在后续更新中移除实例。

对于永久 Buff，必须重写 `OnUpdate`，否则不应将 `expiredTime` 当作普通过期时间使用：

```lua
function Buff_CustomShield:OnUpdate()
    -- Duration=0 的永久 Buff：执行持续逻辑，不做过期检查
end
```

### 3.11 一个完整的调用示例

以下示例为本地 Actor 添加 5 秒速度加成，并在结束时清理：

```lua
local SPEED_BUFF_ID = 5

function ApplySpeedBuff(actor)
    if actor == nil then
        return
    end

    NetworkBuffManager.AddBuff(actor.actorID, SPEED_BUFF_ID, {
        source = "speed_prop",
        level = 1,
    })
end

function ClearSpeedBuff(actor)
    if actor == nil then
        return
    end

    NetworkBuffManager.RemoveBuff(actor.actorID, SPEED_BUFF_ID)
end

function IsSpeedBuffActive(actor)
    return actor ~= nil and NetworkBuffManager.HasBuff(actor.actorID, SPEED_BUFF_ID)
end
```

该调用不需要手动启动计时器。因为配置中的 `Duration = 5`，系统会在添加时写入服务器时间，主权方在 `Update` 中完成过期清理，并通过 `syncBuffDic` 将移除结果同步给其他客户端。

## 4、常见问题与限制

### 4.1 当前 SDK 项目中的 Buff 目录不完整

`Hot Dance Only SDK` 当前只包含：

```text
Assets/Scripts/Server/Logic/Buff/
├─ BuffConfig.lua
├─ BuffDefine.lua
└─ ServerBuffBase.lua
```

客户端没有独立的 `BuffSystem`、`NetworkBuff.lua` 和 `NetworkBuffManager.lua`。客户端 `PlayerSystem.lua` 中的 `playerDataLobbyBuffRequested` 只是已移除的历史业务标记，不是可调用的 Buff 管理器。

因此不能只复制 `Server/Logic/Buff` 就认为 Buff 系统已经接入；至少还需要 Client BuffSystem、网络 Buff 预制体以及对应的 Host Script。

### 4.2 Client 和 Server 的配置必须一致

以下内容不一致会导致客户端无法识别或两端行为不同：

- Buff ID；
- `BuffType` 数值；
- `MutexID`；
- `Priority`；
- `Duration`；
- `extData` 的结构。

建议把配置变更作为一次完整修改，同时检查 Client 和 Server 两份文件，而不是只改其中一端。

另外，当前模板的 `BuffConfig.lua` 中，表 key `[3]` 和 `[4]` 的 `ID` 字段仍为 `2`。系统运行时通过 `BuffConfig[buffID]` 使用表 key 查找配置，因此实际调用 ID 仍分别是 `3` 和 `4`；新增配置时应保持“表 key、`ID`、调用参数三者一致”，并建议后续修正这两项配置，避免调试和日志中的 ID 产生歧义。

### 4.3 `NetworkBuff` 尚未生成时的调用

`NetworkBuffManager.AddBuff` 和 `UpdateBuffData` 支持在网络对象尚未生成时缓存请求，但查询接口在对象不存在时会返回 `false` 或 `nil`。因此：

- 添加可以提前调用；
- 查询应在 Actor 和 NetworkBuff 准备完成后调用；
- 若需要确认添加成功，应监听后续状态或在短延迟后再次查询；
- 不要把 `HasBuff == false` 直接等同于“添加失败”，也可能是网络对象尚未注册。

### 4.4 非主权客户端不能直接改同步数据

业务层可以在任意客户端调用管理器接口，但实际修改会转发到 Actor 主权方。具体 Buff 内部如果直接操作 `syncBuffDic`，必须先判断主权，否则可能造成状态被覆盖或逻辑不一致。

### 4.5 `RemoveBuff` 和 `RemoveBuffInstance` 的范围不同

`RemoveBuff(actorID, buffID)` 会移除该 Buff ID 的所有实例；需要只结束某一次效果时，必须保存 `buffInstanceID` 并使用 `RemoveBuffInstance`。

### 4.6 静态 `Data` 和运行时 `extData` 不同

- `BuffConfig[buffID].Data`：静态配置，适合默认参数；
- `extData`：每次添加或更新时传入的运行时数据，适合资源 key、玩家 ID、关卡 ID、动态数值等；
- `runtimeData`：Buff 实例本地运行时数据，不参与网络同步，适合保存实例化的 GameObject、Transform 和临时引用。

不要把 Unity 对象、函数或不能序列化的对象放入 `extData`。网络 Buff 的扩展数据最终会写入 JSON。

### 4.7 当前模板中部分类型仍是预留或依赖业务补充

`NetworkBuff.lua` 中包含 `Grab`、`Flee`、`Sitout`、`FleeCamera` 等类型映射，但模板实际是否提供这些类型的具体类，需要以当前目录文件为准。新增或启用类型时必须确认三件事：

1. `BuffDefine` 中存在类型；
2. `BuffConfig` 中存在配置；
3. `NetworkBuff.lua` 能映射到已加载的具体类。

缺少任一项，Buff 都无法完整工作。

### 4.8 Buff 系统不等于持久化系统

网络 Buff 默认是房间运行时状态。它不会自动写入数据存储，也不会自动在玩家下次进入房间时恢复。如果 Buff 需要跨房间或跨登录保存，需要由服务端单独设计持久化数据，并在玩家加入或数据加载完成后重新添加 Buff。

### 4.9 推荐的排查顺序

当 Buff 没有生效时，按以下顺序检查：

1. `buffID` 是否存在于 `BuffConfig`；
2. Client 和 Server 的 ID、Type、Duration、MutexID 是否一致；
3. Actor 是否存在且 `actorID` 正确；
4. `NetworkBuff.prefab` 是否正确生成；
5. `NetworkBuffManager` 是否已注册该 Actor；
6. 当前调用方是否拥有 Actor 主权；
7. `NetworkBuff.lua` 是否能根据 `Type` 找到具体 Buff 类；
8. `OnAdd` 是否因为 Actor、系统或资源未准备完成而提前返回；
9. `OnRemove` 是否清理了表现，导致刚添加的效果立即被移除；
10. 查看 `[DS_TRACE][BUFF_VISUAL]` 和 `NetworkBuff` 相关日志。
