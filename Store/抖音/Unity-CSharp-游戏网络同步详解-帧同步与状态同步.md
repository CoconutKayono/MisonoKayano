# Unity + C# 游戏网络同步详解：帧同步与状态同步

> 本文面向使用 Unity 与 C# 开发联网游戏的工程师，重点深入讲解两种主流同步架构——**状态同步（State Synchronization）** 与 **帧同步（Frame Synchronization / Lockstep）**，以及它们各自的数据组织与同步方式。

## 目录

1. [游戏网络同步基础](#一游戏网络同步基础)
2. [Unity 常用网络方案概览](#二unity-常用网络方案概览)
3. [状态同步详解](#三状态同步state-synchronization)
4. [帧同步详解](#四帧同步frame-synchronization--lockstep)
5. [两种方案对比](#五帧同步-vs-状态同步-对比)
6. [数据同步通用设计要点](#六数据同步的通用设计要点)
7. [实践建议与常见坑](#七实践建议与常见坑)
8. [总结](#八总结)

---

## 一、游戏网络同步基础

### 1.1 为什么要做网络同步

单机游戏中，所有逻辑都在同一台机器上运行，数据天然一致。联网游戏则有多台设备（客户端与服务器）同时运行各自的一份游戏逻辑，每一台设备对“游戏世界当前状态”的认知都可能不同。网络同步的目标，就是让这些分散的状态在可接受的延迟与带宽下，最终保持一致，从而让所有玩家看到同一个“合理的游戏世界”。

### 1.2 核心问题：状态一致性

网络同步本质上要解决三个问题：

- **一致性（Consistency）**：不同玩家看到的游戏状态是否一致。
- **实时性（Latency）**：状态从发生到被其他玩家感知的时间差。
- **带宽（Bandwidth）**：同步数据占用多少网络流量。

这三者互相制约：想要更强一致性和更低延迟，通常需要更高的同步频率或更复杂的预测算法，消耗更多带宽与 CPU。

### 1.3 网络模型

- **权威服务器（Authoritative Server / Dedicated Server）**
  服务器拥有最终权威，客户端只发送输入或请求，服务器计算结果并广播。安全性最好，状态同步通常采用此模型。

- **主机托管（Host / Listen Server）**
  某个玩家既当客户端又当服务器（P2P 中的主机角色），成本和延迟低，但存在主机玩家作弊风险与主机掉线问题。帧同步在局域网或小规模对战常用。

- **纯 P2P（Peer-to-Peer）**
  每个客户端互相同步，没有中心权威。实现复杂、易作弊，实际游戏较少采用，常见于早期局域网游戏。

### 1.4 传输层：TCP vs UDP

| 特性 | TCP | UDP |
|------|-----|-----|
| 可靠性 | 可靠、有序、有确认重传 | 不可靠、无序、可能丢包 |
| 延迟 | 重传与拥塞控制可能导致延迟抖动 | 低延迟、无阻塞 |
| 适用 | 大厅、登录、聊天、回合制、关键一次性数据 | 实时移动、射击、高频状态/指令同步 |
| 在游戏中的定位 | 控制面 / 关键数据 | 数据面 / 高频数据 |

**实践结论**：实时对战类游戏通常采用 **UDP + 可靠性应用层协议**（如 KCP、Enet、WebRTC 数据通道），或使用 TCP 但接受其延迟特性。Unity 的 NGO / Mirror 底层默认可用 UDP 传输，也支持 WebSocket 等。

### 1.5 关键指标

- **RTT（往返延迟）**：数据包一去一回的时间，直接影响“操作到反馈”的手感。
- **丢包率（Packet Loss）**：决定是否需要重传、前向纠错（FEC）或冗余发送。
- **抖动（Jitter）**：延迟的波动，帧同步中通过缓冲帧来吸收。
- **同步频率（Tick Rate）**：服务器每秒钟更新/广播状态的次数，如 20Hz、30Hz、60Hz。

---

## 二、Unity 常用网络方案概览

| 方案 | 类型 | 说明 |
|------|------|------|
| **UNet / HLAPI** | 官方旧方案 | 已被 Unity 移除（2022+），不推荐新项目使用 |
| **Mirror** | 社区方案 | UNet 的精神续作，API 与 UNet 相似，生态成熟 |
| **Netcode for GameObjects (NGO)** | 官方现役方案 | Unity 官方推荐，支持权威服务器、RPC、网络变量、插值 |
| **Photon PUN / Fusion** | 商业云方案 | 免服务器运维，Fusion 支持状态同步 + 预测 + 快照 |
| **FishNet** | 社区方案 | 高性能、功能丰富，预测与回滚支持较好 |
| **自研 Socket** | 自定义 | 用 C# Socket + 序列化自行实现，灵活但工作量大 |

无论用哪套方案，底层的同步架构都离不开状态同步或帧同步这两种范式。下面分别详解。
---

## 三、状态同步（State Synchronization）

### 3.1 概念与原理

**状态同步**：以“游戏世界的状态”作为同步单位。服务器（权威端）运行核心逻辑，维护世界的真实状态；客户端把玩家操作（输入）上传给服务器，服务器计算后把更新后的状态广播给相关客户端；客户端收到后渲染这个状态。

一句话：**客户端上传“我想做什么”（输入），服务器下发“世界变成了什么样”（状态）。**

流程示意：

```
客户端A               服务器                客户端B
  |--- 输入(移动/开火) -->|                      |
  |                      |-- 计算世界状态 ------->|
  |<--- 状态快照 ---------|                      |
  |<--- 状态快照 --------------------------------|
  |     （渲染）          |                      |
```

### 3.2 状态同步需要同步什么数据

按“谁需要知道”和“变化频率”来分类：

- **高频、连续变化**：位置（Position）、朝向（Rotation）、速度（Velocity）、动画状态。
- **低频、事件性**：开火、受伤、拾取、技能释放（用 RPC / 事件消息）。
- **持久状态**：血量、等级、装备、Buff、阵营、队伍。
- **全局状态**：对局阶段、倒计时、比分、刷怪信息。

### 3.3 同步策略

1. **全量快照（Full Snapshot）**
   每个 tick 发送完整状态。实现简单，但带宽浪费大，只适合小状态量。

2. **增量同步（Delta）**
   只发送“变化了”的字段。通过脏标记（Dirty Flag）或字段对比实现，是主流做法。例如 Mirror/NGO 的 SyncVar 只在值变化时同步。

3. **基于重要性的差异化同步（Interest Management）**
   只把状态同步给“关心”它的客户端（如距离较近、同一区域）。降低带宽与 CPU。

4. **同步频率差异化**
   位置每 0.05s 同步一次，血量只在变化时同步，聊天即时同步。

### 3.4 客户端预测与服务器和解（Client Prediction & Server Reconciliation）

状态同步的最大痛点是：玩家输入后要等一个 RTT 才能看到反馈，手感会“飘”。解决方式是客户端预测。

- **预测（Prediction）**：客户端在发出输入的同时，立即本地执行移动，先渲染结果。
- **和解（Reconciliation）**：服务器收到输入后计算权威状态并下发；客户端收到服务器快照时，对比自己预测的位置，若偏差超过阈值，则回滚到服务器状态并重放（Replay）尚未确认的输入。

简化代码示例（NGO 风格的权威移动）：

```csharp
using Unity.Netcode;
using UnityEngine;
using System.Collections.Generic;

public class PlayerMotor : NetworkBehaviour
{
    [SerializeField] float moveSpeed = 5f;

    // 客户端提交的输入（通过 RPC 发送给服务器）
    Vector3 pendingInput;

    public override void OnNetworkSpawn()
    {
        // 本机玩家：由预测逻辑驱动，保证即时手感
    }

    void Update()
    {
        if (!IsOwner) return;

        Vector3 raw = new Vector3(Input.GetAxisRaw("Horizontal"), 0, Input.GetAxisRaw("Vertical"));
        pendingInput = raw.normalized;

        // 客户端本地预测：立即移动
        if (IsClient && !IsServer)
        {
            transform.position += pendingInput * moveSpeed * Time.deltaTime;
        }

        // 周期性把输入发给服务器
        SubmitInputServerRpc(pendingInput);
    }

    [ServerRpc]
    void SubmitInputServerRpc(Vector3 input)
    {
        if (!IsServer) return;
        // 服务器权威移动
        transform.position += input * moveSpeed * Time.deltaTime;
    }
}
```

> 说明：上面是简化示意。工程实践中，客户端预测需要维护输入队列、保存预测前状态，并在收到服务器权威快照时做**回滚 + 重放**。NGO 的 `NetworkTransform`、FishNet 的预测模块都内置了这套机制。

### 3.5 插值（Interpolation）

服务器 tick 频率通常低于渲染帧率（例如服务器 20Hz，渲染 60Hz）。如果客户端直接按收到的位置渲染，会出现抖动。插值在“过去”的两个快照之间做平滑过渡：

- **实体插值**：对非本机玩家的实体，渲染位置滞后于服务器最新状态约 100ms，用两个历史快照线性插值。
- **本机玩家不插值**：本机玩家用预测，保证即时反馈。

```csharp
// 简化：在历史快照 buffer 中取包围当前渲染时间的两个状态做 Lerp
void ApplyInterpolation(float renderTime)
{
    while (buffer.Count >= 2 && buffer[1].timestamp <= renderTime)
        buffer.RemoveAt(0);

    if (buffer.Count < 2) return;

    var a = buffer[0];
    var b = buffer[1];
    float t = (renderTime - a.timestamp) / (b.timestamp - a.timestamp);
    transform.position = Vector3.Lerp(a.position, b.position, t);
}
```

### 3.6 状态同步的数据组织与代码示例

一个典型的状态同步网络对象包含：

- **网络身份（NetworkId / Spawn）**：服务器生成对象后分配 ID，通知客户端 Spawn。
- **同步变量（SyncVar / NetworkVariable）**：自动在变化时同步。
- **RPC（远程调用）**：用于一次性事件与操作。

以 Mirror 风格为例：

```csharp
using Mirror;
using UnityEngine;

public class Player : NetworkBehaviour
{
    // 变化时自动同步到所有客户端
    [SyncVar(hook = nameof(OnHealthChanged))]
    public int health = 100;

    [SyncVar]
    public int score;

    void OnHealthChanged(int oldValue, int newValue)
    {
        // 客户端收到变化后刷新 UI
        Debug.Log($"HP {oldValue} -> {newValue}");
    }

    [Command] // 客户端 -> 服务器
    void CmdShoot()
    {
        if (!isServer) return;
        // 服务器执行开火逻辑
        RpcShootEffect();
    }

    [ClientRpc] // 服务器 -> 所有客户端
    void RpcShootEffect()
    {
        // 播放枪口特效
    }
}
```

**数据流总结（状态同步）**：

| 方向 | 内容 | 频率 | 例子 |
|------|------|------|------|
| 客户端 → 服务器 | 输入指令 / 操作请求 | 每帧或固定频率 | 移动输入、开火命令 |
| 服务器 → 客户端 | 权威状态 / 事件 | 固定 tick | 位置、血量、比分、RPC 事件 |

### 3.7 状态同步的优缺点与适用场景

**优点**

- 逻辑集中在服务器，安全性高，易做反作弊。
- 对客户端设备性能要求低，客户端可“弱逻辑”。
- 容易处理动态加入、断线重连、观战。
- 数据量可控，可通过兴趣管理、增量同步优化。

**缺点**

- 延迟反馈依赖预测/插值，实现复杂。
- 高频、大量单位的同步带宽压力大（如 RTS 的成百上千单位）。
- 需要服务器承载所有逻辑，服务器成本高。

**适用场景**：MMORPG、FPS/TPS、MOBA 的服务器权威部分、需要强反作弊的竞技游戏、开放世界多人游戏。
---

## 四、帧同步（Frame Synchronization / Lockstep）

### 4.1 概念与原理

**帧同步（锁步同步）**：以“玩家输入指令”作为同步单位。每个客户端都运行**完全相同**的游戏逻辑；只需保证在每一逻辑帧，所有客户端拿到**相同的输入**，它们就会算出**相同的世界状态**。由于逻辑是确定性的，不需要同步状态本身。

一句话：**同步的是“玩家在这一帧做了什么”（指令），而不是“世界长什么样”（状态）。**

流程示意：

```
       玩家A 输入                玩家B 输入
           |                       |
           v                       v
     帧 N 指令集合  <--- 汇集/广播 --->  帧 N 指令集合
           |                       |
           v                       v
     推进逻辑帧 N                  推进逻辑帧 N
      (确定性计算)                 (确定性计算)
           |                       |
           v                       v
     A 的本地世界状态  ==(一致)==   B 的本地世界状态
```

### 4.2 确定性（Determinism）是核心

帧同步要求“同样的输入 + 同样的初始状态 = 同样的结果”。一旦某台机器计算结果不同，就会“漂移”，最终彻底不同步。保证确定性的关键：

- **使用定点数代替浮点数**：不同 CPU/编译器对浮点运算的舍入可能不同。定点数（如 1/1000 精度的整数）可保证跨平台一致。
- **固定逻辑帧率**：逻辑帧与渲染帧解耦，固定步长（如 15/30 逻辑帧每秒），不受渲染帧率波动影响。
- **避免依赖不确定的数据结构**：不遍历 `Dictionary` / `HashSet` 的未定义顺序，改用数组/有序列表。
- **避免依赖不确定的系统 API**：如 `Time.time`（基于真实时间）、随机数需用**共享种子 + 确定性随机**。
- **物理引擎确定性**：Unity 自带 PhysX 不保证跨平台确定，帧同步通常用**自研确定性物理/碰撞**（如定点物理引擎），或只做简单的 AABB/格点碰撞。
- **统一浮点模式与编译平台**：避免 32/64 位差异，避免依赖 NaN/Infinity 等未定义行为差异。

### 4.3 帧同步同步什么数据

**核心同步数据 = 玩家指令 + 帧号。**

- **玩家指令（Player Input / Command）**：移动方向、技能按键、目标、视角等，打包成定长字节。
- **帧号（Frame / Turn）**：标识该指令属于第几逻辑帧。
- **随机种子（Random Seed）**：保证所有客户端随机结果一致。
- **校验和（Checksum）**：周期性对状态做校验，检测是否漂移。
- **重连所需快照（可选）**：断线重连时，需补发缺失的指令，或直接发送某个历史帧的完整状态（快照）加速追帧。

### 4.4 锁步流程

1. 所有玩家上报本帧指令。
2. 服务器（或主机）汇集所有指令，加上帧号打包。
3. 广播该帧的完整指令集合。
4. 每个客户端收到后，把指令喂给本地确定性逻辑，推进到该帧。
5. 重复上述过程。

帧同步的“帧”通常不是渲染帧，而是**逻辑帧（Simulation Tick）**。常见做法是让逻辑帧率固定，渲染帧用插值补齐。

### 4.5 帧数据组织与代码示例

```csharp
using System.Collections.Generic;

// 单个玩家的一帧指令（定长、可序列化）
[System.Serializable]
public struct PlayerCommand
{
    public uint frame;        // 逻辑帧号
    public byte playerId;     // 玩家编号
    public byte moveDir;      // 移动方向编码 0-7（八方向）
    public byte skillId;      // 释放的技能
    public bool jump;
}

// 一帧内所有玩家的指令集合
public class FrameInput
{
    public uint frame;
    public List<PlayerCommand> commands = new List<PlayerCommand>();
}

// 锁步管理器（简化示意）
public class LockstepManager
{
    const int LogicFramePerSecond = 15;   // 15 逻辑帧/秒
    const int BufferFrames = 5;           // 缓冲帧，吸收网络抖动
    const float LogicDelta = 1f / LogicFramePerSecond;

    // 待推进的帧指令队列
    Queue<FrameInput> frameQueue = new Queue<FrameInput>();
    // 本机已上报但还没收到完整帧的指令（等待回填）
    Dictionary<uint, PlayerCommand> localPending = new Dictionary<uint, PlayerCommand>();

    uint currentFrame = 0;
    float accumulator = 0f;

    public void LocalPlayerInput(PlayerCommand cmd)
    {
        // 本机输入先入本地缓存，并上报给服务器/主机
        localPending[cmd.frame] = cmd;
        SendCommandToServer(cmd);
    }

    public void OnFrameInputReceived(FrameInput frameInput)
    {
        // 收到一帧完整指令，加入队列等待推进
        frameQueue.Enqueue(frameInput);
    }

    public void Update(float deltaTime)
    {
        // 固定步长推进逻辑帧
        accumulator += deltaTime;
        while (accumulator >= LogicDelta)
        {
            accumulator -= LogicDelta;
            TickLogic();
        }
    }

    void TickLogic()
    {
        // 缓冲未满则等待，以吸收网络抖动
        if (frameQueue.Count <= BufferFrames)
            return;

        FrameInput frame = frameQueue.Dequeue();
        currentFrame = frame.frame;

        // 把本帧所有玩家指令喂给确定性逻辑
        foreach (var cmd in frame.commands)
        {
            GameLogic.StepPlayer(currentFrame, cmd);
        }

        // 推进世界逻辑（移动、碰撞、技能结算），全部基于确定性实现
        GameLogic.AdvanceWorld(LogicDelta);
    }
}
```

### 4.6 处理网络抖动：缓冲帧 / 追帧

网络延迟是波动的。如果一帧指令没到就推进，会卡住；如果一帧迟到，就会错过。做法：

- **输入缓冲（Jitter Buffer）**：客户端维护一个小缓冲（如上例的 `BufferFrames`），当队列里积累足够帧后才开始推进。缓冲越大越抗抖动，但引入的“操作到响应”延迟也越大。
- **追帧 / 快进（Fast Forward）**：落后太多的客户端加快逻辑帧推进，追上最新帧。
- **补帧**：缺失帧时请求重发或直接快进跳过。

### 4.7 回滚与追帧（Rollback）

用于格斗、RTS 等对延迟极敏感的游戏：

- **Rollback（回滚网络代码）**：客户端不等待远端输入，先用**预测输入**（如对手上一帧输入）立即推进；当真实输入到达时，回滚到该帧、替换输入、重新推进到当前帧。需要逻辑支持**快照与回滚（保存状态 / 恢复状态）**。

```csharp
// 确定性逻辑需要支持快照回滚
public class GameState
{
    public int[] playerX;   // 用定点数更稳妥，这里以 int 示意
    public int[] playerY;
    public int[] hp;

    public GameState Clone() => (GameState)MemberwiseClone();
}

public class RollbackManager
{
    // 保存每一逻辑帧的完整状态快照
    Dictionary<uint, GameState> history = new Dictionary<uint, GameState>();

    public void SaveFrame(uint frame, GameState state)
    {
        history[frame] = state.Clone();
    }

    public GameState RollbackTo(uint frame)
    {
        return history[frame].Clone();
    }
}
```

### 4.8 一致性校验（Checksum）

即使做了确定性保证，仍可能因 bug 漂移。可在每帧或每隔若干帧计算一次状态校验和，发给服务器比对；不一致时告警或触发重连/重同步。

```csharp
public static uint CalcChecksum(GameState state)
{
    uint hash = 2166136261u; // FNV-1a
    foreach (var x in state.playerX) { hash ^= (uint)x; hash *= 16777619u; }
    foreach (var y in state.playerY) { hash ^= (uint)y; hash *= 16777619u; }
    foreach (var h in state.hp)    { hash ^= (uint)h; hash *= 16777619u; }
    return hash;
}
```

### 4.9 帧同步的优缺点与适用场景

**优点**

- **带宽极低**：只传指令，不传状态，成千上万单位也只传操作。
- **观战/回放简单**：保存所有帧的指令即可完整回放。
- **对服务器逻辑压力小**：服务器只转发指令，不做世界计算（或只做轻量校验）。
- **一致性天然有保证**（在确定性成立的前提下）。

**缺点**

- **实现难度高**：对确定性要求苛刻，浮点、物理、随机、容器顺序都要控制。
- **对客户端性能要求高**：每个客户端都要跑完整逻辑。
- **网络等待**：锁步模式下，任意玩家网络差会拖慢所有人（卡帧）。
- **作弊风险**：客户端有完整状态，易被透视/修改，需要额外反作弊。
- **断线重连复杂**：需要补帧或快照机制。

**适用场景**：RTS（星际争霸、魔兽争霸）、MOBA（如王者荣耀）、格斗游戏（Rollback）、棋牌/回合制、局域网联机、强调大量单位同步的游戏。
---

## 五、帧同步 vs 状态同步 对比

| 维度    | 状态同步                | 帧同步                    |
| ----- | ------------------- | ---------------------- |
| 同步对象  | 世界状态（位置、血量、事件）      | 玩家指令（输入 + 帧号）          |
| 权威方   | 服务器计算，客户端渲染         | 各客户端各自计算，服务器/主机转发指令    |
| 带宽占用  | 高（随单位数量线性增长）        | 低（与单位数量基本无关）           |
| 延迟敏感度 | 依赖预测 + 插值改善         | 锁步受最慢玩家影响；Rollback 可改善 |
| 确定性要求 | 低，逻辑可集中在服务器         | 极高，所有客户端逻辑必须一致         |
| 服务器压力 | 高（承载世界逻辑）           | 低（转发 + 校验）             |
| 客户端压力 | 低                   | 高（跑完整逻辑）               |
| 断线重连  | 简单（快照 + 增量）         | 复杂（补帧/快照/追帧）           |
| 反作弊   | 容易（状态不透明）           | 困难（客户端拥有全量状态）          |
| 观战/回放 | 需额外录制               | 天然支持（指令回放）             |
| 典型场景  | FPS/TPS、MMORPG、开放世界 | RTS、MOBA、格斗、回合制、棋牌     |

## 六、数据同步的通用设计要点

### 6.1 序列化与压缩

- 用**二进制序列化**（如 MessagePack、Protobuf、自定义字节流）代替 JSON/XML，减小体积。
- **定点数/量化压缩**：位置用短整型 + 缩放因子代替 float，朝向用 byte 量化到 256 份。
- 指令用**位域（Bitfield）压缩**：方向 3 bit、技能 5 bit、按键 1 bit，一个 byte 装多个字段。

### 6.2 同步频率与优先级

- 区分高频/低频数据，高频走数据面（UDP），低频/关键走控制面（TCP/可靠）。
- 用脏标记只同步变化字段，降低带宽。
- 用兴趣管理（AOI）只同步相关对象。

### 6.3 权威与权限校验

- 服务器必须校验客户端上报的数值合法性（速度上限、冷却、位置合理性），防止加速/瞬移。
- 状态同步中服务器是唯一权威；帧同步中可加服务器校验（校验和比对、行为规则检查）。

### 6.4 断线重连

- 状态同步：服务器给重连客户端发当前全量快照，再继续增量。
- 帧同步：补发缺失帧指令，或发送历史快照 + 让客户端追帧到最新。

### 6.5 作弊防护

- 状态同步：关键逻辑上服务器，客户端只做表现。
- 帧同步：客户端拥有全量状态，难防透视；需加密协议、内存模糊化、服务器行为校验、异常检测。

## 七、实践建议与常见坑

1. **帧同步务必用定点数**：浮点跨平台不一致是最常见翻车点，从一开始就上定点数库。
2. **逻辑帧与渲染帧分离**：逻辑固定步长，渲染插值，避免“高帧率下逻辑加速”。
3. **避免在逻辑里用真实时间/随机/容器遍历顺序**：统一注入确定性随机种子，容器用有序结构。
4. **状态同步优先使用现成网络组件**：NGO/Mirror 的 NetworkTransform、NetworkAnimator、SyncVar 能省大量时间，先搞懂其插值与预测开关。
5. **关注带宽预算**：单条消息、每秒消息量、房间人数都要提前估算，避免大厅阶段就带宽爆表。
6. **先定义协议再做功能**：消息 ID、字段顺序、字节序（大端/小端）要固定并版本化，方便热更与兼容。
7. **做好断线与重连**：不能只考虑正常对战，掉线、重连、观战、中途加入都要设计。
8. **压测与校验**：帧同步加 checksum 报警，状态同步做自动化对局回归，尽早发现漂移与不同步。

## 八、总结

- **状态同步**同步“世界状态”，适合服务器权威、需强反作弊、单位数量适中、客户端性能受限的场景。核心在于**权威服务器 + 客户端预测 + 插值 + 兴趣管理**。
- **帧同步**同步“玩家指令”，适合大量单位、低带宽、天然回放、局域网或信任度较高的竞技场景。核心在于**确定性逻辑 + 锁步推进 + 缓冲/追帧/回滚 + 校验和**。

实际项目中二者也常混合：用帧同步跑局内核心逻辑，用状态同步做大厅、匹配、结算与次要表现；或状态同步为底，局部战斗用帧同步。理解两种范式的数据流与取舍，是设计健壮联网游戏的前提。