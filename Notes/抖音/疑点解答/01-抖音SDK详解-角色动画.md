# 抖音虚拟世界 SDK 详解（一）：角色动画

> 面向对象：抖音虚拟世界创作者、服务端/客户端程序员
> 定位：以专家视角讲透"抖音 SDK 下角色动画"的全貌，并明确**哪些 Unity 能力被支持、哪些被禁止**。
> 关联资料：《虚拟世界API参考》之 `DouyinActor` 系列、《虚拟世界创作文档》之《合养精灵动作》、《SDK API白名单/黑名单》。

---

## 目录

1. [概念模型：动画在抖音虚拟世界里是怎么运作的](#1-概念模型)
2. [核心 API 逐项拆解](#2-核心-api-逐项拆解)
3. [三种动作控制手段对比](#3-三种动作控制手段对比)
4. [动画事件（Animation Event）](#4-动画事件animation-event)
5. [多人同步播放的正确姿势](#5-多人同步播放的正确姿势)
6. [Unity 支持 / 禁止清单（动画相关）](#6-unity-支持--禁止清单动画相关)
7. [常见误区与避坑](#7-常见误区与避坑)
8. [官方参考文档索引](#8-官方参考文档索引)

---

## 1. 概念模型

### 1.1 一句话总览

在抖音虚拟世界里，**动画资源（AnimationClip）不是字符串、不是网络数据，而是"编辑器里配置好、随世界包（AssetBundle）分发到每个客户端"的 Unity 资源引用**。运行时，你通过 `DouyinActor` 上的 API，把"本地已有的动画剪辑"播放到某个角色（Actor）身上。

```
[编辑器]
  制作 AnimationClip / AnimatorController / AnimatorOverrideController
        │  拖拽引用到脚本字段 / 场景
        ▼
[云构建] 打成 AssetBundle 随世界包下发
        │
        ▼
[每个客户端运行时]
  DouyinActor.PlayAnimation(本地动画引用)  ← 传的是资源引用，不是下载
```

### 1.2 两个关键对象

| 对象 | 含义 |
| --- | --- |
| **Actor（精灵/角色）** | 世界里的每个角色（玩家小火人、合养精灵 Pet）。通过 `DouyinActorService.GetLocalActor()`（本地）或 `GetActorById(actorID)`（任意）获取。 |
| **AnimationClip / RuntimeAnimatorController** | Unity 动画资源。**必须在项目中配置好并随包发布**，运行时只能引用、不能加载/下载。 |

> ⚠️ 平台没有"运行时从服务端拉动画资源"的能力（详见第 5、6 节）。这是理解本主题最重要的一点。

---

## 2. 核心 API 逐项拆解

### 2.1 `DouyinActor.PlayAnimation` —— 播放动作

```csharp
public void PlayAnimation(Animation clip, Action<AnimationEvent> cb = null, DouyinAnimatorMask mask = DouyinAnimatorMask.WholeBody)
```

| 参数 | 说明 |
| --- | --- |
| `clip` | 要播放的动画剪辑（**编辑器配置好的资源引用**） |
| `cb` | 可选回调；动画事件触发时回调，传 `AnimationEvent` 对象 |
| `mask` | 可选，默认 `WholeBody`；指定动画作用的身体部位遮罩 |

`DouyinAnimatorMask` 可选值：

| 值 | 影响范围 |
| --- | --- |
| `WholeBody` | 全身动画 |
| `Head` | 头部 |
| `UpperBody` | 上半身 |
| `LowerBody` | 下半身 |
| `Arms` | 双臂 |
| `LeftArm` / `RightArm` | 左臂 / 右臂 |
| `LeftHand` / `RightHand` | 左手 / 右手 |

> 💡 典型用法：`actor:PlayAnimation(clip, nil, DouyinAnimatorMask.UpperBody)` —— 只播上半身动作，下半身保留行走。

### 2.2 `DouyinActor.StopAnimation` —— 停止动作

```csharp
public void StopAnimation(DouyinAnimatorMask mask = DouyinAnimatorMask.WholeBody)
```

停止由 `PlayAnimation` 触发的动作，同样支持 `mask` 精确到身体部位。与 `PlayAnimation` 成对使用。

### 2.3 `DouyinActor.SetOverrideAnimation` —— 重载单个动作

```csharp
public void SetOverrideAnimation(string key, AnimationClip clip, Action<AnimationEvent> callback = null)
```

| 参数 | 说明 |
| --- | --- |
| `key` | 要重载的动画槽位唯一键名（如官方示例中的 `"proxy_Idle"`） |
| `clip` | 新的动画剪辑；**传 `nil` 表示还原**为原始动作 |
| `callback` | 可选，Animation Event 回调 |

> 💡 官方舞池示例：进入舞池把"待机"替换成"跳舞"，离开时传 `nil` 还原。

### 2.4 `DouyinActor.SetOverrideAnimationController` —— 重载整个动画状态机

```csharp
public void SetOverrideAnimationController(RuntimeAnimatorController animatorController)
```

这是**自由度最高**、也**最复杂**的方式：整体替换角色的 AnimatorController，实现"完全不同的动作逻辑"（如全新的动作游戏）。传 `nil` 还原。

> 官方建议结合 Unity 的 `AnimatorOverrideController` 使用，以在运行时对 AnimatorController 里的具体动作做动态替换/混合。

### 2.5 `DouyinActor.PlayEmoji` —— 播放表情

```csharp
public void PlayEmoji(int emojiIndex)
```

按索引播放表情。表情与动作是两条独立通道（`onEmotionPlay` / `onActionPlay` 分别监听）。

### 2.6 `DouyinScript.SetAnimationEvent` —— 给动画剪辑绑定事件回调

```csharp
public void SetAnimationEvent(AnimationClip clip, Action<AnimationEvent> callback)
```

不播放、只给某个动画剪辑注册 Animation Event 回调；当播放该剪辑时会触发回调。

### 2.7 相关事件与开关

| 事件 / 属性 | 类型 | 说明 |
| --- | --- | --- |
| `DouyinActor.onActionPlay` | `UnityEvent<string>` | 角色使用动作事件，参数为动作名 |
| `DouyinActor.onEmotionPlay` | `UnityEvent<string>` | 角色使用表情事件，参数为表情名 |
| `DouyinActor.onActorLoaded` | 事件 | 切换 Actor 形象时回调 |
| `DouyinPlayerSettings.allowAction` | `bool` | 是否允许动作功能（默认 true） |
| `DouyinPlayerSettings.allowEmotion` | `bool` | 是否允许表情功能 |

---

## 3. 三种动作控制手段对比

| 手段 | API | 适合场景 | 复杂度 |
| --- | --- | --- | --- |
| **播放/停止** | `PlayAnimation` / `StopAnimation` | 立刻播放一个动作、播完即止 | ★☆☆ |
| **重载动作** | `SetOverrideAnimation` | 动态替换某个动作槽（舞池、换武器动作） | ★★☆ |
| **重载状态机** | `SetOverrideAnimationController` | 完全改变动作逻辑（新动作游戏） | ★★★ |

官方文档《合养精灵动作》原话归纳：

- 播放某个动作：`PlayAnimation` 让显示对象立刻播放新动作，`StopAnimation` 停止。
- 重载某个动作：`SetOverrideAnimation` 指定"被重载的动作名称"，传 nil 还原。
- 重载动作控制器：`SetOverrideAnimationController` 需要先配置好包含正确状态切换逻辑的新控制器，再用 Unity 相关 API 控制。

---

## 4. 动画事件（Animation Event）

`PlayAnimation` / `SetOverrideAnimation` 支持动画事件，实现"动画播到某个时间点触发逻辑"（如出拳瞬间触发伤害判定）。

**使用要点（官方明确）：**

1. 事件在 Unity 动画窗口配置（参考 Unity Animation Event）。
2. **Event 中填写的 Function 名称不会起作用** —— 所有 Event 都会触发你传入的**那一个回调函数**。
3. 回调函数中可读取 `AnimationEvent` 的**其他参数**（时间、int/float/string 参数等）。

```lua
function PlayAnimWithEvent()
    local me = DouyinActorService.GetLocalActor()
    me:PlayAnimation(AttackClip, function(animEvent)
        print("动画事件触发，时间：", animEvent.time, "字符串参数：", animEvent.stringParameter)
    end)
end
```

---

## 5. 多人同步播放的正确姿势

**核心原则：动画资源不通过网络传输，同步的是"指令"。**

官方示例流程（点击 → 全房间看到该玩家播放动作）：

```lua
-- 触发方：广播动作指令
function PlayAnimation()
    local me = DouyinActorService.GetLocalActor()
    self:SendMessageToAll("SyncAnimation", me.actorID)   -- 广播 actorID
end

-- 每个客户端：收到指令后，对目标 Actor 本地播放动画
function SyncAnimation(actorID)
    local actor = DouyinActorService.GetActorById(actorID)
    actor:PlayAnimation(Animation)   -- Animation 是本地已打包的动画资源
end
```

要点：

- 同步载体是 `actorID`（或动作 ID/枚举），**不是动画本体**。
- 所有客户端必须有这份动画资源（随世界包分发），才能保证播放一致。
- 更进阶的架构：服务端（DS）统一下发"动作 ID"，客户端查本地动作表播放 —— 详见《服务端调用》文档。

---

## 6. Unity 支持 / 禁止清单（动画相关）

> 依据：《SDK API白名单》《SDK API黑名单》。白名单是**严格生效**的沙箱清单，不在清单内的引擎命名空间/组件，Lua 侧不允许调用或反射获取。

### 6.1 与动画相关的 Unity 命名空间（✅ 白名单内）

| 命名空间 | 说明 |
| --- | --- |
| `UnityEngine` | 基础（含 `AnimationClip`、`Animator`、`RuntimeAnimatorController` 等核心类型所在） |
| `UnityEngine.Animations` | 动画相关 |
| `UnityEngine.Playables` | 可播放对象（PlayableGraph） |
| `UnityEngine.Events` | `UnityEvent`、`Action` 等 |

> 也就是说：**`AnimationClip`、`RuntimeAnimatorController`、`AnimatorOverrideController` 这些类型本身在沙箱内是可引用、可传给 SDK API 的**。前提是资源来自工程内配置、随包发布。

### 6.2 动画相关组件（✅ 白名单内 Douyin 组件）

- `DouyinSceneEnvironment`（含角色光照等，与动画联动）
- 官方"通用功能业务组件"里没有专门动画组件，动画能力由 `DouyinActor` 提供

### 6.3 被禁止 / 不可用的能力（❌）

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| `Resources.Load` 动态加载动画 | ❌ | 官方明确回复不可用，资源随包分发 |
| `UnityEngine.Networking`（`UnityWebRequest` 等） | ❌ | 黑名单禁用，无法运行时下载动画 |
| `System.IO`（读取本地文件） | ❌ | 黑名单禁用，无法读本地动画文件 |
| 反射调用（`GetMethod`/`Invoke` 等） | ❌ | 禁止绕过白名单 |
| `AnimationClip` 运行时创建/编码 | ⚠️ 受限 | 沙箱内没有公开的运行时构建/下载动画资源通道；只能引用工程内资源 |
| `Animator` 直接操控 | ⚠️ 谨慎 | 需要走 `DouyinActor` 的封装 API；直接 `GetComponent(typeof(UnityEngine.Animator))` 在白名单内可尝试，但官方推荐用 `SetOverrideAnimationController` 等受控接口 |

> 🔧 白名单规则补充：Lua 里用 `GetComponent / AddComponent` 需要带 `typeof` 参数（见《调用Unity API》）。

---

## 7. 常见误区与避坑

1. **误区：动画是"字符串/名称"** —— 不是。`PlayAnimation` 第一参是动画剪辑资源引用。若要"按名字播"，需自己维护 `name → AnimationClip` 映射表。
2. **误区：可以运行时从服务端拉新动画** —— 不可以。新动画资源只能走重新发布世界版本。
3. **误区：Animation Event 里的函数名会生效** —— 不会。所有 Event 都触发你传的回调。
4. **避坑：同步变量只适合状态值** —— 播放动作是"一次性事件"，用 `SendMessageToAll` / RemoteEvent 广播指令更合适。
5. **避坑：动作开关** —— 记得检查 `DouyinPlayerSettings.allowAction`，若为 false 动作会被拦截。

---

## 8. 官方参考文档索引

- API：`DouyinActor.PlayAnimation` / `StopAnimation` / `SetOverrideAnimation` / `SetOverrideAnimationController` / `PlayEmoji`
- API：`DouyinActor.onActionPlay` / `onEmotionPlay` / `onActorLoaded`
- API：`DouyinScript.SetAnimationEvent`
- API：`DouyinPlayerSettings.allowAction` / `allowEmotion`
- 创作文档：《合养精灵动作》《调用Unity API》《SDK API白名单》《SDK API黑名单》
