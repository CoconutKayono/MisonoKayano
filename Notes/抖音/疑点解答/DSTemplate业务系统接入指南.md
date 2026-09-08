# DSTemplate 业务系统接入指南

本文档以新增成就系统为例，说明如何在 DSTemplate 中接入一条完整的业务系统。这里的“业务系统”不仅是一个客户端页面或一个 Manager，而是由协议、服务端数据域、服务端业务处理、客户端数据镜像、客户端 System 和生命周期注册共同组成的端到端链路。

> 适用范围：需要在 Scripts 中新增玩家业务、持久化数据、C2S/S2C 通信和客户端表现的功能。
> 相关基础说明：[DSTemplate 模板框架与 Scripts 目录说明](DSTemplate模板框架与Scripts目录说明.md)；[DSTemplate 数据存储详解](DSTemplate数据存储详解.md)。

## 1. 一条业务的完整链路

~~~text
客户端 UI / View
    ↓ 调用
AchievementSystem:CSUnLockAchievement(achievementId)
    ↓ C2S
服务端协议包 / Handler
    ↓ 转发
ServerAchievementManager.HandleUnlockAchievement(...)
    ↓ 访问
ServerPlayerData 聚合根
    ↓
ServerAchievementData.Update(...)
    ↓ 标脏，等待统一 Flush 落盘
    ↓ S2C
SCUnLockAchievement
    ↓
AchievementSystem:OnSCUnLockAchievement(...)
    ↓
ClientAchievementData 覆写本地镜像
    ↓
UI / 表现刷新
~~~

关键原则：

- 客户端只提交意图和必要参数，不决定最终结果；
- 服务端负责身份、参数、条件、重复操作和数据域状态校验；
- 服务端通过 ServerPlayerData 聚合根访问数据域；
- 数据域通过 Create、Update、Remove 等接口标脏；
- 客户端 Model 是服务端数据的镜像，不能作为持久化入口；
- S2C 回包应携带服务端最终状态，避免客户端预测结果长期漂移。

## 2. 新增业务通常涉及哪些文件

以 Achievement 为例，典型文件分布如下：

~~~text
Scripts/
├─ Common/
│  └─ NetworkPacket/
│     ├─ NetPacketType.lua              # 新增协议类型
│     ├─ CSUnLockAchievement.lua        # C2S 包
│     ├─ SCUnLockAchievement.lua        # S2C 包
│     └─ index.lua                      # 注册/加载协议包
├─ Server/
│  ├─ Data/
│  │  ├─ ServerAchievementData.lua      # 服务端数据域
│  │  └─ index.lua
│  ├─ Logic/
│  │  └─ Achievement/
│  │     └─ ServerAchievementManager.lua
│  ├─ Network/
│  │  └─ ClientPacketRegister.lua       # C2S Handler 注册位置，按模板实际文件为准
│  └─ ServerPlayerData.lua               # 聚合根接入
└─ Client/
   ├─ Model/
   │  ├─ ClientAchievementData.lua       # 客户端内存镜像
   │  └─ ClientPlayerData.lua             # 客户端聚合根接入
   ├─ System/
   │  └─ AchievementSystem/
   │     ├─ AchievementSystem.lua
   │     └─ AchievementSystemRegister.lua
   └─ Network/
      └─ ClientPacketRegister.lua         # S2C Handler 注册位置
~~~

实际模板可能把 ClientPacketRegister、ServerPacketRegister 或业务目录拆分成不同文件。判断标准不是文件名，而是：

- C2S 在服务端注册；
- S2C 在客户端注册；
- Data 在对应端的 index.lua 中加载；
- 带裸生命周期函数的 Register/Host Script 由框架挂载。

## 3. 第一步：设计协议

### 3.1 先定义协议类型

在 Common/NetworkPacket/NetPacketType.lua 增加 C2S 和 S2C 类型。协议类型必须在双端使用同一份定义，避免 Client 和 Server 的枚举值不一致。

建议先确定：

- 请求名称：例如 CSUnLockAchievement；
- 回包名称：例如 SCUnLockAchievement；
- 请求参数：通常为 achievementId；
- 回包结构：code、msg、data；
- data 中携带的最终状态：例如成就 ID、是否已解锁、当前成就列表或增量。

### 3.2 协议包负责 Pack / Unpack

自定义包继承 BaseNetPacket，只负责序列化和反序列化，不在包类中写业务规则。

示意结构：

~~~lua
CSUnLockAchievement = BaseClass:DefineClass(
    "CSUnLockAchievement",
    BaseNetPacket
)

function CSUnLockAchievement:Pack(achievementId)
    return {
        achievementId = achievementId,
    }
end

function CSUnLockAchievement:Unpack(data)
    return {
        achievementId = data.achievementId,
    }
end
~~~

S2C 回包应遵循统一结果格式：

~~~lua
{
    code = 0,
    msg = "",
    data = {
        achievementId = achievementId,
        unlocked = true,
    },
}
~~~

建议约定：

- code == 0：成功；
- code < 0：业务失败；
- msg：适合日志和调试的简短信息；
- data：只有成功或客户端需要恢复状态时才填充有效业务数据。

包的字段名必须在发送方和接收方完全一致。Pack/Unpack 不要擅自把数字 ID 转成字符串或反之，除非协议已经统一约定。

### 3.3 在 Common/index.lua 注册

协议类在 Common/NetworkPacket/index.lua 或模板规定的统一注册入口中加载。不要创建一套平行的协议枚举或网络管理器，否则容易出现：

- 包类型值重复；
- Server 能收包但 Client 无法创建回包；
- 本地测试正常、云端包注册顺序不一致。

## 4. 第二步：创建服务端数据域

### 4.1 ServerAchievementData 的职责

服务端数据域负责：

- 保存成就领域的内存快照；
- 提供默认值；
- 归一化历史或异常数据；
- 通过 Create、Update、Remove 标记数据变更；
- 被聚合根统一加载、Flush 和重同步。

数据域不负责：

- 直接收网络包；
- 直接向客户端发回包；
- 在 DataStore 上自行建一套读写逻辑；
- 把玩家权限校验散落在数据字段操作里。

示意结构：

~~~lua
ServerAchievementData = BaseClass:DefineClass(
    "ServerAchievementData",
    ServerDataBase
)

function ServerAchievementData:__init(playerOpenId)
    ServerDataBase.__init(
        self,
        playerOpenId,
        "achievement",
        "achievement_",
        "achievement_data"
    )
end

function ServerAchievementData:GetDefaultValue()
    return {
        achievements = {},
    }
end

function ServerAchievementData:NormalizeValue(rawValue)
    if type(rawValue) ~= "table" then
        return self:GetDefaultValue()
    end

    if type(rawValue.achievements) ~= "table" then
        rawValue.achievements = {}
    end

    return rawValue
end
~~~

当前模板的 ServerDataBase:__init 使用 playerOpenId、domainKey、scopePrefix、dataKey 四个参数。新增域时应以当前基类实现为准，不要照搬旧版五参数构造方式。

### 4.2 接入 ServerPlayerData

至少要检查以下位置：

1. ServerPlayerData.__init：创建 achievementData；
2. AreAllDomainsLoaded：加入 achievementData:IsLoaded()；
3. LoadIntoCache：调用 achievementData:Load(...)，并纳入异步加载计数；
4. Flush：调用 achievementData:Save(force, callback)；
5. SendPlayerDataToPlayer：首包加入 achievementData:Get()；
6. SendResyncToPlayer：重同步时按域版本返回成就数据。

另外，ServerDataCache.versionedDomains 必须加入 achievement，这样该域才能参与断线重连和版本重同步。

完整数据域接入方法见：[DSTemplate 数据存储详解](DSTemplate数据存储详解.md)。

## 5. 第三步：创建服务端 Manager

### 5.1 Manager 的职责

ServerAchievementManager 是业务权威入口，负责：

- 接收 C2S Handler 转发；
- 校验请求参数；
- 获取当前玩家聚合根；
- 检查成就是否存在、是否已解锁、是否满足解锁条件；
- 修改 ServerAchievementData；
- 组织 S2C 回包；
- 返回可重试或不可重试的错误。

Manager 不应直接调用 ServerDataCache，也不应直接向 DataStore 写入。

### 5.2 推荐处理顺序

~~~lua
function ServerAchievementManager:HandleUnlockAchievement(playerOpenId, request)
    local achievementId = request and request.achievementId
    if achievementId == nil then
        return {
            code = -1,
            msg = "missing achievementId",
            data = {},
        }
    end

    local aggregate = ServerPlayerDataManager.Get(playerOpenId)
    if aggregate == nil then
        return {
            code = -2,
            msg = "player aggregate not found",
            data = {},
        }
    end

    local data = aggregate.achievementData
    if data == nil or not data:IsLoaded() then
        return {
            code = -3,
            msg = "achievement data is not loaded",
            data = {},
        }
    end

    -- 这里继续做配置、条件和重复解锁校验。
    -- 通过 Update/Create 标脏，而不是直接修改 Get() 返回表后忘记通知数据域。
    local achievements = data:Get("achievements") or {}
    achievements[tostring(achievementId)] = true
    data:Update("achievements", achievements)

    return {
        code = 0,
        msg = "",
        data = {
            achievementId = achievementId,
            unlocked = true,
        },
    }
end
~~~

上面代码展示职责边界，实际模板中的 Handler 和发送回包方式应沿用已有 Manager 的写法。

### 5.3 错误码建议

| code | 含义 | 客户端处理建议 |
| --- | --- | --- |
| 0 | 成功 | 用回包最终状态刷新 Model |
| -1 | 请求缺少必要参数 | 修正调用方，不重试原请求 |
| -2 | 玩家聚合不存在 | 等待玩家数据初始化或记录异常 |
| -3 | 数据域尚未加载 | 等待初始化完成后再发起 |
| 其他负数 | 业务条件不满足/重复/配置错误 | 根据业务决定提示或重试 |

错误码不是安全校验的替代品。服务端仍要对所有来自客户端的字段重新校验。

## 6. 第四步：注册 C2S Handler

在服务端网络注册入口中，把 CSUnLockAchievement 绑定到 ServerAchievementManager：

~~~lua
NetPacketManager:RegisterHandler(
    NetPacketType.CSUnLockAchievement,
    function(playerOpenId, packet)
        local result =
            ServerAchievementManager:HandleUnlockAchievement(
                playerOpenId,
                packet
            )

        -- 按当前 ServerEventNetwork 的发送约定回发 SC。
        SendSCUnLockAchievement(playerOpenId, result)
    end
)
~~~

注册逻辑只负责“收到什么包、交给谁处理、回什么包”。不要在注册函数中堆放成就规则，否则后续测试、复用和错误处理都会变得困难。

## 7. 第五步：创建客户端 Model

ClientAchievementData 是本地内存镜像，职责是：

- 保存首包和 S2C 回包中的成就数据；
- 提供查询接口给 System 和 View；
- 在服务端回包后整体或局部替换；
- 必要时触发数据变更事件。

它不负责：

- 写 DataStore；
- 绕过 C2S 修改服务端；
- 代替 AchievementSystem 发网络包；
- 把客户端预测结果当成最终状态。

示意：

~~~lua
ClientAchievementData = BaseClass:DefineClass(
    "ClientAchievementData",
    ClientDataBase
)

function ClientAchievementData:ApplyServerData(newData)
    if type(newData) ~= "table" then
        return false
    end

    self:ReplaceRootDataFromServer(newData)
    return true
end
~~~

同时修改 ClientPlayerData：

- 创建 achievementData；
- 销毁时释放该数据域；
- 首包构造时把服务端的 achievementData 传入；
- 重同步时按 changedDomains 更新；
- 断线重连时将其纳入缺失域检查。

## 8. 第六步：创建客户端 System 和 Register

### 8.1 System

AchievementSystem 面向 UI/View 或其他客户端逻辑提供接口：

~~~lua
AchievementSystem = BaseClass:DefineClass(
    "AchievementSystem",
    BaseSystem
)

function AchievementSystem:CSUnLockAchievement(achievementId)
    local packet = CSUnLockAchievement:New()
    packet:Pack({
        achievementId = achievementId,
    })

    -- 按项目 ClientEventNetwork / NetPacketManager 的约定发送。
    ClientEventNetwork:Send(packet)
end

function AchievementSystem:OnSCUnLockAchievement(result)
    if result == nil then
        return
    end

    if result.code == 0 then
        local model = GetMol("ClientPlayerData")
        local data = model and model.achievementData
        if data ~= nil and result.data ~= nil then
            data:ApplyServerData(result.data)
        end
    end
end
~~~

具体包的构造方式可能是 New、Create 或由网络管理器创建，必须以模板现有协议包示例为准。这里最重要的是调用方向：System 发请求，回包处理函数更新 Model。

### 8.2 Register / Host Script

AchievementSystemRegister.lua 负责：

- 创建 AchievementSystem；
- 注册到客户端 IOC；
- 注册 S2C Handler；
- 接收 Awake、OnDestroy 等生命周期；
- 在销毁时注销监听器和 IOC 实例。

业务调用处通过 IOC 获取：

~~~lua
local achievementSystem = GetSys("AchievementSystem")
achievementSystem:CSUnLockAchievement(achievementId)
~~~

包含裸生命周期函数的 *Register.lua 是 Host Script，应由框架自动挂载。不要再从 Client/System/index.lua 手动重复 require，避免系统和监听器重复创建。

## 9. 成就 Demo 的联调顺序

建议按以下顺序联调，能够快速定位问题所在层：

1. 先用固定请求确认客户端能发出 C2S；
2. 服务端打印 playerOpenId 和 achievementId，确认 Handler 被触发；
3. 检查 ServerPlayerDataManager.Get(openId) 是否返回聚合根；
4. 检查 ServerAchievementData:IsLoaded()；
5. 在 Create/Update 后检查数据域是否 IsDirty()；
6. 检查 Manager 是否发出 S2C，回包 code 是否为 0；
7. 客户端检查 OnSCUnLockAchievement 是否触发；
8. 检查 ClientAchievementData 是否更新；
9. 离开房间或等到 Flush 后重新进入，确认云端数据仍存在；
10. 断线重连，确认版本号和 changedDomains 能触发该域重同步。

## 10. 新增业务的八项速查

### Common

- [ ] NetPacketType.lua 增加 C2S/S2C；
- [ ] 新建 C2S、S2C BaseNetPacket 子类；
- [ ] 在 Common/NetworkPacket/index.lua 统一注册。

### Server

- [ ] 新建 Server<Name>Data.lua；
- [ ] 实现默认值和 NormalizeValue；
- [ ] 新建 Server<Name>Manager.lua；
- [ ] 注册 C2S Handler；
- [ ] 修改 ServerPlayerData 的创建、加载、首包、重同步、Flush；
- [ ] ServerDataCache.versionedDomains 加入新域。

### Client

- [ ] 新建 Client<Name>Data.lua；
- [ ] 修改 ClientPlayerData 的创建、销毁和首包/重同步；
- [ ] 新建 *System.lua；
- [ ] 新建 *SystemRegister.lua；
- [ ] 注册 S2C Handler；
- [ ] 使用 GetSys、GetMol 获取 System 和 Model。

### 质量检查

- [ ] 客户端不能决定最终奖励或解锁结果；
- [ ] 服务端修改使用数据域接口并正确标脏；
- [ ] 首包、Flush、离房、重同步四条路径都覆盖；
- [ ] 重复请求具有幂等性；
- [ ] 错误码和日志能区分参数错误、未加载和业务拒绝。

