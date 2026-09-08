# 抖音虚拟世界 SDK 详解（六）：服务端数据怎么拿？Excel 配置怎么进世界？

> 面向对象：客户端/服务端程序员、需要对接配置的同事
> 定位：回答两个实操问题——
> 1. **我们服务端的数据，客户端怎么拿到？**
> 2. **我们有 Excel 表，应该导出成 Lua 资源文件吗？**
> 关联资料：《Dedicated Server 开发模式详解》《数据存储详解》《数据存储使用说明》《自定义 Module Script》《支持动态加载资源吗？》

---

## 目录

1. [先分清：三种"数据"对应三条通道](#1-先分清三种数据对应三条通道)
2. [通道一：随包配置（Excel → Lua 资源文件）](#2-通道一随包配置)
3. [通道二：DS 服务端下发（RemoteEvent / RemoteFunction）](#3-通道二ds-服务端下发)
4. [通道三：平台数据存储 DataStore](#4-通道三平台数据存储-dataStore)
5. [Excel 到底该导出成什么？为什么是 Lua 而不是 JSON？](#5-excel-到底该导出成什么)
6. [Excel → Lua 导出规范与示例](#6-excel--lua-导出规范与示例)
7. [把动作表串起来：一个完整链路示例](#7-把动作表串起来一个完整链路示例)
8. [常见误区与避坑](#8-常见误区与避坑)
9. [官方参考文档索引](#9-官方参考文档索引)

---

## 1. 先分清：三种"数据"对应三条通道

在抖音虚拟世界里，"服务端的数据"要分清它属于哪种性质，再选通道：

| 数据性质 | 典型例子 | 正确通道 | 更新方式 |
| --- | --- | --- | --- |
| **静态配置**（变化不频繁、所有玩家一致） | 动作表、道具表、关卡表、商品表 | **随包配置：Excel → Lua 资源** | 重新发布世界版本 |
| **实时数据**（房间内动态变化） | 服务端判定结果、动作指令、状态广播 | **DS 通信：RemoteEvent / RemoteFunction** | 实时 |
| **持久化数据**（跨局、跨天保存） | 玩家金币、背包、签到、存档 | **平台 DataStore** | 实时读写 |

> ⚠️ **判断口诀**：**要"发下去"的用 Lua 配置；要"算出来"的用 DS 通信；要"存下来"的用 DataStore。**

---

## 2. 通道一：随包配置（Excel → Lua 资源文件）

### 2.1 为什么静态配置必须随包

抖音虚拟世界**没有运行时读文件/下载资源**的能力（`System.IO`、`UnityWebRequest` 全被禁用，详见《03-本地JSON与数据格式》）。所以"动作表、道具表"这类**所有玩家都一样的静态配置**，唯一可靠的做法是：**在编辑器阶段把 Excel 导出成 Lua 表，随世界包发布。**

### 2.2 Lua 配置在运行时怎么被使用

自定义脚本目录结构（《自定义 Module Script》）：

```
CustomScripts/
├── index.lua            ← 入口，先被加载执行
├── Config/
│   └── GameConfig.lua   ← 配置表（由 Excel 导出）
└── ItemSystem/
    └── ItemManager.lua
```

```lua
-- index.lua：加载配置
local Config = require("Config/GameConfig.lua");
```

```lua
-- ItemManager.lua：用相对路径引用配置
local Config = require("../Config/GameConfig.lua");
_G.ItemManager = {}
function ItemManager:GetItem(id)
    return Config.Items[id]
end
return ItemManager
```

> 关键：脚本目录必须放在 `DouyinScriptLoader` 的 **Custom Scripts Folder** 字段指向的文件夹，且目录下必须有 `index.lua`，否则上传世界会报错。

---

## 3. 通道二：DS 服务端下发（RemoteEvent / RemoteFunction）

### 3.1 适用场景

"实时算出来的数据"——比如服务端校验动作是否合法、下发当前局的状态、广播给所有客户端。**只有 DS 模式有真正的服务端**（`DouyinApplication.isServer`）。

### 3.2 两种通信方式

| 方式 | 方向 | 适合 |
| --- | --- | --- |
| `DouyinRemoteEvent` | 单向（C→S 或 S→C），不需要响应 | 广播动作指令、通知 |
| `DouyinRemoteFunction` | 双向（C↔S），带响应 | 客户端请求 → 服务端校验 → 返回结果 |

### 3.3 客户端"拿到服务端数据"的两种写法

```lua
-- 写法 A：客户端主动请求（RemoteFunction，带响应）
ClientToServerFunc:InvokeServer(function(...)
    local resp = {...}               -- 服务端返回的数据
    for _, v in ipairs(resp) do print("拿到服务端数据:", v) end
end, "请求参数")

-- 写法 B：服务端主动推送（RemoteEvent，广播/单发）
ServerToClientEvent.onClientEvent:AddListener(function(...)
    local args = {...}               -- 服务端推来的数据
    for _, v in ipairs(args) do print("服务端推送:", v) end
end)
```

### 3.4 ⚠️ 硬性限制（务必告诉服务端同事）

- **只能传基础类型**：`bool, byte, short, int, long, float, double, string`。
- **不能传 table / 对象 / 二进制**。
- **复杂结构**：用 `dkjson.encode` 拼成 JSON 字符串传，对面 `dkjson.decode` 还原。
- **不保证 100% 送达**，接收方断线不补发。

---

## 4. 通道三：平台数据存储 DataStore

### 4.1 适用场景

需要**跨局保存**的数据：玩家金币、背包、签到记录、存档位置。

### 4.2 使用要点（《数据存储详解》《数据存储使用说明》）

1. 所有操作必须在 `DATASTORE(function() ... end)` 代码块内，否则报 **-10034**。
2. 存的是**字符串**：Lua 表用 `dkjson.encode` 序列化后写入，读取后 `dkjson.decode` 还原。
3. 键结构：`gameName + storeKey + dataKey` 唯一标识一条数据。
   - 账号级：`gameName="sim_game", storeKey="player_"..playerOpenID, dataKey="coin"`
   - 小火人级：`storeKey="pet_"..petOpenID`
4. 限制：单个 value 约 **6000 字符**、单个 DataStore 约 **1000 个 key**、dataKey 最长 128 字符。
5. **DS 模式下，数据存储必须写在服务端脚本**，客户端调用会报 **-11002**。

```lua
-- 示例：读玩家金币
DATASTORE(function()
    local ok, store = DouyinDataService.GetDataStore("sim_game", "player_"..openID, false)
    if ok == 0 then
        local ok2, value = store:GetData("coin")
        if ok2 == 0 then
            print("金币:", tonumber(value))
        end
    end
end)
```

---

## 5. Excel 到底该导出成什么？为什么是 Lua 而不是 JSON？

### 5.1 直接回答

> **是的，应该让策划/配置把 Excel 导出成 Lua 资源文件（`.lua` 表）。** 这是抖音虚拟世界唯一"原生、顺滑、随包可用"的配置形态。

### 5.2 为什么不是 JSON / CSV / 二进制？

| 格式                             | 运行时是否可直接用      | 说明                                     |
| ------------------------------ | -------------- | -------------------------------------- |
| **Lua 表**                      | ✅ 直接 `require` | 平台亲儿子，无需解析、无加载限制                       |
| JSON 文件                        | ❌ 不能读文件        | 只能运行时 `dkjson.decode` 处理**字符串**，文件加载被禁 |
| CSV / Excel 文件                 | ❌ 不能读文件        | 运行时无解析器                                |
| 二进制 / Proto                    | ❌ 不能读文件、通信也不支持 | 无官方支持                                  |
| JSON **字符串**（存 DataStore/同步变量） | ✅ 可            | 但那属于"运行时数据"，不是"静态配置"                   |

> 结论：**Excel → Lua 表（静态配置）** 和 **运行时 JSON 字符串（动态数据）** 是两回事。前者解决"配置怎么进游戏"，后者解决"数据怎么在端上传递"。

### 5.3 Excel → Lua 的推荐工作流

```
策划维护 Excel（动作表/道具表/关卡表）
      │  配置导出工具（编辑器脚本/本地工具）
      ▼
生成 Lua 表文件（Config/xxx.lua）
      │  放入自定义脚本目录（DouyinScriptLoader 指向）
      ▼
随世界包发布
      ▼
运行时 require 使用
```

---

## 6. Excel → Lua 导出规范与示例

### 6.1 推荐的导出结构

用"ID 为 key 的嵌套表"结构，便于 O(1) 查询：

```lua
-- Config/ActionConfig.lua（由 Excel "动作配置表" 导出）
local ActionConfig = {
    [1001] = {
        id     = 1001,
        name   = "wave",
        animName = "Anim_Wave",      -- 对应 Unity 工程内动画资源名
        mask   = "UpperBody",
        cd     = 5,
        unlockLevel = 1,
    },
    [1002] = {
        id     = 1002,
        name   = "dance",
        animName = "Anim_Dance",
        mask   = "WholeBody",
        cd     = 10,
        unlockLevel = 3,
    },
}
return ActionConfig
```

### 6.2 导出工具建议（可选）

- 用 Unity 编辑器脚本（`[MenuItem]`）或独立 Python/Node 脚本读 `.xlsx`，输出 Lua。
- 输出格式保持稳定：**首列 `id` 作为外层 key**，其余列作为字段。
- 字段命名统一 snake_case；枚举值（mask 等）建议导出为字符串，运行时映射到 `DouyinAnimatorMask`。

### 6.3 运行时把"配置名"映射到"真实资源"

Lua 表里存的是**资源名字符串**（因为 Lua 拿不到编辑器里的对象引用？——不，其实可以，见下方说明），更稳妥的做法是：**在 Unity 编辑器里，把 AnimationClip 以 `---@var` 注释绑定，或维护一个 名称→Clip 的映射**：

```lua
---@var ActionClips:UnityEngine.AnimationClip[]  -- 在脚本里声明/拖拽
---@end

local clipByName = {}
for _, clip in ipairs(ActionClips) do
    clipByName[clip.name] = clip
end

-- 用 Excel 导出的配置：ID → 动画名 → 真实 Clip
function PlayAction(actionId)
    local cfg = ActionConfig[actionId]
    if not cfg then return end
    local clip = clipByName[cfg.animName]
    if clip then
        DouyinActorService.GetLocalActor():PlayAnimation(clip)
    end
end
```

> 这样：**策划只改 Excel**（加行/改参数）→ 重新导出 Lua → 重新发布；客户端代码零改动。新动作**必须**在 Unity 工程里有对应动画资源并随包发布。

---

## 7. 把动作表串起来：一个完整链路示例

把"静态配置 + 服务端指令"组合成最终方案：

```lua
-- ① 客户端：Excel 导出的动作配置（随包）
local ActionConfig = require("Config/ActionConfig.lua")

-- ② 客户端：服务端下发动作ID → 查表 → 播放
ServerToClientEvent.onClientEvent:AddListener(function(actionId)
    local cfg = ActionConfig[actionId]           -- 查本地配置表
    if cfg then
        local clip = clipByName[cfg.animName]     -- 取本地动画资源
        if clip then
            DouyinActorService.GetLocalActor():PlayAnimation(clip)
        end
    end
end)
```

```
[服务端 DS]
  校验通过 → FireAllClients(actionId)
        │
        ▼
[客户端]
  收到 actionId → ActionConfig[actionId]（Excel导出的Lua表）→ clipByName[animName] → PlayAnimation
```

**职责划分：**

- **策划改 Excel** → 决定"有哪些动作、参数、解锁条件"。
- **服务端下发 ID** → 决定"这个玩家此刻能不能播、播哪个"。
- **客户端播本地动画** → 表现层。

---

## 8. 常见误区与避坑

1. **误区：Excel 导出成 JSON 文件放包里读** —— 不能，运行时读不了文件。
2. **误区：配置放服务端数据库，客户端随时拉** —— 静态配置走 Lua 随包；DataStore 只放玩家个人数据。
3. **误区：RemoteEvent 能传整个表格/对象** —— 只能传基础类型，复杂结构用 JSON 字符串。
4. **避坑：脚本目录必须有 index.lua** —— 否则上传世界报错。
5. **避坑：DS 模式数据存储只能在服务端** —— 客户端调报 -11002。
6. **避坑：Excel 加新动作 ≠ 客户端能播** —— 新动作的动画资源必须同时进 Unity 工程随包发布；否则查表找不到 Clip。
7. **避坑：DataStore 单 value 6000 字符** —— 大配置别塞 DataStore，放 Lua 表。

---

## 9. 官方参考文档索引

- 创作文档：《自定义 Module Script》《Module Script 介绍》《数据存储详解》《数据存储使用说明》《Dedicated Server 开发模式详解》《支持动态加载资源吗？》
- API：`DouyinRemoteEvent.*` / `DouyinRemoteFunction.*`、`DouyinDataService.GetDataStore`、`DouyinActor.PlayAnimation`
- 规则：《SDK API白名单》《SDK API黑名单》
