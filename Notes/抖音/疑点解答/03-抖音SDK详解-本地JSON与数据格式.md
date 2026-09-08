# 抖音虚拟世界 SDK 详解（三）：能否加载本地 JSON 文件？

> 面向对象：抖音虚拟世界创作者、服务端/客户端程序员
> 定位：直接回答"抖音 SDK 能否加载本地 JSON"，并**横向拓展**到二进制、Protobuf、CSV、Lua 配置等开发者关心的数据形态，附 Unity 支持/禁止清单。
> 关联资料：《数据存储详解》《数据存储使用说明》《自定义 Module Script》《Module Script 介绍》《SDK API黑名单》。

---

## 目录

1. [直接回答](#1-直接回答)
2. [为什么不能？沙箱权限分析](#2-为什么不能)
3. [那 JSON 在 SDK 里到底能用在哪？](#3-那-json-在-sdk-里到底能用在哪)
4. [配置数据怎么带进世界：可行替代方案](#4-配置数据怎么带进世界)
5. [横向拓展：二进制 / Protobuf / CSV / 其他格式](#5-横向拓展)
6. [Unity 支持 / 禁止清单（数据读取相关）](#6-unity-支持--禁止清单)
7. [常见误区与避坑](#7-常见误区与避坑)
8. [官方参考文档索引](#8-官方参考文档索引)

---

## 1. 直接回答

> **不能加载"任意本地 JSON 文件"。**
>
> - 抖音虚拟世界没有面向业务脚本的"读取本地文件 → 解析 JSON"通用 API。
> - 本地文件读取通道（`System.IO`、Lua `io`）和网络下载通道（`UnityWebRequest`）**全部被沙箱黑名单禁止**。
> - SDK 中唯一带 `LoadJson / JsonAsset` 的 `DouyinSceneEnvironment`，是**引擎内部**加载"场景效果参数配置"用的，**不是给业务读任意 JSON 的接口**，且 `JsonAsset` 对象"不能被创建成一个新类"。

**一句话：本地 JSON 文件加载 —— 原生不支持。**

---

## 2. 为什么不能？沙箱权限分析

抖音虚拟世界运行在一个 **Lua 沙箱**（xLua）中，权限由《SDK API白名单/黑名单》严格管控：

| 通道 | 状态 | 说明 |
| --- | --- | --- |
| `System.IO.File` / `StreamReader` | ❌ 黑名单 | `System.IO` 命名空间整体不可用 |
| Lua `io` 库 | ❌ 黑名单 | `io` 标准库不可用 |
| `UnityEngine.Networking.UnityWebRequest` | ❌ 黑名单 | 连网络拉文本都不行 |
| `AssetBundle.LoadFrom*` | ❌ 黑名单 | 反射相关加载成员被禁 |
| `os.execute / os.remove / os.rename` | ❌ 黑名单 | 文件系统操作被禁 |

> 也就是说，抖音虚拟世界**刻意没有开放"读文件"能力**，所有数据要么打进世界包由引擎/组件消费，要么走平台提供的存储/序列化 API。

---

## 3. 那 JSON 在 SDK 里到底能用在哪？

JSON **不是被禁止的**，只是"文件加载"被禁止。JSON **字符串的编解码**在运行时是支持的，典型场景：

### 3.1 平台提供的 JSON 序列化/反序列化

| API | 说明 |
| --- | --- |
| `dkjson.encode(table)` | Lua 表 → JSON 字符串 |
| `dkjson.decode(jsonStr)` | JSON 字符串 → Lua 表 |
| `Json.Encode(...)` / `Json.Decode(...)` | 平台封装（文档中亦出现） |

官方示例（《数据存储详解》《数据存储使用说明》）：

```lua
-- 表 → JSON 字符串（存入 DataStore）
local signInfos = { coin = 100, level = 5, items = {1,2,3} }
local jsonStr = dkjson.encode(signInfos)

-- JSON 字符串 → 表（读回后反序列化）
local data = dkjson.decode(jsonStr)
print(data.coin)
```

### 3.2 典型落地场景

1. **DataStore 存取**：数据库只能存字符串，把 Lua 表 JSON 序列化后写入，读取后反序列化。单个 value 约 6000 字符上限。
2. **同步变量传结构体**：官方明确"目前同步变量只支持基础值类型，如需结构体，用 JSON 序列化成字符串，在 `OnValueChange` 时反序列化"。
3. **本地 Lua 配置**：把"动作配置/商品配置/关卡配置"写成 Lua 表，运行时直接 `require` 使用。

### 3.3 唯一的"JSON 资源"类 API（⚠️ 不是给业务用的）

| API | 说明 |
| --- | --- |
| `DouyinSceneEnvironment.JsonAsset` | "返回场景效果参数配置表，该对象**通过读取 json 文件获取**，并且**不能被创建成一个新类**" |
| `DouyinSceneEnvironment.LoadJson(SceneEnvironmentSetting, bool load = true)` | "加载一个 json asset 的数据对象，对**环境参数**进行配置" |

> 这两个是引擎加载场景光照/雾/后处理等环境配置的机制。你不能用它读自己项目的任意 JSON。

---

## 4. 配置数据怎么带进世界：可行替代方案

既然不能读本地 JSON 文件，开发者把"数据配置"带进世界的常规手段有：

| 方案 | 做法 | 适合 |
| --- | --- | --- |
| **Lua 配置表（最常用）** | 把配置写成 `.lua`，放在自定义脚本目录，用 `require` 引入（`index.lua` 为入口） | 动作/道具/关卡/商品配置 |
| **DataStore + JSON** | 配置存平台 DataStore，运行时 `dkjson.decode` 读成表 | 需动态修改的配置、玩家数据 |
| **场景挂载组件** | 把字段配在 Unity 组件 Inspector 上，随场景序列化 | 固定参数（出生点、加载距离等） |
| **网络对象 + 同步变量** | 用 `---@varSync` 同步基础类型，字符串字段可放 JSON 字符串 | 运行时共享的状态数据 |

```lua
-- 动作配置示例（Lua 表）
local ActionTable = {
    [1] = { name = "wave",    clip = WaveClip,     mask = "UpperBody" },
    [2] = { name = "dance",   clip = DanceClip,    mask = "WholeBody" },
}
-- 使用时按 ID 查表，再 PlayAnimation(clip)
```

> 这套方案正好支撑"服务端下发动作 ID → 客户端查本地表播放"的架构（详见《服务端调用》文档）。

---

## 5. 横向拓展

> 你问的是 JSON，我们把它放到"数据格式"全景里看：**二进制、Protobuf、CSV、YAML 等，在抖音虚拟世界里分别是什么地位？**

### 5.1 二进制（byte[]）

| 问题 | 答案 |
| --- | --- |
| 能读本地二进制文件吗？ | ❌ 不能。`System.IO.File.ReadAllBytes` 被禁止 |
| 能通过网络下载二进制吗？ | ❌ 不能。`UnityWebRequest` 被禁止 |
| 二进制**数据**（byte 数组）能否在通信中传输？ | ⚠️ 有限。RemoteEvent/RemoteFunction/消息互通**只支持基础类型**，官方列出的基础类型中**未包含 byte[] 数组**；`byte` 单值可以，但数组/table 不可 |
| 同步变量能存二进制吗？ | ❌ 不支持 byte[]。同步变量支持基础类型 + List/Dictionary（值类型为所列基础类型），**不含 byte[]** |

> 📌 结论：**二进制文件加载与二进制大块传输都不受支持**。要做二进制协议，得先把 byte 数组用基础类型（如字符串编码）表达，且注意 RemoteEvent 不支持 table，只能拼成字符串/枚举传递。

### 5.2 Protobuf / Proto

| 问题 | 答案 |
| --- | --- |
| 能用 protobuf 序列化吗？ | ⚠️ **非常受限**。Lua 沙箱内没有官方 protobuf 库；第三方库需要打进项目并通过白名单，**当前白名单未收录** |
| 能用 `.proto` 文件定义协议吗？ | ❌ 不能读本地 `.proto` 文件（没有文件读取能力） |
| 编译后的 protobuf 消息对象能传吗？ | ❌ 不能跨客户端/服务端传对象；通信只认基础类型 |
| 平台有 protobuf 支持吗？ | ❌ 文档中**无任何 protobuf / Protocol Buffers 支持** |

> 📌 结论：**抖音虚拟世界当前不支持 protobuf 体系**。跨端数据统一用"基础类型 + JSON 字符串（dkjson）"表达。

### 5.3 CSV / 表格配置

| 问题 | 答案 |
| --- | --- |
| 能读本地 CSV 文件吗？ | ❌ 不能（同文件读取禁令） |
| 能用表格（Excel/CSV）做配置吗？ | ⚠️ 可以，但需在**编辑器阶段**转成 Lua 表或场景组件字段后再打包；运行时**不能再读原始 CSV** |

### 5.4 其他格式小结

| 格式 | 本地文件加载 | 运行时编解码 |
| --- | --- | --- |
| JSON | ❌ | ✅ `dkjson.encode/decode`、`Json.Encode/Decode` |
| 二进制 byte[] | ❌ | ❌ 无官方二进制编解码；通信不支持 byte[] |
| Protobuf | ❌ | ❌ 无官方支持 |
| CSV / YAML / XML | ❌ | ❌ 无官方解析器；XML 等需第三方且未过白名单 |
| Lua 表 | ✅ `require`（这是平台亲儿子） | ✅ 运行时直接可用 |

> **本质规律：抖音虚拟世界把"数据载体"统一收敛到「Lua 表」和「JSON 字符串」两种形态。** 其他格式都需要在编辑器阶段转换，运行时不再有"读文件 + 解析"环节。

---

## 6. Unity 支持 / 禁止清单（数据读取相关）

| 能力                          | 状态    | 说明                                                            |
| --------------------------- | ----- | ------------------------------------------------------------- |
| `UnityEngine.TextAsset` 引用  | ⚠️ 受限 | TextAsset 作为工程内资源可引用、可读 `.text`，但**不能运行时从磁盘/网络加载新 TextAsset** |
| `UnityEngine.JsonUtility`   | ⚠️ 谨慎 | 属于 `UnityEngine` 命名空间（白名单），但文档未作为推荐路径；平台推荐用 `dkjson`          |
| `System.IO` 全家              | ❌ 禁止  | 黑名单                                                           |
| `UnityEngine.Networking` 全家 | ❌ 禁止  | 黑名单                                                           |
| Lua `io`                    | ❌ 禁止  | 黑名单                                                           |
| 反射加载程序集/类型                  | ❌ 禁止  | 黑名单（`Assembly.Load*`、`CreateInstance` 等）                      |
| `dkjson` / `Json`（平台封装）     | ✅ 支持  | 运行时 JSON 编解码唯一推荐通道                                            |

> 🔧 补充：`Module Script` 会被 Unity 在场景保存时**序列化成二进制数据**存入场景 —— 这是引擎内部行为，与业务能否读二进制文件无关。

---

## 7. 常见误区与避坑

1. **误区：`DouyinSceneEnvironment.LoadJson` 能读我的配置文件** —— 不能，它只加载场景环境参数。
2. **误区：UnityWebRequest 能拉 JSON 配置** —— 不能，整个 `UnityEngine.Networking` 被禁。
3. **误区：同步变量能存结构体/byte[]** —— 不能，只有基础类型；结构体用 JSON 字符串绕。
4. **误区：RemoteEvent 能传 table/二进制** —— 不能，只支持基础类型（bool/byte/short/int/long/float/double/string）。
5. **避坑：DataStore 单 value 约 6000 字符** —— 大 JSON 需拆分存储。
6. **避坑：配置放 Lua 而不是 JSON 文件** —— 这是平台最顺滑的做法。

---

## 8. 官方参考文档索引

- 创作文档：《数据存储详解》《数据存储使用说明》《自定义 Module Script》《Module Script 介绍》
- API：`DouyinSceneEnvironment.JsonAsset` / `LoadJson`
- 规则：《SDK API白名单》《SDK API黑名单》
