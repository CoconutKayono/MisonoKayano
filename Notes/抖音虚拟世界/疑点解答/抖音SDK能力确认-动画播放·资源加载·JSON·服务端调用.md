# 抖音虚拟世界 SDK 能力确认

> 背景：策划询问"抖音平台能否在客户端调用我们服务端的动作资源"。本文基于抖音官方 Wiki 文档（`虚拟世界创作文档`）与 API 参考手册（`虚拟世界API参考`）整理，逐条确认以下四个问题：
>
> 1. 抖音 SDK 如何播放角色动画
> 2. 抖音 SDK 如何进行资源加载
> 3. 抖音 SDK 能否加载本地 JSON 文件
> 4. 抖音 SDK 如何调用服务端
>
> 并在此基础上给出对"客户端调用服务端动作资源"这一需求的结论与可行方案。

---

## 〇、结论速览（TL;DR）

| 问题               | 结论                                                                                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 播放角色动画           | 通过 `DouyinActor.PlayAnimation / StopAnimation / SetOverrideAnimation / SetOverrideAnimationController` 播放，动画对象（`AnimationClip`）是**随世界包分发、编辑器内配置好的资源**，运行时传入引用即可 |
| 资源加载             | **不支持** `Resources.Load` 动态加载资源；资源统一由云构建打进 AssetBundle，随世界包发布；运行时只能通过平台 API（如 `NetSpawn`）实例化**预先配置好**的 Prefab/网络对象                                              |
| 加载本地 JSON        | 没有面向业务脚本的"任意本地 JSON 文件加载"API；`System.IO`、`UnityWebRequest` 均被黑名单禁用。JSON 只能用于**序列化/反序列化字符串**（`dkjson` / `Json`），配置数据通常以 Lua 脚本形式组织                               |
| 调用服务端            | **Dedicated Server（DS）模式下**可用 `DouyinRemoteEvent`（单向）与 `DouyinRemoteFunction`（双向）做客户端↔服务端通信；参数仅支持基础类型，**不支持传资源对象**                                              |
| **客户端调用服务端动作资源** | **不可行（不能运行时从服务端拉取动画资源）**。可行替代：服务端下发"动作 ID/名称"指令，客户端用**本地已随包分发的动画**播放；即"服务端发指令、客户端播本地资源"                                                                         |

---

## 一、抖音 SDK 如何播放角色动画

### 1.1 相关 API（均挂在 `DouyinActor` 上）

| API | 说明 | 关键签名 |
| --- | --- | --- |
| `PlayAnimation` | 播放一个动作，支持 Animation Event 回调 | `PlayAnimation(Animation clip, Action<AnimationEvent> cb = null, DouyinAnimatorMask mask = WholeBody)` |
| `StopAnimation` | 停止播放动作 | `StopAnimation(DouyinAnimatorMask mask = WholeBody)` |
| `SetOverrideAnimation` | 重载某个动作（可替换某个动画槽位），传 `nil` 还原 | `SetOverrideAnimation(string key, AnimationClip clip, Action<AnimationEvent> callback = null)` |
| `SetOverrideAnimationController` | 重载整个动画状态机（最复杂、自由度最高） | `SetOverrideAnimationController(RuntimeAnimatorController animatorController)` |
| `PlayEmoji` | 播放表情 | `PlayEmoji(int emojiIndex)` |
| `SetAnimationEvent`（DouyinScript） | 给指定动画剪辑设置 Animation Event 回调 | `SetAnimationEvent(AnimationClip clip, Action<AnimationEvent> callback)` |

相关事件（用于监听动作/表情播放）：`onActionPlay`、`onEmotionPlay`、`onActorLoaded`、`onDuoInteractionStart/End/Waiting` 等。

相关开关：`DouyinPlayerSettings.allowAction`（是否允许动作功能，默认 true）、`DouyinPlayerSettings.allowEmotion`（是否允许表情功能）。

### 1.2 关键要点

1. **动画对象是资源引用，不是字符串。** `PlayAnimation` 的第一个参数类型为 `Animation` / `AnimationClip`，即动画剪辑**必须在编辑器中配置好，作为资源随世界包分发**。运行时把剪辑引用传给 API 即可播放。
2. **`DouyinAnimatorMask` 控制影响部位**：`WholeBody / Head / UpperBody / LowerBody / Arms / LeftArm / RightArm / LeftHand / RightHand`，可只播上半身动作（如边走边挥手）。
3. **Animation Event 回调**：支持在动画播放到特定时刻触发回调。注意官方文档特别说明：Event 里填写的 Function 名称不会起作用，**所有 Event 都会触发传入的回调函数**，回调中可读取 Event 的其他参数。
4. **三种动作控制方式**（官方文档《合养精灵动作》归纳）：
   - **播放**：`PlayAnimation` / `StopAnimation` —— 让显示对象立刻播放/停止某个动作。
   - **重载动作**：`SetOverrideAnimation("proxy_Idle", 舞曲动画)` —— 把某个默认动作槽替换成新动画，传 nil 还原（官方舞池跳舞示例即此用法）。
   - **重载状态机**：`SetOverrideAnimationController(新 AnimatorController)` —— 完全替换动画逻辑，可做"全新的动作游戏"，配合 Unity 的 `AnimatorOverrideController` 使用。
5. **多人同步播放**：官方示例中，点击后通过 `self:SendMessageToAll("SyncAnimation", me.actorID)` 通知所有客户端，各客户端在自己的 `SyncAnimation(actorID)` 里对对应 Actor 调用 `actor:PlayAnimation(Animation)` —— 动画同步靠的是**消息互通把动作指令广播出去，各端本地播放**，而非网络传输动画本身。

### 1.3 官方示例（来自《合养精灵动作》）

```lua
-- 播放：点击后让房间内所有人看到该玩家播放动作
function PlayAnimation()
    local me = DouyinActorService.GetLocalActor();
    self:SendMessageToAll("SyncAnimation", me.actorID);   -- 广播动作指令
end
function SyncAnimation(actorID)
    local actor = DouyinActorService.GetActorById(actorID);
    actor:PlayAnimation(Animation);                       -- 各端本地播放
end

-- 重载动作（舞池跳舞）
function StartDance(actorID)
    local actor = DouyinActorService.GetActorById(actorID);
    actor:SetOverrideAnimation("proxy_Idle", NormalDance); -- 把待机替换为跳舞
end
function EndDance(actorID)
    local actor = DouyinActorService.GetActorById(actorID);
    actor:SetOverrideAnimation("proxy_Idle", nil);         -- 还原
end
```

---

## 二、抖音 SDK 如何进行资源加载

### 2.1 核心结论：不支持动态加载，资源随包分发

官方《支持动态加载资源吗？》原文：

> 问：是否可以使用 Unity 的 Resource.Load 来动态加载资源，进行版本更新。
> 答：**不可以**。目前世界上传的时候，云构建会生成 AssetBundle 资源包。对于创作者来说，**无法通过访问 Resources 目录，也就意味着无法使用 Resources.Load 来加载资源**。如果要对世界进行版本更新，需要重新走一遍发布世界的路线（上传新版本）。

即：**运行时不存在"按需下载/加载资源"的能力**。所有资源（模型、动画、Prefab、贴图等）在发布时由平台云构建打进 AssetBundle 随世界包下发到客户端。

### 2.2 资源在运行时如何使用

1. **场景内摆放**：静态资源直接在 Unity 场景中摆好，构建时随场景打包。
2. **网络对象动态生成**（多人可见的物体必须用平台 API）：
   - 在 `DouyinWorldRoot` 组件上配置 **Douyin Net Spawn Object Asset**（`key` → `GameObject`，GameObject 需挂网络同步组件 `Douyin Object Sync`）。
   - 运行时用 `DouyinObjectService.NetSpawn(string key, ...)` 以 **key** 实例化；销毁用 `NetDestroy`。
   - **不可使用 Unity 原生 `Instantiate` / `Destroy`** 动态创建/销毁网络对象（《抖音虚拟世界开发模式简介》明确要求）。
3. **DS 专属**：`DouyinObjectService.ServerSpawn` 在服务端生成对象，仅存在于服务端、不同步到客户端。
4. **场景流式加载**：开启流式能力后，`DouyinWorldRoot` 配置加载距离等参数，运行时通过 `DouyinStreamingService` 查询区域加载状态。但所有参数**构建期固化、运行时只读**，且**不能强制加载/卸载指定区域**。

### 2.3 运行时被禁用的资源/IO 相关能力

- `UnityEngine.Networking`（`UnityWebRequest`、`DownloadHandler`）—— **黑名单禁用**。
- `System.IO`、`System.Reflection.Emit`、`System.Runtime.InteropServices` —— **黑名单禁用**。
- Lua `io` 库、`os.execute / os.remove / os.rename` 等 —— **不可用**。
- `Resources.Load` —— 平台明确回复不可用。

### 2.4 对"用资源做版本更新"的含义

不能靠运行时下载新资源热更。版本更新 = 重新走发布流程、上传新版本，由平台分发。

---

## 三、抖音 SDK 能否加载本地 JSON 文件

### 3.1 直接回答：不能加载"任意本地 JSON 文件"

- 黑名单已禁用 `System.IO.File`、`io` 库等一切本地文件读取通道；`UnityWebRequest` 也被禁用，无法从本地或网络拉取文本。
- SDK 中与 JSON 沾边的 API 仅有场景环境配置：
  - `DouyinSceneEnvironment.JsonAsset`：返回场景效果参数配置表，"该对象**通过读取 json 文件获取**，并且**不能被创建成一个新类**"。
  - `DouyinSceneEnvironment.LoadJson(SceneEnvironmentSetting newSetting, bool load = true)`：加载一个 json asset 的数据对象，对**环境参数**进行配置。
  - 这是**引擎内部**用于加载场景效果配置（光照、雾、后处理等）的机制，不是给业务脚本加载任意 JSON 配置用的通用 API。

### 3.2 JSON 在 SDK 内实际可用在哪

1. **序列化/反序列化字符串**（运行时内存层面）：
   - 平台提供 `dkjson.encode()` / `dkjson.decode()`（见《数据存储详解》）；
   - 也有 `Json.Encode()` / `Json.Decode()` 封装。
   - 典型场景：把 Lua 表序列化成 JSON 字符串写入 DataStore，读回后再反序列化。
2. **配置数据的常规做法**：由于不能读本地文件，创作者通常把配置写在 **Lua 脚本**里（自定义脚本文件夹 + `require` 组织模块），`index.lua` 作为入口加载各配置模块（见《自定义 Module Script》）。

### 3.3 对"加载本地 JSON 动作配置"的含义

如果需求是"客户端读一份本地 JSON 来描述动作配置"，**原生不支持**。可行变通：把该配置写成 Lua 表（或先存 DataStore，运行时 `Json.Decode` 读成表），再映射到本地已分发的动画资源。

---

## 四、抖音 SDK 如何调用服务端

### 4.1 先厘清：平台有两种开发模式

| 模式 | 逻辑运行位置 | 是否真有"服务端" |
| --- | --- | --- |
| **Shared Mod** | 逻辑跑在各客户端，房间服务器只做转发/存储 | 无业务服务端（房主/分散主权执行） |
| **Dedicated Server（DS）** | 引入官方托管的独立服务端进程 | 有（`DouyinServerRoot` 节点 + `DouyinServerScriptLoader`） |

**只有 DS 模式存在真正的"服务端脚本"**。用 `DouyinApplication.isServer` / `DouyinPlayer.isServer` 判断当前环境。

### 4.2 DS 模式下客户端↔服务端通信

#### （1）`DouyinRemoteEvent` —— 异步单向

| 方向 | 方法 / 事件 |
| --- | --- |
| 客户端 → 服务端 | `FireServer(object[] args)`；服务端监听 `onServerEvent` |
| 服务端 → 指定客户端 | `FireClient(DouyinPlayer player, object[] args)`；客户端监听 `onClientEvent` |
| 服务端 → 所有客户端 | `FireAllClients(object[] args)` |

#### （2）`DouyinRemoteFunction` —— 双向（带响应）

| 方向 | 方法 / 事件 |
| --- | --- |
| 客户端调用服务端 | `InvokeServer(Action<object[]> response, object[] args)`；服务端监听 `onServerInvoke` |
| 服务端调用客户端 | `InvokeClient(DouyinPlayer player, Action<DouyinPlayer, object[]> response, object[] args)`；客户端监听 `onClientInvoke` |

#### （3）重要限制

- **参数仅支持基础类型**：`bool, byte, short, int, long, float, double, string` 等，**不支持 table 等复杂类型**（也就不能传 `AnimationClip` / `GameObject` 这类资源对象）。
- **不保证 100% 送达**：RemoteEvent / RemoteFunction 均基于 TCP，但发送方不等待确认，接收方断线/重连时平台不补发。
- **不要在方法内定义** RemoteEvent / RemoteFunction 局部变量，否则被 GC 回收时监听会被移除，异步回调会报 nil。
- DS 模式下**数据存储必须写在服务端脚本**，客户端调用数据存储 API 会报 -11002 错误。

### 4.3 非 DS 场景的"服务端"替代（Shared Mod）

即便不启用 DS，也可以实现类似"集中判定 + 广播"的玩法逻辑：

- **消息互通（RPC）**：`DouyinScript.SendMessageToAll / SendMessageToTarget / SendMessageToOwner`、`OwnerCall / TargetCall` —— 事件驱动、即时发送、不保证一定到达，参数同样为基础类型。
- **同步变量**：`---@varSync` 声明，`SetValue / GetValue / OnValueChange`；只有**主权方**能改，定时同步（70–120ms 延迟），断线重进后拉取最新值。适合血量、分数等持续状态。

### 4.4 没有"对外部 HTTP 服务"的调用能力

文档中**不存在** `DouyinHttpService` 或类似请求外网接口的 API；`UnityWebRequest` 被黑名单禁用。即：客户端脚本**不能**直接请求你们自建的外部服务端。

---

## 五、核心问题：客户端能否调用服务端的动作资源？

### 5.1 结论

**不能。** 抖音虚拟世界 SDK 不存在"客户端从服务端拉取/调用动作资源"的能力，理由如下：

1. **动作资源（AnimationClip）不通过网络传输**。动画在编辑器里配置、随世界包（AssetBundle）分发到客户端，运行时以资源引用传入 `PlayAnimation`。平台没有提供任何运行时下载/加载动画资源的 API（`Resources.Load` 禁用、`UnityWebRequest` 禁用）。
2. **服务端通信传不了资源**。`DouyinRemoteEvent` / `DouyinRemoteFunction` 的参数只支持基础类型，无法传递 `AnimationClip`、`GameObject` 等对象。服务端能下发的是**标识**（字符串 ID、整型枚举），不是资源本身。
3. **DS 服务端进程本身也不渲染**。服务端只是逻辑进程，动画播放始终发生在客户端本地。

### 5.2 可行的等价方案："服务端发指令，客户端播本地资源"

这其实就是官方推荐的动作同步范式（详见 1.2 节第 5 点），完全可以满足"由服务端控制动作播放"的诉求：

**方案 A —— DS 模式下，由服务端统一下发动作指令（推荐，服务端有校验权）：**

```lua
-- 客户端：请求服务端授权播放某个动作
CSToCFunction:InvokeServer(function(resp)
    -- 服务端校验通过后，各客户端收到的广播里播放
end, actionId)   -- actionId 为基础类型，如 int / string

-- 服务端：收到请求 → 校验 → 广播给所有客户端
function OnServerResponseHandle(player, actionId)
    if 校验通过(actionId, player) then
        ServerToClientEvent:FireAllClients(actionId)   -- 广播动作ID
    end
end

-- 客户端：收到动作ID → 用本地已打包的动画播放
function OnClientEventHandle(actionId)
    local clip = LocalActionTable[actionId]            -- 本地动画表
    if clip then
        DouyinActorService.GetLocalActor():PlayAnimation(clip)
    end
end
```

**方案 B —— Shared Mod 模式下，用消息互通广播动作（房主/主权方做判定）：**

```lua
-- 玩家A触发动作，广播给所有人
self:SendMessageToAll("SyncAnimation", actorID, actionId)
```

**方案 C —— 动作配置放服务端，动画资源放客户端：**

- 服务端（DS 脚本）维护"动作 ID → 动作名/参数"的配置表，需要更新配置时只需发布**服务端脚本**，客户端无需重新下载资源（前提是动画资源本身已在客户端包内）。
- 动作**资源本体**（新动画、新模型）仍无法运行时下发，只能走"重新发布世界新版本"。

### 5.3 给策划/项目的落地建议

| 诉求 | 可行性 | 做法 |
| --- | --- | --- |
| 服务端控制"什么时候/谁播放哪个动作" | ✅ 可行 | 服务端广播动作 ID，客户端本地播放 |
| 服务端下发动作 ID → 动画的映射配置 | ✅ 可行 | 映射表存服务端脚本 / DataStore，客户端按 ID 查本地动画表 |
| 服务端下发新的动画/模型资源（热更资源） | ❌ 不可行 | 只能重新发布世界新版本 |
| 客户端直连你们自己的外部服务端 | ❌ 不可行 | 无 HTTP API；如需外部服务，应走平台侧能力或由官方接口承担 |

---

## 六、参考文档索引

**创作文档（`虚拟世界创作文档`）：**
- 《合养精灵动作》—— 动作播放/停止/重载/状态机全部用法与示例
- 《支持动态加载资源吗？》—— Resources.Load 不可用
- 《抖音虚拟世界开发模式简介》—— Shared Mod / DS 两种模式、网络对象、主权
- 《Dedicated Server 开发模式详解》—— DS 开启、RemoteEvent/RemoteFunction 全教程、FAQ
- 《消息互通》—— SendMessageToAll/Target/Owner、OwnerCall/TargetCall
- 《同步变量》—— varSync、主权方修改、OnValueChange
- 《数据存储详解》—— DATASTORE 块、dkjson/Json 编解码、DS 数据存储限制
- 《自定义 Module Script》—— 用 Lua 组织配置数据
- 《世界流式能力》—— 流式加载，构建期固化、运行时只读
- 《世界WebGL模式介绍》、《调用Unity API》—— 沙箱与白名单调用方式

**API 参考（`虚拟世界API参考`）：**
- `DouyinActor.PlayAnimation / StopAnimation / SetOverrideAnimation / SetOverrideAnimationController / PlayEmoji`
- `DouyinActor.onActionPlay / onEmotionPlay / onActorLoaded`
- `DouyinScript.SetAnimationEvent`
- `DouyinPlayerSettings.allowAction / allowEmotion`
- `DouyinRemoteEvent.*` / `DouyinRemoteFunction.*`
- `DouyinObjectService.NetSpawn / ServerSpawn`
- `DouyinSceneEnvironment.JsonAsset / LoadJson`
- `SDK API白名单` / `SDK API黑名单`
