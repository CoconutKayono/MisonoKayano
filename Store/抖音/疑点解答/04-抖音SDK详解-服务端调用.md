# 抖音虚拟世界 SDK 详解（四）：如何调用服务端

> 面向对象：抖音虚拟世界创作者、服务端/客户端程序员
> 定位：讲透"抖音虚拟世界里到底有没有服务端、怎么从客户端调服务端、能传什么"，并给出与**自建外部服务端**对接的可行性判断，附 Unity 支持/禁止清单。
> 关联资料：《抖音虚拟世界开发模式简介》《Dedicated Server 开发模式详解》《消息互通》《同步变量》《接入方式》《SDK API白名单/黑名单》。

---

## 目录

1. [先搞清楚：抖音虚拟世界有几种"服务端"？](#1-先搞清楚)
2. [模式一：Shared Mod（无业务服务端）](#2-模式一shared-mod)
3. [模式二：Dedicated Server（DS，真正的服务端）](#3-模式二dedicated-server)
4. [DS 客户端→服务端通信：RemoteEvent / RemoteFunction](#4-客户端→服务端通信)
5. [通信参数类型限制（非常重要）](#5-通信参数类型限制)
6. [能对接"我们自己部署的外部 HTTP 服务"吗？](#6-能对接外部服务吗)
7. [完整示例：服务端统一下发动作指令](#7-完整示例)
8. [何时用同步变量、何时用 DS 通信、如何实现状态同步](#8-何时用同步变量-何时用-ds-通信-如何实现状态同步)
9. [Unity 支持 / 禁止清单（网络相关）](#9-unity-支持--禁止清单)
10. [常见误区与避坑](#10-常见误区与避坑)
11. [官方参考文档索引](#11-官方参考文档索引)

---

## 1. 先搞清楚：抖音虚拟世界有几种"服务端"？

| 模式                       | 逻辑运行位置                                     | 是否有"业务服务端"     | 判断 API                                               |
| ------------------------ | ------------------------------------------ | -------------- | ---------------------------------------------------- |
| **Shared Mod**           | 逻辑跑在**每个客户端**；房间服务器只做**转发 + 数据存储**，不参与业务计算 | ❌ 无（房主/主权分散执行） | 无                                                    |
| **Dedicated Server（DS）** | 引入**官方托管的独立服务端进程**，运行服务端脚本                 | ✅ 有            | `DouyinApplication.isServer`、`DouyinPlayer.isServer` |

> ⚠️ **只有 DS 模式存在"真正的服务端脚本"**。Shared Mod 下你感知不到"服务端"，只能通过消息互通/同步变量做玩家间同步。

DS 模式开启方式（《Dedicated Server 开发模式详解》）：

1. 场景建 `DouyinServerRoot` 空节点（下挂服务脚本）。
2. 挂 `DouyinServerScriptLoader`（服务端专用脚本，**客户端不可见**）。
3. `DouyinScriptLoader` 里的脚本两端都能用；两者互斥，不能放同一脚本。
4. `DouyinServerRoot` 下不允许挂 Canvas。

**DS 服务端脚本的生命周期与房间生命周期一致**（最后一名玩家退出房间，服务端脚本随之结束）。

---

## 2. 模式一：Shared Mod

Shared Mod 下所有玩法逻辑在客户端执行，靠**消息互通（RPC）**和**同步变量**维持多端一致。

| 手段 | API | 特点 |
| --- | --- | --- |
| 消息互通（RPC） | `DouyinScript.SendMessageToAll / SendMessageToTarget / SendMessageToOwner`、`OwnerCall / TargetCall` | 事件驱动、即时发送、**不保证一定到达**；参数为基础类型 |
| 同步变量 | `---@varSync` 声明，`SetValue / GetValue / OnValueChange` | 持续状态值，定时同步（约 70–120ms），**只有主权方可修改**；断线重进后拉最新值 |

```lua
-- 广播给所有人（含自己），接收方自动调用同名函数
self:SendMessageToAll("SyncAnimation", actorID, actionId)
```

> 💡 想实现"某个玩家/物体说了算"：用**主权**（Ownership）概念 —— `HasOwnership / RequestOwnership / SetOwner / SendMessageToOwner / OwnerCall`。

---

## 3. 模式二：Dedicated Server（DS）

DS 引入官方托管的独立服务端，适合强竞技、抽奖、排行榜、商业化等需要服务端校验的玩法。

关键特性（《抖音虚拟世界开发模式简介》）：

- 服务端运行**服务端脚本**（`DouyinServerRoot` 节点下的对象）与**客户端脚本**（其他脚本）；客户端**只运行客户端脚本**。
- 服务端脚本与服务器对象对客户端**完全不可见**，核心参数无法被客户端读取或篡改。
- 房间内公共对象主权由**服务端**持有（玩家角色 Actor 除外）。
- 服务端允许创建公共对象，也允许创建**服务端专属对象**（`ServerSpawn`，客户端不可见）。
- DS 模式下**数据存储必须写在服务端脚本**，客户端调数据存储 API 会报 **-11002** 错误。

---

## 4. 客户端→服务端通信

DS 模式下客户端与服务端通信，使用平台提供的两个类：

### 4.1 `DouyinRemoteEvent` —— 异步单向（不需要响应）

| 方向 | 方法 / 事件 |
| --- | --- |
| 客户端 → 服务端 | `FireServer(object[] args)`；服务端监听 `onServerEvent` |
| 服务端 → 指定客户端 | `FireClient(DouyinPlayer player, object[] args)`；客户端监听 `onClientEvent` |
| 服务端 → 所有客户端 | `FireAllClients(object[] args)` |

```lua
-- 客户端：发起请求
ClientToServerEvent:FireServer(actor.actorID)

-- 服务端：接收
ClientToServerEvent.onServerEvent:AddListener(function(player, args)
    -- player 为发起请求的 DouyinPlayer
end)
```

### 4.2 `DouyinRemoteFunction` —— 双向（带响应）

| 方向       | 方法 / 事件                                                                                                            |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| 客户端调用服务端 | `InvokeServer(Action<object[]> response, object[] args)`；服务端监听 `onServerInvoke`                                    |
| 服务端调用客户端 | `InvokeClient(DouyinPlayer player, Action<DouyinPlayer, object[]> response, object[] args)`；客户端监听 `onClientInvoke` |

```lua
-- 客户端：请求并处理响应
CSToCFunction:InvokeServer(function(...)
    local resp = {...}
    print("服务端返回", unpack(resp))
end, "参数1", "参数2")

-- 服务端：接收并返回结果
CSToCFunction.onServerInvoke:AddListener(function(player, ...)
    return "Server-Response-1", "Server-Response-2"   -- 返回值给客户端
end)
```

### 4.3 使用注意（官方 FAQ）

1. **不保证 100% 送达**：两者均基于 TCP，但发送方不等待确认；接收方断线/重连时平台**不补发**。
2. **不要**在方法内部定义 `DouyinRemoteEvent / DouyinRemoteFunction` 局部变量 —— 被 GC 回收时监听会被移除，异步回调会报 nil。
3. 用 `Dispose()` 清理；`OnDestroy` 里 `RemoveListener` + `Dispose`。
4. RemoteEvent/RemoteFunction **只用于 DS 模式**。

---

## 5. 通信参数类型限制（非常重要）

| 限制          | 说明                                                              |
| ----------- | --------------------------------------------------------------- |
| **支持的类型**   | `bool, byte, short, int, long, float, double, string` 等**基础类型** |
| **不支持的类型**  | `table`（Lua 表）、对象、`byte[]` 数组、`AnimationClip`、`GameObject` 等    |
| **多参数**     | 可通过 Lua 可变参数（`...`）传多个基础类型数据                                    |
| **复杂数据怎么办** | 拼成 JSON 字符串（`dkjson.encode`）在服务端 `dkjson.decode` 还原             |

> ⚠️ **结论：跨端通信传不了资源对象，也传不了复杂结构体。** 服务端能下发的是**标识/数值/字符串**，客户端拿到后在本地解析执行。这正是"服务端下发动作 ID、客户端播本地动画"架构成立的前提。

---

## 6. 能对接外部服务吗

> 问题：能不能让抖音客户端直接请求**我们自己部署的外部 HTTP 服务**？

**❌ 不能。** 依据：

- SDK 中**没有**任何 HTTP/WebRequest 服务类（无 `DouyinHttpService` 等）。
- `UnityEngine.Networking`（`UnityWebRequest`）被黑名单**整体禁止**。
- 文档中所有"服务端"概念均指**平台 DS 服务端进程**，不开放任意外网请求。

**可行替代思路：**

| 诉求              | 是否可行  | 做法                                                            |
| --------------- | ----- | ------------------------------------------------------------- |
| 客户端直连自建 HTTP 服务 | ❌     | 无通道                                                           |
| 逻辑收敛到平台 DS 服务端  | ✅     | 客户端 → `FireServer/InvokeServer` → 服务端处理 → 广播                  |
| 外部系统数据进入世界      | ⚠️ 有限 | 需平台能力支持或人工/后台配置；脚本内无外网通道                                      |
| 商业化（充值/发货）      | ✅ 走官方 | `DouyinMarketingService`（官方商业 API），DS 下监听 `onOrderPayment` 发货 |

---

## 7. 完整示例：服务端统一下发动作指令

> 需求：服务端决定"玩家能播什么动作"，客户端只负责播放。这正是"客户端调用服务端动作资源"的官方可行形态（资源在本地，指令在服务端）。

```lua
-- ============ 服务端（DS 脚本）============
local ServerToClientEvent = DouyinRemoteEvent("ServerToClient")
local ClientToServerFunc   = DouyinRemoteFunction("ClientToServer")

-- 客户端请求动作，服务端校验后广播
ClientToServerFunc.onServerInvoke:AddListener(function(player, actionId)
    if CheckAction(actionId, player) then               -- 服务端校验
        ServerToClientEvent:FireAllClients(actionId)     -- 广播动作 ID
    end
end)

-- ============ 客户端 ============
-- 请求服务端授权播放动作
ClientToServerFunc:InvokeServer(function(...) end, actionId)

-- 收到广播 → 查本地动作表 → 播放
ServerToClientEvent.onClientEvent:AddListener(function(actionId)
    local clip = LocalActionTable[actionId]              -- 本地已打包的动画
    if clip then
        DouyinActorService.GetLocalActor():PlayAnimation(clip)
    end
end)
```

动作表（客户端）用 Lua 表维护：`{ [动作ID] = 本地动画引用 }`（详见《角色动画》与《本地JSON与数据格式》文档）。

---

## 8. 何时用同步变量、何时用 DS 通信、如何实现状态同步

> 三种网络能力是不同层次的"语法糖"：同步变量 = 数据容器自动同步；RPC = 客户端间消息；RemoteEvent = C↔S 调用；网络对象 = 物体级状态复制。本节回答"该选哪个 + 状态同步怎么做"。

### 8.1 一图决策

| 需求                   | 用哪种                          | 理由                 |
| -------------------- | ---------------------------- | ------------------ |
| 持续状态值（血量/得分/道具数量）    | 同步变量                         | 自动同步、最终一致、断线重进拉最新  |
| DS 客户端提交指令 / 服务端下发结果 | RemoteEvent / RemoteFunction | C↔S 直连，只用于 DS      |
| 客户端间临时通知             | RPC（SendMessageToXXX）        | 次要通知，非核心业务         |
| 高频角色模型位置/动画          | ❌ 网络对象                       | 底层不保证可靠、易卡顿；应做状态同步 |

### 8.2 同步变量在 DS 模式的使用边界

- 挂在**公共网络对象**（客户端可见）→ 同步变量自动同步到所有客户端，主权方（DS 下通常是服务端）`SetValue`，客户端 `OnValueChange`。
- 挂在**服务器对象**（`DouyinServerRoot` 下 / `ServerSpawn`，客户端不可见）→ **不会同步到客户端**（《Dedicated Server 开发模式详解》FAQ#6），要用 RemoteEvent。

```lua
-- 公共对象上的同步变量（服务端持主权）
---@varSync hp:int
---@varSync score:int
---@end

-- 服务端：只有主权方能写
function SetHp(v)
    if not self:HasOwnership() then return end
    hp:SetValue(v)
end

-- 任意客户端：监听变化
function OnNetSpawned()
    hp:OnValueChange(function(cur, pre) UpdateHpBar(cur) end)
    score:OnValueChange(function(cur, pre) RefreshScore(cur) end)
end
```

> 注意：同步变量是 70–120ms 定时同步，不适合逐帧位置；适合低频状态值。

### 8.3 何时用 DS 通信（RemoteEvent / RemoteFunction）

客户端→服务端的操作请求、服务端→客户端的广播结果用 RemoteEvent/RemoteFunction（详见 [4. 客户端→服务端通信](#4-客户端→服务端通信) 与 [7. 完整示例](#7-完整示例)）。它事件驱动、实时，但**不保证 100% 送达**，参数只能传基础类型。

### 8.4 状态同步完整示例：自定义角色模型的位置 + 动画

> 场景：不使用官方 Actor，用自定义模型；要同步模型的**位置 + 旋转 + 动画**。做法：模型是**客户端本地对象**（`Instantiate`，不是网络对象），服务端只广播**状态数据**，客户端据此本地渲染。

```lua
-- ============ 服务端（DouyinServerRoot 脚本）============
local S2CState = DouyinRemoteEvent("S2CState")      -- 服务端→客户端 状态广播
local C2SInput = DouyinRemoteFunction("C2SInput")   -- 客户端→服务端 输入请求

-- 客户端提交移动/动作，服务端校验后广播给所有客户端
C2SInput.onServerInvoke:AddListener(function(player, px, py, pz, rx, ry, rz, animID)
    if not CheckValid(player, px, py, pz) then return end   -- 服务端权威校验
    S2CState:FireAllClients(player.playerID, px, py, pz, rx, ry, rz, animID)
end)
```

```lua
-- ============ 客户端 ============
local modelMap = {}   -- playerID -> 本地模型实例（Instantiate 出来的本地对象）

-- 客户端把操作发给服务端
C2SInput:InvokeServer(function() end, px, py, pz, rx, ry, rz, animID)

-- 收到服务端广播 → 更新所有玩家（含自己）的本地模型
S2CState.onClientEvent:AddListener(function(playerID, px, py, pz, rx, ry, rz, animID)
    local model = modelMap[playerID]
    if model == nil then return end
    model.transform.position = UnityEngine.Vector3(px, py, pz)
    model.transform.eulerAngles = UnityEngine.Vector3(rx, ry, rz)
    local animator = model:GetComponent(typeof(UnityEngine.Animator))
    if animator ~= nil and animID ~= model.curAnim then
        animator:Play(animID)
        model.curAnim = animID
    end
end)
```

要点：
1. **模型是本地对象**，动画由本地 `Animator` 播放，天然顺滑，彻底避开网络对象卡顿。
2. **参数拆基础类型**：位置 3 个 float、旋转 3 个 float（欧拉角）、动画用 int/string；RemoteEvent 不能传 table/Vector3。
3. **不要逐帧广播**：10–20Hz + 客户端插值；动画用事件驱动（状态变化才发）。
4. 服务端必须做**权威校验**（`CheckValid`），不能直接信任客户端坐标，否则形同 Shared。

### 8.5 为什么不推荐网络对象做角色

网络对象 = 物体级状态复制，`NetSpawn` 动态对象不销毁会残留、断线重连不触发 `OnNetSpawned`、底层不保证可靠（网络差时部分玩家看不到对象）。角色模型这种高频更新的实体，用它会卡顿。正确做法就是 8.4 的状态同步：**只同步数据，客户端本地渲染**。

> 补充三点，把“物体级复制”和“为什么状态同步更抗丢”讲透：

**① “物体级复制”到底复制什么？**
网络对象不会在运行时把模型/mesh/贴图资源通过网络传输——资源必须提前打进 AssetBundle（网络对象生成配置里注册好 prefab）。它复制的是**对象实例本身**：每个客户端都有一份 GameObject 实例，并且 transform/刚体/同步变量等**状态自动同步**，不用手写推送。

| 机制 | 传什么 | 客户端拿到什么 |
| --- | --- | --- |
| 网络对象 | 对象实体 + 状态 | 每个端各一份对象实例，状态自动一致 |
| 同步变量 | 数据 | 挂在网络对象上，数值自动同步 |
| RemoteEvent | 数据（基础类型） | 收到后自行处理，不产生新对象 |

**② 为什么状态同步在弱网下对象仍可见？**
不是 RemoteEvent 比网络对象更可靠（两者都基于 TCP、都不保证 100% 到达），而是“对象实例的存在”依赖不同：
- 网络对象：动态对象靠 `NetSpawn` 的创建消息让其他端实例化；创建时丢包 → 该端根本没有实例；且**断线重连不触发 `OnNetSpawned`**，不会补建 → 永久看不到。
- 状态同步：模型是客户端本地 `Instantiate` 的**本地对象**，不依赖网络创建；网络只喂状态数据，丢一条只是这一帧没更新，对象始终可见。

**③ 同步变量只能作用于网络对象吗？——是**
同步变量用 `---@varSync` 写在 Douyin Script 里，而挂 Douyin Script 的对象会自动加 DouyinNetworkGuid，本身就是网络对象；纯本地对象（Instantiate 的本地模型）挂不了同步变量，SDK 网络接口与同步变量都不执行。DS 下还有一层：服务器对象也是网络对象，但它的同步变量**不下发客户端**，跨端要 RemoteEvent。

记忆口诀：**同步变量 = 挂在网络对象上的自动同步数据槽；没有网络对象就没有同步变量。**

---

## 9. Unity 支持 / 禁止清单（网络相关）

| 能力                                                            | 状态   | 说明                                       |
| ------------------------------------------------------------- | ---- | ---------------------------------------- |
| `UnityEngine.Networking`（`UnityWebRequest`、`DownloadHandler`） | ❌ 禁止 | 黑名单整体禁用                                  |
| `System.Net`（`HttpWebRequest`、`Socket` 等）                     | ❌ 禁止 | 未在白名单，且 `System` 网络类型不可访问                |
| `System.IO`（文件/流）                                             | ❌ 禁止 | 黑名单                                      |
| 反射加载程序集/类型                                                    | ❌ 禁止 | 黑名单（`Assembly.Load*`、`CreateInstance` 等） |
| 平台 RPC：`SendMessageToAll/Target/Owner`、`OwnerCall/TargetCall` | ✅ 支持 | Shared Mod / 客户端间                        |
| 平台同步变量：`---@varSync` + `SetValue/GetValue/OnValueChange`      | ✅ 支持 | 状态同步                                     |
| 平台 DS 通信：`DouyinRemoteEvent` / `DouyinRemoteFunction`         | ✅ 支持 | 仅 DS 模式，C↔S 双向                           |
| `DouyinApplication.isServer` / `DouyinPlayer.isServer`        | ✅ 支持 | 判断当前环境                                   |
| 官方商业化：`DouyinMarketingService`                                | ✅ 支持 | 充值、下单、发货（DS 侧监听支付事件）                     |

---

## 10. 常见误区与避坑

1. **误区：Shared Mod 也有服务端脚本** —— 没有，只有 DS 模式才有独立服务端进程。
2. **误区：RemoteEvent 一定能送达** —— 不保证，接收方断线不补发。
3. **误区：能传 table / 对象 / 二进制** —— 只能传基础类型；复杂数据用 JSON 字符串。
4. **误区：客户端能直连外部 HTTP 服务** —— 不能，`UnityWebRequest` 被禁。
5. **避坑：DS 数据存储只能在服务端** —— 客户端调数据存储 API 报 -11002。
6. **避坑：别在方法内定义 RemoteEvent/RemoteFunction** —— GC 会导致回调 nil。
7. **避坑：DS 服务端只能启动一个** —— 重复启动会顶掉之前的服务端。

---

## 11. 官方参考文档索引

- 创作文档：《抖音虚拟世界开发模式简介》《Dedicated Server 开发模式详解》《消息互通》《同步变量》《接入方式》《主权》
- API：`DouyinRemoteEvent.*`（`FireServer / FireClient / FireAllClients / onServerEvent / onClientEvent`）；`DouyinRemoteFunction.*`（`InvokeServer / InvokeClient / onServerInvoke / onClientInvoke`）；`DouyinApplication.isServer`；`DouyinPlayer.isServer`；`DouyinObjectService.ServerSpawn / ServerDestroy`；`DouyinScript` 消息互通系列；`DouyinMarketingService`
- 规则：《SDK API白名单》《SDK API黑名单》
