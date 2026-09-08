# DSTemplate 模板框架与 Scripts 目录说明

本文档根据新增的 DSTemplate 模板说明资料整理，用于帮助创作者理解 `Assets/DSTemplate` 的职责边界、双端分层、脚本加载方式和常见扩展入口。

## 1. DSTemplate 是什么

`DSTemplate` 是一套面向 Dedicated Server（DS）开发的玩法模板。它提供：

- Common 共享层：协议、网络包、Lua OOP、工具和配置；
- Server 服务端层：权威业务、玩家数据聚合、数据域、DataStore 落盘、状态机；
- Client 客户端层：系统、界面、客户端数据镜像、网络回包和表现；
- 网络对象、Buff、事件消息、商业化等可复用基础模块；
- 成就系统等端到端 Demo，用于演示如何新增一条业务。

模板中的 `AchievementSystem`、`ServerAchievementData`、`ServerAchievementManager` 和 `ClientAchievementData` 是参考 Demo，不代表模板必须具备的正式业务。它的价值在于完整演示“新增一个数据域 + 一对协议 + 一个客户端 System”的接入过程。

## 2. 双端分层

### 2.1 服务端四层

服务端推荐调用方向为：

```text
协议层 → Logic / Manager → Data / 聚合根 → DataStore
```

各层职责如下：

| 层               | 主要职责                   | 不应承担的职责                 |
| --------------- | ---------------------- | ----------------------- |
| 协议层             | 收包、参数初步解析、转发到 Manager  | 直接读写 DataStore、实现完整业务规则 |
| Logic / Manager | 权威校验、业务规则、调用数据域、组装回包   | 绕过 Data 域直接操作 KV        |
| Data / 聚合根      | 玩家数据域的内存快照、脏标记、加载和保存协调 | 直接向客户端发业务包              |
| DataStore       | 云端 KV 读写、JSON 序列化      | 处理玩法规则                  |

协议层不直接读写数据，Logic 不直接打 KV，Data 不负责发包。如果出现跨层调用，通常说明逻辑应该移动到对应的 Manager 或聚合根。

### 2.2 客户端三层

客户端调用方向为：

```text
协议层 → Logic / System → Data / Client Model
```

客户端没有 DataStore 层。`ClientPlayerData` 和各个 `Client*Data` 只是服务端权威数据的内存镜像：

```text
客户端写请求 → C2S → 服务端校验并修改 → 服务端 Save / Flush
           → SC 回包 → 客户端覆写本地镜像
```

客户端不要把本地 Model 当作持久化数据库，也不要在客户端直接写入最终权威数据。

## 3. Scripts 目录职责

典型目录结构如下：

```text
Assets/DSTemplate/Scripts/
├─ Common/
│  ├─ Config/                  # 表格导出后的配置访问类
│  ├─ Core/OOP/                # BaseClass 等 Lua OOP 基础设施
│  ├─ NetworkPacket/           # 协议类型、Pack/Unpack、协议包
│  └─ Utility/                 # Json、ServerUtils、打印等双端工具
├─ Server/
│  ├─ Data/                    # Server*Data 数据域和玩家聚合根
│  ├─ DataStore/               # ServerDataCache、ServerDataStoreManager
│  ├─ Logic/                   # 玩法 Manager、状态机、Buff 服务端实现
│  ├─ Network/                 # ServerEventNetwork、C2S 注册
│  └─ GameServerModule.lua     # DS 宿主入口和房间生命周期
└─ Client/
   ├─ Model/                   # Client*Data 纯内存数据域和聚合根
   ├─ Network/                 # ClientEventNetwork、S2C 注册
   ├─ System/                  # 客户端业务 System 和 Register 宿主脚本
   ├─ View/                    # UI 表现与输入采集
   └─ Framework/               # IOC、System 基类等客户端框架
```

### 3.1 Common

`Common` 由 Client 和 Server 共享，必须先于双端业务模块加载。

关键入口：

- `Common/NetworkPacket/NetPacketType.lua`：协议类型枚举和扩展注册入口；
- `Common/NetworkPacket/NetPacketManager.lua`：协议包创建、序列化后分发和 Handler 注册；
- `Common/NetworkPacket/BaseNetPacket.lua`：所有自定义协议包的基类；
- `Common/Core/OOP/BaseClass.lua`：`BaseClass:DefineClass("ClassName")`；
- `Common/Config/`：由表格生成或维护的配置访问类；
- `Common/Utility/`：JSON、日志、打印等工具。

新增协议时不要再创建并行的 `GameNetPacketType.lua`。应在 `NetPacketType` 的内置表或 `RegisterExtensions` 中统一登记。

### 3.2 Server

服务端入口 `GameServerModule.lua` 负责：

1. `Start` 中初始化网络和服务端模块，并注册 C2S Handler；
2. `Update` 中执行数据 Flush 节拍和游戏逻辑 Tick；
3. 将玩家加入、重连、离开转发给玩家数据管理器和游戏逻辑管理器；
4. `OnDestroy` 中清理网络和商业化模块。

服务端通常通过 `JudgeIsServer()` 或 `DouyinApplication.isServer` 做入口闸门，因为同一套脚本可能在双端环境中被加载。

### 3.3 Client

客户端不是通过一个统一的服务端式入口运行所有业务，而是由各系统的 `*Register.lua` 作为 Host Script 接收生命周期：

```text
Awake / Start / Update / OnDestroy / OnPlayerJoined / OnActorSpawned ...
```

业务类一般是 `*System.lua`，Host Script 一般是 `*SystemRegister.lua`：

- `*System.lua`：继承 `BaseSystem`，放业务方法；
- `*SystemRegister.lua`：创建 System、注册到 IOC、处理生命周期；
- `Client/System/index.lua`：只 require 业务类定义，不 require Host Script。

## 4. require 与 Host Script 规则

### 4.1 普通 Lua 模块

没有裸生命周期函数的类、配置、工具和协议模块，应通过对应的 `index.lua` 加载：

```lua
require "Common.index"
require "Client.index"
require "Server.index"
```

### 4.2 Host Script

包含以下裸函数的脚本由框架自动挂载，不应在 `index.lua` 中重复 require：

```lua
Awake
Start
OnEnable
Update
LateUpdate
FixedUpdate
OnDestroy
OnActorSpawned
OnPlayerJoined
OnPlayerLeft
```

典型 Host Script 包括：

- `GameServerModule.lua`；
- `*SystemRegister.lua`；
- `NetworkBuff.lua`；
- `NetworkBuffManager.lua`；
- `NetworkObject.lua`。

重复 require Host Script 可能导致监听器、全局单例或 Update 逻辑被重复注册。

## 5. IOC 使用约定

客户端 IOC 分为 System 和 Model 两类：

```lua
IOCContainer:Register("AchievementSystem", system)
IOCContainer:RegisterModel("ClientPlayerData", playerData)
```

业务层通过全局便利函数获取：

```lua
local system = GetSys("AchievementSystem")
local playerData = GetMol("ClientPlayerData")
```

不要在业务脚本之间长期保存其他 System 或 Model 的实例引用。应通过 `GetSys` / `GetMol` 获取，以便断线重连、玩家数据重建和系统销毁时保持引用有效。

## 6. 推荐开发顺序

新增一条业务时，建议按以下顺序执行：

1. 先确定服务端权威数据和客户端展示数据；
2. 设计 C2S / S2C 协议及 `packet.data` 结构；
3. 创建服务端 Data 域和 `NormalizeValue`；
4. 创建服务端 Manager，完成校验和聚合数据修改；
5. 接入 `ServerPlayerData` 的加载、首包、重同步、Flush；
6. 创建客户端 Data 域；
7. 创建客户端 System 和 Host Script；
8. 接入 `ClientPlayerData`、`PlayerSystem` 和协议回包；
9. 补齐各层 `index.lua` 和双端 Handler 注册；
10. 最后再接入 UI、特效、商业化或 Buff 表现。

## 7. 相关文档

- [DSTemplate数据存储详解](DSTemplate数据存储详解.md)
- [DSTemplate业务系统接入指南](DSTemplate业务系统接入指南.md)
- [DSTemplate Buff系统接入指南](DSTemplate%20Buff系统接入指南.md)
- [DSTemplate商业化系统接入指南](DSTemplate商业化系统接入指南.md)
