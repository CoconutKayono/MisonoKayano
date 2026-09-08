# 抖音虚拟世界 SDK 详解（七）：DataStore 数据存储怎么用？必须是 DS 模式吗？

> 面向对象：客户端/服务端程序员、需要存玩家数据的同事
> 定位：完整讲清楚 **DataStore 怎么用**，以及最关键的选型问题——**必须开 DS（Dedicated Server）模式吗？**
> 关联资料：《数据存储使用说明》《数据存储详解》《数据存储限制说明》《数据存储错误码查询》《如何启用数据存储》《Dedicated Server 开发模式详解》。

---

## 目录

1. [先给结论：不强制 DS，但两种模式差别很大](#1-先给结论)
2. [DataStore 是什么、适合存什么](#2-datastore-是什么)
3. [第一步：启用数据存储能力](#3-第一步启用数据存储能力)
4. [核心用法：四步走](#4-核心用法四步走)
5. [常用 API 与代码示例](#5-常用-api-与代码示例)
6. [存储 JSON / 表数据](#6-存储-json--表数据)
7. [容量与限制（红线，务必看）](#7-容量与限制红线务必看)
8. [错误码速查](#8-错误码速查)
9. [常见误区与避坑](#9-常见误区与避坑)
10. [官方参考文档索引](#10-官方参考文档索引)

---

## 1. 先给结论

> **DataStore 不强制要求 DS 模式。Shared Mod（普通模式）下客户端可以直接调用 DataStore。**
>
> **但是**：如果你们用 DS 模式开发，那么**数据存储必须写在服务端脚本上，客户端脚本不允许调用 DataStore**（会报 -11002）。

| 开发模式 | 谁可以调 DataStore | 备注 |
| --- | --- | --- |
| **Shared Mod**（默认，不开 DS） | **客户端可以直接调** | 官方示例基本都是客户端调用 |
| **Dedicated Server（DS）** | **只能服务端脚本调** | 客户端调 → 报 **-11002** |

所以一句话：**"能不能在客户端用 DataStore" 取决于你们是不是 DS 模式。不开 DS → 可以；开了 DS → 不行（必须走服务端）。**

> 🔑 这个结论对你们很重要：如果只是"存玩家进度/金币"这种轻需求，**不用上 DS，客户端直接用 DataStore 即可**，架构最简单。只有需要"服务端校验/防作弊/公平性"时才上 DS，代价是存储逻辑也要挪到服务端。

---

## 2. DataStore 是什么、适合存什么

DataStore 是抖音虚拟世界提供的**持久化键值存储**，**独立于房间存在**：玩家分布在不同的房间，也能读写同一份数据。适合存：

- 玩家物品、装备、背包
- 关卡进度、存档位置
- 金币、积分、签到记录

> ⚠️ 不同世界之间数据不互通（各世界存储相互独立）。

两个实体类：

| 类                        | 说明                                       |
| ------------------------ | ---------------------------------------- |
| `DouyinDataStore`        | 通用键值存储，值可为 number / boolean / string / 表 |
| `DouyinOrderedDataStore` | 只能存**数值**，自动排序、分页（排行榜场景）                 |

获取对象统一入口：`DouyinDataService.GetDataStore(...)` / `GetOrderedDataStore(...)`。

---

## 3. 第一步：启用数据存储能力

默认情况下**不启用**，直接调用会失败。启用流程（《如何启用数据存储》）：

1. 点击 **上传按钮 > 上传新世界**。
2. 上传成功后，前往 **抖音虚拟创作平台 > 虚拟世界 > 选择你上传的世界 > 数据存储**。
3. 打开 **启用数据存储能力** 开关。

本地调试：
- 在 Unity 调试器里勾选 **启用数据存储**。
- 选择"已开通数据存储能力"的世界进行调试。

> 未启用时：编辑器写入会报 **-10015**；模拟器调用相关 API 会返回错误码。

---

## 4. 核心用法：四步走

1. **拿对象**：`DouyinDataService.GetDataStore(name, scope)`
2. **读写数据**：`store:GetData(key)` / `store:SetData(key, value)` 等
3. **所有 DataStore 代码必须包在 `DATASTORE(function() ... end)` 块内**，否则报 **-10034**
4. **序列化**：存表数据用 `dkjson.encode`，读回用 `dkjson.decode`

### 键结构设计

完整键 = `name` + `scope` + `key`。

- `name`：DataStore 名称（长度 ≤ 20）
- `scope`：作用域（长度 ≤ 50），**通常用玩家 ID 当 scope**（一玩家一 scope）
- `key`：数据字段名（长度 ≤ 128）

> 设计要点（来自官方"容量限制"文档）：**"一玩家一 scope"**，而不是"所有玩家塞进同一个 DataStore 的多个 key"。因为单个 DataStore 实例最多 1000 个 key，超过后新增写入会失败。

---

## 5. 常用 API 与代码示例

### 5.1 读写玩家数据（基础示例）

```lua
-- 保存/读取玩家金币（Shared Mod 客户端可直接调用）
local player = DouyinPlayerService.GetLocalPlayer()
if not player then return end

DATASTORE(function()
    -- 1. 获取 DataStore 对象（scope 用玩家ID）
    local ok, store = DouyinDataService.GetDataStore("my_world", "player_" .. player.playerOpenID)
    if ok ~= 0 then
        print("获取 DataStore 失败, code:", ok)
        return
    end

    -- 2. 写数据
    local ok2 = store:SetData("coin", 100)
    if ok2 ~= 0 then print("写入失败, code:", ok2) return end

    -- 3. 读数据
    local ok3, value, info = store:GetData("coin")
    if ok3 == 0 then
        print("金币:", value)
    elseif ok3 == -10001 then
        print("数据不存在（新号），需要初始化")
    end
end)
```

### 5.2 增量更新（避免并发不一致）

`IncrementData` 是原子操作，适合"全局计数 / 多人并发改同一个值"：

```lua
DATASTORE(function()
    local ok, store = DouyinDataService.GetDataStore("my_world", "players_info")
    if ok ~= 0 then return end
    -- 玩家总数 +1
    ok, message = store:IncrementData("total_player_count", 1)
    if ok ~= 0 then
        print("增量失败, code:", ok, "msg:", message)
    end
end)
```

### 5.3 排行榜（OrderedDataStore）

```lua
-- 存分数（仅数值）
_, store = DouyinDataService.GetOrderedDataStore("game", "football")
store:SetData("user001", 10)
store:SetData("user002", 20)

-- 降序分页取排名（每页100）
_, pages = store:GetSortedData(false, 100, -1, 0)
_, value = pages:GetCurrentPage()
for k, v in pairs(value) do
    print("user:" .. k .. " score:" .. v.value)
end
```

> 上限：单个 OrderedDataStore 最多 **5000** 个键，超限需分片设计。

---

## 6. 存储 JSON / 表数据

DataStore 里如果直接存 Lua 表，读出来是 **string** 而不是 table。所以存表要用 JSON 序列化：

```lua
-- 存
local data = { coin = 100, level = 5, items = {1, 2, 3} }
local jsonStr = dkjson.encode(data)
store:SetData("player_data", jsonStr)

-- 读
local ok, value = store:GetData("player_data")
if ok == 0 then
    local t = dkjson.decode(value)
    print("金币:", t.coin, "等级:", t.level)
end
```

> 注意值大小限制：单条 value（JSON 序列化后）约 **6000** 字符（部分文档写 32767 字节，以 -10013 错误码的说明为准，两者都是"超长报错"）。大表请拆分存储。

---

## 7. 容量与限制（红线，务必看）

| 限制项 | 数值 | 说明 |
| --- | --- | --- |
| **单世界存储总容量** | **100 MB** | 超出部分失效，超限可联系运营 |
| `name` 长度 | ≤ 20 | `GetDataStore` 参数 |
| `scope` 长度 | ≤ 50 | `GetDataStore` 参数 |
| `key` 长度 | ≤ 128 | `SetData/GetData` 的 key |
| `value` 长度 | 约 6000 字符（超长报 -10013） | number/boolean/string |
| `metadata` 长度 | ≤ 1000 | 元数据 |
| **单个 DataStore 实例键数** | **1000** | 超限新增写入报错（-11005/-10014）；**已存在键更新不受影响** |
| **单个 OrderedDataStore 键数** | **5000** | 超限需分片（-11007） |
| **调用频率** | 默认 **900 次/分钟**/房间，峰值 1800 | 所有读写共享队列；超出失效（-11001） |

> 📌 频率红线很重要：房间内所有玩家共享这 900 次/分钟。如果你的玩法频繁读写，要控制调用频率，避免"一屋子人一起写"瞬间打爆限额。

---

## 8. 错误码速查

| 错误码 | 含义 |
| --- | --- |
| 0 | 成功 |
| -10001 | 数据不存在（新号场景，需初始化） |
| -10013 | 值大小超限 |
| -10015 | 未启用数据存储 |
| -10034 | 代码没放在 `DATASTORE()` 块内 |
| -10050 | DataStore 暂时不可用（网络问题，可重试） |
| -11001 | 存储请求频率超上限 |
| **-11002** | **DS 模式下客户端不可调用存储 API** |
| -11004 | 世界存储容量触达上限（100M） |
| -11005 | DataStore scope 键值对触达上限（1000） |
| -11007 | OrderedDataStore 触达上限（5000） |

> 完整清单见《数据存储错误码查询》。

---

## 9. 常见误区与避坑

1. **误区：必须开 DS 才能用 DataStore** —— 不是。Shared Mod（默认）客户端可直接用；**开了 DS 才反过来变成"只能服务端调"**。
2. **误区：DataStore 代码随便写在哪都行** —— 必须在 `DATASTORE(function() ... end)` 块内，否则 -10034。
3. **误区：直接存 Lua 表** —— 读出来是 string，要用 `dkjson.encode/decode` 序列化。
4. **误区：所有玩家塞同一个 DataStore 的不同 key** —— 单实例 1000 key 上限，正确做法是"一玩家一 scope"。
5. **避坑：频繁读写** —— 房间共享 900 次/分钟限额，注意频率控制与重试（-10050）。
6. **避坑：DS 模式客户端调存储** —— 一律走服务端脚本中转（客户端 RemoteFunction → 服务端 → DataStore → 返回）。

---

## 10. 官方参考文档索引

- 创作文档：《数据存储使用说明》《数据存储详解》《数据存储限制说明》《数据存储错误码查询》《如何启用数据存储》《Dedicated Server 开发模式详解》
- API：`DouyinDataService.GetDataStore / GetOrderedDataStore / CreateDataSetOptions`；`DouyinDataStore.GetData / SetData / IncrementData / UpdateData / RemoveData`；`DouyinOrderedDataStore`；`DouyinDataPages`
