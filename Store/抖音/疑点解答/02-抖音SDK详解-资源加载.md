# 抖音虚拟世界 SDK 详解（二）：资源加载

> 面向对象：抖音虚拟世界创作者、服务端/客户端程序员
> 定位：讲透抖音虚拟世界下"资源是如何产生、打包、分发、运行时使用"的完整链路，并明确**哪些 Unity 资源加载能力被支持、哪些被禁止**。
> 关联资料：《支持动态加载资源吗？》《抖音虚拟世界开发模式简介》《网络对象生成配置》《世界流式能力》《SDK API白名单/黑名单》。

---

## 目录

1. [核心结论：抖音不支持运行时动态加载资源](#1-核心结论)
2. [资源生命周期：编辑器 → 云构建 → 客户端](#2-资源生命周期)
3. [静态资源怎么用](#3-静态资源怎么用)
4. [动态生成对象：NetSpawn 与网络对象](#4-动态生成对象nettspawn-与网络对象)
5. [场景流式加载（Streaming）](#5-场景流式加载streaming)
6. [音视频等特殊资源](#6-音视频等特殊资源)
7. [Unity 支持 / 禁止清单（资源加载相关）](#7-unity-支持--禁止清单)
8. [常见误区与避坑](#8-常见误区与避坑)
9. [官方参考文档索引](#9-官方参考文档索引)

---

## 1. 核心结论

> **抖音虚拟世界不支持在运行时动态加载资源。**
>
> 官方《支持动态加载资源吗？》原文：
> > 问：是否可以使用 Unity 的 Resource.Load 来动态加载资源，进行版本更新。
> > 答：**不可以**。目前世界上传的时候，云构建会生成 AssetBundle 资源包。对于创作者来说，**无法通过访问 Resources 目录，也就意味着无法使用 Resources.Load 来加载资源**。如果要对世界进行版本更新，需要重新走一遍发布世界的路线（上传新版本）。

**推论：**

- 没有 `Resources.Load`。
- 没有 `UnityWebRequest` 下载资源（黑名单禁用）。
- 没有 `AssetBundle.LoadFromFile / LoadFromMemory`。
- 没有"运行时从服务端拉新资源"的能力。
- **资源更新 = 重新发布世界新版本**，由平台分发。

---

## 2. 资源生命周期

```
[Unity 编辑器]
  创建模型/动画/贴图/音效/Prefab/场景
        │  在场景摆放、或配置进 DouyinWorldRoot 的网络对象表
        ▼
[上传世界 → 云构建]
  平台把所有资源打成 AssetBundle 资源包
        │
        ▼
[客户端运行时]
  · 场景随包加载
  · 网络对象通过 NetSpawn(key) 实例化（key 预先在 DouyinWorldRoot 配置）
  · 不支持按需下载/加载
```

关键点：

- **打包方式**：云构建生成 AssetBundle，创作者**不可访问 Resources 目录**。
- **发布节奏**：资源有变化 → 走发布流程传**新版本**。
- **运行时能力**：只能"使用已随包到达的资源"，不能"加载尚未到达的资源"。

---

## 3. 静态资源怎么用

静态资源（场景里摆好的模型、环境、交互物体）直接放在 Unity 场景中，随场景打包。运行时通过 `GameObject.Find`、`GetComponent`（需 `typeof`）或场景引用使用。

要点：

- 场景里必须有一个 **`DouyinWorldRoot`** 组件（任何世界上传的前提），它承载出生点、玩家属性、相机、网络对象表等。
- 静态/动态物体的网络化要求（详见第 4 节）。

---

## 4. 动态生成对象：NetSpawn 与网络对象

### 4.1 为什么动态生成必须走网络对象

凡是**多个玩家需要看到一致状态**的物体，都必须是"网络对象"。平台规定（《抖音虚拟世界开发模式简介》）：

> 支持使用平台提供的 API 来动态创建（`NetSpawn`）与销毁（`NetDestroy`），**不可使用 Unity 原生 API（`Instantiate` / `Destroy`）**来动态创建与销毁网络对象。

### 4.2 网络对象的配置流程

1. 给 GameObject 挂 **`Douyin Object Sync`（网络同步组件）** 与 **`DouyinNetworkGuid`**（挂 DouyinScript 时默认自带）。
2. 在 `DouyinWorldRoot` 的网络对象生成配置中创建 **Douyin Net Spawn Object Asset**，将 GameObject 关联进去，并设置一个**全局唯一主键 key**。
3. 运行时用 key 实例化。

> ⚠️ 上限：**一个世界最多共存 10,000 个网络对象**（《Douyin World Root 组件》）。

### 4.3 `DouyinObjectService.NetSpawn` 的四个重载

```csharp
public static GameObject NetSpawn(string key, out int id)
public static GameObject NetSpawn(string key, Vector3 position, out int id)
public static GameObject NetSpawn(string key, Vector3 position, Vector3 rotation, out int id)
public static GameObject NetSpawn(string key, Vector3 position, Quaternion rotation, out int id)
```

```lua
-- Lua 示例：按 key 在指定位置生成网络对象
local netObj, netid = DouyinObjectService.NetSpawn("NetObject_1", Vector3(1,1,1), function(obj, id)
    print("生成成功", obj.name, id)
end)
```

`NetSpawn` 传的是 **key（字符串）**，不是 prefab 引用 —— 这也是"资源预配置"模式的体现：key 背后对应的 GameObject 在构建期已打进包内。

### 4.4 服务器端生成：`ServerSpawn` / `ServerDestroy`

DS 模式专属（仅在服务端执行）：

```lua
local netObj, netObjId = DouyinObjectService.ServerSpawn("NetObj_1", Vector3(1,0,0), function(netObj, netObjId)
    -- 仅存在于服务端，不同步到客户端
end)
```

> ⚠️ `ServerSpawn` 生成的对象仅存在于服务器、客户端无实例，**不要带 Rigidbody**，否则会导致客户端/服务端位置同步异常（官方明确警告）。

---

## 5. 场景流式加载（Streaming）

官方提供"流式能力"以优化加载：按区块、按玩家视点距离做 High / Medium / Low / Release 四档加卸载。

| 配置/能力 | 说明 |
| --- | --- |
| `DouyinWorldRoot` → 启用流式加载 | 设置加载距离、低模参数等，**构建期固化** |
| `DouyinHLODNodeSettings` | 物体级控制：`Permanent`（常驻）/ `Atomic`（不可拆分） |
| `DouyinStreamingService` | 运行时只读查询区域状态、订阅区域/actor 变化事件 |

**运行时不能做的（官方明确）：**

- 强制加载/卸载指定区域 ❌
- 直接设置区域状态 ❌
- 运行时修改加载距离等参数 ❌

> 流式加载是"平台替你按距离加载资源"，不是"让你运行时按需拉资源"。

---

## 6. 音视频等特殊资源

| 类型 | 说明 | 例子 |
| --- | --- | --- |
| 音频 | 通过 `DouyinActor.SetJumpAudioClip` / `SetFootstepAudioClips` 设置角色音效，`AudioClip` 为编辑器配置的资源 | 跳跃声、脚步声 |
| 视频 | 平台组件 **`DouyinVideoPlayer`** 支持按 URL 播放视频（`videoUrls`、`PlayVideo`、`SetPlaybackMode` 等） | 世界内大屏、剧情视频 |

> 📌 注意：`DouyinVideoPlayer` 是**平台封装**的视频播放能力（支持 URL 列表），这属于**平台提供的资源播放通道**，不等于"客户端可以用 UnityWebRequest 随便下载资源"。普通资源加载仍受黑名单约束。

---

## 7. Unity 支持 / 禁止清单（资源加载相关）

> 依据：《SDK API白名单》《SDK API黑名单》。

### 7.1 ✅ 可用的 Unity 命名空间（白名单）

| 命名空间 | 说明 |
| --- | --- |
| `UnityEngine` | 基础：`GameObject`、`Transform`、`Component`、`Vector3` 等 |
| `UnityEngine.UI` | UGUI |
| `UnityEngine.Audio` | 音频 |
| `UnityEngine.Video` | 视频 |
| `UnityEngine.AI` | 寻路 |
| `UnityEngine.Playables` / `Animations` | 动画/可播放 |
| `UnityEngine.Events` | 事件 |

### 7.2 ✅ 可用的平台组件（白名单）

`DouyinScript`、`DouyinScriptLoader`、`DouyinWorldRoot`、`DouyinObjectSync`、`DouyinNetworkGuid`、`DouyinSceneEnvironment`、`DouyinVideoPlayer`、`DouyinPlayerArea` 等。

### 7.3 ❌ 被禁止的能力（资源加载相关）

| 能力                                                              | 说明                                 |
| --------------------------------------------------------------- | ---------------------------------- |
| `Resources.Load`                                                | ❌ 官方明确不可用                          |
| `UnityEngine.Networking`（`UnityWebRequest` / `DownloadHandler`） | ❌ 黑名单禁用                            |
| `AssetBundle` 加载（`LoadFromFile` / `LoadFromMemory` 等）           | ❌ 黑名单反射禁用（`Load`/`LoadFrom` 等成员被禁） |
| `System.IO`（`File`、`StreamReader` 等）                            | ❌ 黑名单禁用                            |
| `Instantiate` / `Destroy`（对**网络对象**）                            | ❌ 必须用 `NetSpawn` / `NetDestroy`    |
| Lua `io` 库、`os.remove` / `os.rename` 等                          | ❌ 黑名单禁用                            |
| 反射加载程序集/类型（`Assembly.Load*`、`CreateInstance` 等）                 | ❌ 黑名单禁用                            |

### 7.4 ⚠️ 受限 / 需注意

- `GameObject.CreatePrimitive`（白名单内可用，但仅本地、非网络对象语义）。
- 非网络对象的纯本地特效/UI：`Instantiate` 是否可用需按**当前沙箱规则**判断 —— 官方文档强调网络对象必须走平台 API；本地对象在编辑器里预先摆好或按白名单方式创建更稳妥。

---

## 8. 常见误区与避坑

1. **误区：云构建产物可被创作者访问/读取** —— 不可，Resources 目录对创作者关闭。
2. **误区：可以用 UnityWebRequest 下载配置/资源** —— 不可，`UnityEngine.Networking` 整体黑名单。
3. **误区：网络对象用 `Instantiate` 就能同步** —— 不可，必须 `NetSpawn`，且对象需预先在 `DouyinWorldRoot` 配置 key。
4. **避坑：ServerSpawn 对象别加 Rigidbody** —— 会造成 C/S 位置同步异常。
5. **避坑：网络对象 10000 上限** —— 动态生成要注意数量。
6. **避坑：资源热更** —— 只能重新发布世界版本，没有运行时热更通道。

---

## 9. 官方参考文档索引

- 创作文档：《支持动态加载资源吗？》《抖音虚拟世界开发模式简介》《网络对象生成配置》《Douyin World Root 组件》《世界流式能力》《调用Unity API》《获取更多资源》
- API：`DouyinObjectService.NetSpawn` / `NetDestroy` / `GetDouyinObject`；`DouyinActor.NetSpawn`；DS 的 `ServerSpawn` / `ServerDestroy`；`DouyinVideoPlayer.*`；`DouyinActor.SetJumpAudioClip` / `SetFootstepAudioClips`
- 规则：《SDK API白名单》《SDK API黑名单》
