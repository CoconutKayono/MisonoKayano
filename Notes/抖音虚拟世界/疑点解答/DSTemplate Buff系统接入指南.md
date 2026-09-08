# DSTemplate Buff 系统接入指南

本文档根据 DSTemplate 的 Client/Server Buff 模块整理，说明 Buff 的数据模型、同步方式、主权规则、生命周期、配置和接入步骤。Buff 不是单纯的 UI 特效：它通常会影响角色属性、技能、控制状态、伤害或其他玩法规则，因此服务端与客户端必须使用一致的定义，并明确谁有权修改 Buff 状态。

## 1. Buff 系统是什么

Buff 系统把附着在 Actor 上的临时或永久状态统一抽象为 Buff 实例，并提供：

- 添加、查询、更新、移除 Buff；
- Buff 持有扩展数据 extData；
- Buff 的互斥、优先级和持续时间配置；
- 服务端/客户端之间的状态同步；
- Buff 生命周期回调；
- Actor 主权变化、重生、加载和操作状态变化时的通知；
- 运行时查询某个 Buff 影响了哪些 Actor。

典型数据关系：

~~~text
Actor
 └─ NetworkBuffManager
     └─ Buff ID
         ├─ expiredTime
         └─ extData
~~~

在 DSTemplate 中，Buff 的实际运行载体通常是 NetworkBuff Prefab，服务端和客户端分别有一套定义、配置和逻辑：

~~~text
Scripts/Server/Logic/Buff/
├─ BuffDefine.lua
├─ BuffConfig.lua
└─ ServerBuffBase.lua

Scripts/Client/System/BuffSystem/
├─ BuffDefine.lua
├─ BuffConfig.lua
├─ Buff_Base.lua
├─ NetworkBuff.lua
└─ NetworkBuffManager.lua

Prefabs/Buff/
└─ NetworkBuff.prefab
~~~

Scripts 目录中大量内容是 DS 模块源代码。接入 Buff 时应优先复用这些模块和既有接口，不要在业务脚本中重新维护一套状态表。

## 2. Buff 的同步数据模型

NetworkBuff 使用同步变量保存当前 Actor 的 Buff 状态，核心同步字段为：

~~~lua
---@varSync syncActorID:int=0
---@varSync syncBuffID:int=0
---@varSync syncBuffDic:Dictionary<long, string>
~~~

syncBuffDic 的典型 value 结构为：

~~~lua
{
    expiredTime = ...,
    extData = ...,
}
~~~

可以把它理解为：

~~~text
buffInstanceID → { expiredTime, extData }
~~~

其中：

- buffInstanceID 区分同一个 Buff ID 的不同实例；
- syncBuffID 用于同步当前处理或新增的 Buff 类型；
- syncActorID 标识 Buff 所属 Actor；
- expiredTime 是按服务端 Unix 时间计算的过期时间；
- extData 是业务自定义参数，例如来源、层数、倍率、目标技能或状态快照。

不要假设 extData 一定是某一种类型。业务需要在 Client 和 Server 两端约定同样的字段和类型，并在使用前做空值、类型和版本兼容处理。

## 3. 配置定义

客户端和服务端的 Buff 定义/配置至少要保持以下字段一致：

| 字段 | 作用 |
| --- | --- |
| ID | Buff 类型的唯一 ID |
| MutexID | 互斥组 ID，用于处理互斥 Buff |
| Priority | 互斥或覆盖判定时的优先级 |
| Type | Buff 类型，供逻辑分支使用 |
| Duration | 默认持续时间；大于 0 为时效 Buff |
| Data | 业务参数或配置数据 |
| Description | 调试、编辑和配置说明 |

配置的 ID、Type、MutexID、Priority、Duration 和 Data 不能只在一端修改。否则会出现：

- Server 判定 Buff 有效，Client 找不到对应类型；
- 两端过期时间不同；
- 互斥关系和优先级判定不一致；
- 特效显示了，但服务端规则没有生效；
- 重连后 Buff 实例无法恢复。

## 4. 主权规则

Buff 状态的最终修改权属于 Actor 当前主权方：

- 主权方可以实际修改 syncBuffDic；
- 非主权方调用添加、更新或移除时，应把请求转发到主权方；
- 非主权方不能本地直接写同步字典来“抢先生效”；
- 主权发生变化时，Buff 系统需要重新处理当前实例和生命周期。

主权规则尤其重要于：

- 多人房间；
- 角色被转移、重生或重新加载；
- Client/Server 同时存在同一 Actor 的网络对象；
- Buff 会改变伤害、控制或其他需要权威判定的规则。

可以用下面的判断理解调用方向：

~~~text
业务请求
   ↓
当前脚本是否拥有 Actor 主权？
   ├─ 是：直接修改 Buff 实例并触发同步
   └─ 否：转发给主权方，由主权方修改 syncBuffDic
~~~

如果 Buff 会影响奖励、伤害、胜负或其他需要安全保证的玩法，最终判定应放在服务端权威逻辑中；客户端 Buff 主要负责镜像和表现，不能作为安全边界。

## 5. Buff 生命周期

Buff 基类支持以下典型生命周期回调：

| 回调 | 适合做什么 |
| --- | --- |
| __init | 初始化实例字段、读取配置和 extData |
| OnDataUpdate | 同步数据变化后更新内部状态 |
| OnAdd | 第一次加入 Actor 时执行 |
| OnUpdate | 常规 Tick，处理持续效果 |
| OnLateUpdate | LateUpdate 阶段的表现或收尾逻辑 |
| OnFixedUpdate | 固定时间步逻辑，例如物理或周期计算 |
| OnRemove | Buff 被移除或过期时清理效果 |
| OnControllershipLost | 当前对象失去主权 |
| OnControllershipGain | 当前对象获得主权 |
| OnActorRespawn | Actor 重生时重新处理 Buff |
| OnActorLoaded | Actor 或 Buff 网络对象加载完成 |
| OnActorOperationChanged | Actor 的可操作状态变化 |

生命周期函数中要区分“初始化一次”和“每帧调用”：

- OnAdd 适合注册效果、初始化层数；
- OnUpdate 适合轻量周期检查，避免在其中重复创建对象；
- OnRemove 必须撤销 OnAdd 带来的属性、监听器和特效；
- 主权切换回调不能假设实例只在一个端执行；
- 过期判断应使用服务端统一时间，不要使用本地设备时间。

包含裸生命周期函数的 Host Script（例如 NetworkBuff.lua、NetworkBuffManager.lua）由框架自动挂载，不能在 index.lua 中重复 require。

## 6. 管理器 API

NetworkBuffManager 提供的常用接口如下：

~~~lua
NetworkBuffManager.AddBuff(actorID, buffID, extData)
NetworkBuffManager.HasBuff(actorID, buffID)
NetworkBuffManager.GetBuffExtData(actorID, buffID)
NetworkBuffManager.UpdateBuffData(actorID, buffID, extData, resetExpiredTime)
NetworkBuffManager.RemoveBuff(actorID, buffID)
NetworkBuffManager.RemoveBuffInstance(actorID, buffInstanceID)
NetworkBuffManager.GetBuffNumber(buffID)
NetworkBuffManager.GetBuffActorsData(buffID)
~~~

接口语义：

| 接口 | 作用 |
| --- | --- |
| AddBuff | 向 Actor 添加一个 Buff，可携带扩展数据 |
| HasBuff | 判断 Actor 是否拥有指定 Buff |
| GetBuffExtData | 读取指定 Buff 当前扩展数据 |
| UpdateBuffData | 更新扩展数据；按参数决定是否重置过期时间 |
| RemoveBuff | 按 Actor 和 Buff 类型移除 |
| RemoveBuffInstance | 按具体实例 ID 移除 |
| GetBuffNumber | 查询当前某个 Buff 的实例数量 |
| GetBuffActorsData | 查询持有某个 Buff 的 Actor 数据 |

具体函数是否需要通过 NetworkBuffManager 实例调用，取决于当前模板的管理器暴露方式；业务代码应以模板中已有调用示例为准。

## 7. 持续时间与过期规则

推荐统一使用：

~~~lua
DouyinUtility.GetServerUnixTime()
~~~

时间规则：

- Duration > 0：从添加或重置时间开始计算的时效 Buff；
- Duration = 0：通常表示永久 Buff，直到显式移除；
- resetExpiredTime == true：更新数据时重新计算过期时间；
- resetExpiredTime == false：更新扩展数据但保留原过期时间；
- 客户端显示剩余时间时应以同步到的 expiredTime 为准；
- 服务端仍应在关键业务判断处再次检查是否已经过期。

不要直接使用客户端设备时间判断是否过期。设备时间可能被调整，且不同设备之间存在偏差。

## 8. 一个业务 Buff 的接入步骤

### 8.1 定义 ID 和配置

先在 Client/Server 两端的 BuffDefine.lua、BuffConfig.lua 或对应配置表中增加：

- Buff ID；
- 类型；
- 互斥组；
- 优先级；
- 持续时间；
- Data 参数；
- 描述。

确认两端加载的是同一版本配置。

### 8.2 实现 Buff 行为

服务端实现影响规则的部分，客户端实现镜像和表现部分。示意：

~~~lua
-- 业务侧调用，具体入口按项目玩法决定
local extData = {
    sourceActorID = sourceActorID,
    stack = 1,
    multiplier = 1.2,
}

NetworkBuffManager.AddBuff(targetActorID, BuffDefine.PowerUp, extData)
~~~

实现 Buff 类时：

- 在 OnAdd 中应用初始效果；
- 在 OnDataUpdate 中同步层数或倍率；
- 在 OnUpdate / OnFixedUpdate 中执行周期逻辑；
- 在 OnRemove 中撤销效果；
- 如果效果影响服务端玩法，服务端必须有对应权威逻辑；
- 不要把客户端 UI 关闭当作移除 Buff 的真实依据。

### 8.3 接入 NetworkBuff Prefab

确认场景或角色生成流程能够挂载/生成 Prefabs/Buff/NetworkBuff.prefab，并且：

- 网络对象配置正确；
- Buff 管理器生命周期能够运行；
- syncBuffDic 等同步变量被正确声明；
- Server 和 Client 都加载对应 Buff 定义；
- Actor 变化、重生和主权变更事件能到达管理器。

如果项目使用自动挂载，优先复用模板已有注册和 Prefab 配置，不要额外创建同名管理器。

### 8.4 验证同步和主权

至少测试以下场景：

1. Actor 主权方添加 Buff，其他客户端能收到；
2. 非主权方请求添加 Buff，请求最终转发到主权方；
3. 更新 extData 后，两端生命周期收到 OnDataUpdate；
4. 时效 Buff 到期后，主权方移除，其他端也移除；
5. 永久 Buff 不因一次 Tick 自动消失；
6. Actor 重生后 Buff 是否按设计保留、清理或重建；
7. 主权丢失/获得后，Buff 不重复应用效果；
8. 断线重连或 Actor 重新加载后，Buff 状态与主权方一致。

## 9. Buff 与数据存储的边界

Buff 默认是运行时状态，不应因为“看起来像玩家属性”就直接写入玩家 DataStore。需要持久化时，应明确区分：

- 运行时实例：由 NetworkBuff / NetworkBuffManager 管理；
- 玩家长期状态：由 ServerPlayerData 的数据域管理；
- 重新进入房间时：从持久化域按业务规则重新添加 Buff；
- 离开房间时：不要把同步字典直接作为长期存档格式。

例如“VIP 权益”可以持久化为玩家的资格或到期时间，进入房间后由服务端根据该数据添加 VIP Buff；不要让客户端直接保存 VIP Buff 并据此获得权益。

## 10. 常见问题

### Client 有特效但 Server 没有 Buff

通常是客户端直接调用了表现逻辑，或服务端配置/ID 未同步。检查添加入口是否经过主权方，以及两端 BuffDefine 是否一致。

### Buff 添加后立即消失

检查：

- Duration 是否被配置成很小的值；
- 过期时间是否使用了错误的时间单位；
- 是否在 UpdateBuffData 时误传 resetExpiredTime；
- 主权切换回调是否重复执行了移除；
- 互斥组是否被更高优先级 Buff 替换。

### Buff 叠加数量不正确

确认业务使用的是 buffID 还是 buffInstanceID。同一个 Buff 类型可能有多个实例；按类型移除和按实例移除的语义不同。

### 重连后 Buff 状态不一致

检查同步字典是否由主权方维护，Buff 网络对象是否重新加载，OnActorLoaded 是否正确处理，且客户端没有用本地时间或本地缓存覆盖服务端快照。

## 11. Buff 接入清单

- [ ] Client/Server 的 Buff ID 和配置已同步；
- [ ] NetworkBuff.prefab 已接入生成/挂载流程；
- [ ] syncActorID、syncBuffID、syncBuffDic 已正确声明；
- [ ] 主权方负责真正修改 Buff 状态；
- [ ] extData 结构在双端一致；
- [ ] 时效判断使用 DouyinUtility.GetServerUnixTime()；
- [ ] OnAdd 和 OnRemove 成对实现；
- [ ] 主权切换、重生、加载、断线重连均已测试；
- [ ] 需要持久化的长期资格与运行时 Buff 已分层；
- [ ] 不在 index.lua 重复 require Host Script。

