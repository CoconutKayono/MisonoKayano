# DSTemplate 数据存储详解

本文档说明 DSTemplate 中玩家持久化数据的完整链路，重点介绍数据域、玩家聚合根、内存缓存、DataStore、首包、重同步以及新增数据域时的改动点。

## 1. 数据存储总体模型

服务端的数据链路为：

~~~text
业务协议 → Server*Manager → ServerPlayerData 聚合根
         → Server*Data 数据域 → ServerDataCache
         → ServerDataStoreManager → 平台 DataStore 云 KV
~~~

客户端只保留内存镜像：

~~~text
ServerPlayerData 首包 / 重同步
        ↓
ClientPlayerData
        ↓
Client*Data
~~~

因此：

- 服务端是持久化数据的唯一权威；
- 客户端数据域不做本地持久化；
- 客户端写入必须经过 C2S 协议；
- 服务端数据修改先写内存快照并标脏，之后由统一 Flush 落盘。

## 2. 数据域与聚合根

### 2.1 数据域

一个数据域代表玩家持久化数据的一块分片，通常对应一份 KV 记录和一份内存快照，例如：

~~~text
actor / bag / ranking / social / achievement
~~~

服务端域继承 ServerDataBase，客户端域继承 ClientDataBase。

### 2.2 服务端聚合根

ServerPlayerData 是“一名玩家所有持久化数据”的统一入口，按 openId 持有各个 Server*Data：

~~~lua
ServerPlayerData = {
    actorData = ServerActorData,
    bagData = ServerBagData,
    rankingData = ServerRankingData,
    socialData = ServerSocialData,
    achievementData = ServerAchievementData,
}
~~~

业务 Manager 通过以下方式访问：

~~~lua
local agg = ServerPlayerDataManager.Get(openId)
local bagData = agg and agg.bagData
~~~

不要绕过聚合根直接创建一个数据域，也不要直接调用 ServerDataCache 修改数据。

### 2.3 客户端聚合根

ClientPlayerData 是服务端首包的客户端镜像，只负责创建、持有和销毁各个客户端数据域：

~~~lua
local agg = GetMol("ClientPlayerData")
local achievementData = agg and agg.achievementData
~~~

客户端数据写入通常由服务端回包调用：

~~~lua
achievementData:ReplaceRootDataFromServer(serverData)
~~~

## 3. ServerDataBase 的核心接口

| 方法 | 作用 |
| --- | --- |
| Get(key?) | 不传 key 返回整表快照；传 key 返回指定字段 |
| Create(key, value) | 新增字段并标脏 |
| Add(key, value) | Create 的别名 |
| Update(key, value) | 覆盖写入字段并标脏 |
| Remove(key) / Delete(key) | 删除字段并标脏 |
| SetCache(snapshot, markDirty) | 整体替换快照；框架 Load 回写时通常传 false |
| Load(callback) | 从 DataStore 读取、归一化并写入内存 |
| Save(force, callback?) | 强制或按脏标记写入 DataStore |
| IsLoaded() | 判断该域首次加载是否完成 |
| IsDirty() | 判断是否存在未落盘修改 |
| GetDefaultValue() | 返回默认数据结构 |
| NormalizeValue(raw) | 规整云端旧数据、nil 或缺字段 |

### 3.1 推荐的业务写法

~~~lua
local achievements = achievementData:Get("achievements") or {}
achievements[achievementId] = true
local latest = achievementData:Update("achievements", achievements)
~~~

这种写法会正确设置脏标记并参与版本号更新。

### 3.2 不推荐的写法

~~~lua
local snapshot = achievementData:Get()
snapshot.achievements[id] = true
achievementData:SetCache(snapshot)
~~~

直接修改 Get 返回的整表再自行 SetCache，容易漏掉 markDirty，也可能导致重同步版本号没有递增。只有确实需要整体替换时，才使用：

~~~lua
achievementData:SetCache(snapshot, true)
~~~

业务 Logic 不应直接调用 ServerDataCache.SetCacheData。

## 4. DataStore 命名约定

当前模板的 ServerDataBase:__init 使用 4 个参数：

~~~lua
ServerDataBase.__init(self,
    playerOpenId,
    domainKey,
    scopePrefix,
    dataKey
)
~~~

参数含义：

| 参数 | 含义 | 示例 |
| --- | --- | --- |
| playerOpenId | 玩家身份 | "abc123" |
| domainKey | 聚合层内唯一的域 key | "achievement" |
| scopePrefix | 与 openId 拼接的 scope 前缀 | "achievement_" |
| dataKey | scope 下的 DataStore 数据键 | "achievement_data" |

DataStore 命名空间由基类固定为：

~~~lua
STORE_NAMESPACE = "sim_game"
~~~

子类不要再传旧版本的 storeName 第五个参数。

新增域的示例：

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
~~~

## 5. 数据归一 NormalizeValue

数据域必须负责把云端旧数据转换为当前版本需要的结构，不能把归一逻辑散落到业务 Manager 中：

~~~lua
function ServerAchievementData:NormalizeValue(rawValue)
    if type(rawValue) ~= "table" then
        return { achievements = {} }
    end
    if type(rawValue.achievements) ~= "table" then
        rawValue.achievements = {}
    end
    return rawValue
end
~~~

这样可以处理：

- 首次进入时没有旧数据；
- 老版本数据缺少新字段；
- 云端数据类型错误；
- 数据结构从旧版本升级到新版本。

## 6. ServerDataCache 与版本号

ServerDataCache 维护：

~~~text
playerDatas[openId][domain]     # 内存快照
dirty<key>                      # 是否有未落盘修改
domainVersions[openId][domain]  # 重同步版本号
~~~

只有加入 versionedDomains 白名单的数据域才会维护版本号：

~~~lua
local versionedDomains = {
    actor = true,
    bag = true,
    ranking = true,
    social = true,
    achievement = true,
}
~~~

新增域如果没有加入白名单，首包可能仍能拿到数据，但断线重连时无法按域版本感知变更。

域数据通过 SetCache(..., markDirty = true) 或 Create / Update 等接口发生有效修改时，版本号递增。服务端重同步会比较：

~~~text
clientVersion < serverVersion
或
missingDomains[domain] == true
~~~

## 7. 玩家生命周期与落盘

### 7.1 进入房间

~~~text
GameServerModule.OnPlayerJoined
  → ServerPlayerManager.OnPlayerJoined
  → ServerPlayerDataManager.GetOrCreate(openId)
  → agg:LoadIntoCache()
~~~

各数据域并发加载。模板示例中通常有 4 组回调：

- bag；
- ranking；
- actor + social；
- achievement 或其他新增域。

所有回调完成后，聚合根才认为玩家数据加载完成。若客户端请求首包时尚未完成，服务端会把请求挂起，加载结束后再补发。

### 7.2 定时 Flush

ServerPlayerManager.TickFlush 默认以 5 分钟为节拍，遍历在线玩家：

~~~lua
agg:Flush(false)
~~~

ServerDataBase:Save(false) 只有在域为脏时才真正写入，避免每帧或每次 Tick 都写 KV。

### 7.3 离开房间

玩家离开时执行：

~~~text
agg:ClearPending()
→ agg:Flush(true)
→ ServerDataCache.ClearCacheData(openId)
→ ServerPlayerDataManager.Remove(openId)
→ RemovePlayer(openId)
→ coroutine.yield(WaitForSeconds(5))
~~~

Flush(true) 确保离房前进行全量写回；宿主脚本额外等待一段时间，为异步落盘协程留出执行窗口。

## 8. 首包与重同步

### 8.1 首包

服务端 SendPlayerDataToPlayer 构造全量快照：

~~~lua
local playerData = {
    playerData = self.actorData:Get(),
    bagData = self.bagData:Get(),
    rankingData = self.rankingData:Get(),
    socialData = self.socialData:Get(),
    achievementData = self.achievementData:Get(),
    versions = ServerDataCache.GetDomainVersionMap(openId),
}
~~~

注意历史兼容命名：服务端首包的 actor 域字段可能叫 playerData，客户端聚合层统一映射成 actorData，不要为了改名破坏现有协议。

### 8.2 重同步

客户端断线重连或发现本地缺域时发送 CSResyncPlayerData，携带：

- 本地已知版本号 knownVersions；
- 缺失域 missingDomains。

服务端按 resyncDomains 遍历并返回：

- changed：实际变化的数据域；
- versions：最新域版本号；
- changedDomains：本次变更的域清单。

## 9. 客户端数据约定

ClientDataBase 是纯内存基类，核心能力包括：

- _data：当前数据；
- Get(key, default)；
- GetData()；
- Count()；
- IsLoaded() / MarkLoaded()；
- EmitEvent()；
- ReplaceRootDataFromServer(rootTable)：服务端快照整表覆盖。

客户端数据域示例：

~~~lua
ClientAchievementData = BaseClass:DefineClass(
    "ClientAchievementData",
    ClientDataBase
)

function ClientAchievementData:ApplyServerData(newData)
    assert(type(newData) == "table")
    self:ReplaceRootDataFromServer(newData)
end
~~~

客户端 Model 不负责发请求、不直接改服务端数据。业务 System 负责发 C2S，收到 SC 后调用 ApplyServerData 或 ReplaceRootDataFromServer。

## 10. 新增一个数据域的检查清单

服务端：

- [ ] 新建 Server<Name>Data.lua；
- [ ] 继承 ServerDataBase；
- [ ] 实现 NormalizeValue；
- [ ] 在 Server/Data/index.lua require；
- [ ] ServerPlayerData.__init 创建域实例；
- [ ] AreAllDomainsLoaded 加 IsLoaded；
- [ ] 首包 payload 加域字段；
- [ ] resyncDomains 加域名和分支；
- [ ] LoadIntoCache 加 Load 回调，pendingAsyncCount +1；
- [ ] Flush 加 Save；
- [ ] ServerDataCache.versionedDomains 加域名。

客户端：

- [ ] 新建 Client<Name>Data.lua；
- [ ] 继承 ClientDataBase；
- [ ] 在 ClientPlayerData.__init 创建；
- [ ] 在 ClientPlayerData.__delete 销毁；
- [ ] PlayerSystem 首包构造加域字段；
- [ ] PlayerSystem 重同步派发加域字段；
- [ ] PlayerSystem 缺域探测加域字段；
- [ ] PlayerSystem IOC 清理加域模型；
- [ ] Client/index.lua require 模型；
- [ ] Client/System/index.lua 或对应 System 注册模型使用。

## 11. 常见错误

### 首包没有新增域

检查 ServerPlayerData.SendPlayerDataToPlayer 是否加了字段，以及 PlayerSystem.OnSCRequestPlayerData 是否把字段传给 ClientPlayerData.New。

### 重连后数据没有更新

检查：

- resyncDomains 是否包含新域；
- SendResyncToPlayer 是否有该域分支；
- versionedDomains 是否包含新域；
- 客户端 PlayerDataApplyResyncChanged 是否调用了该域的 ApplyServerData。

### 数据修改后没有落盘

不要只修改 Get 返回的表；使用 Create / Update / Remove 标脏。检查 Flush 是否调用了新域的 Save。

### 客户端本地数据与服务端发散

不要把客户端 Model 当成写入入口。应由客户端发 C2S，服务端修改并保存，再通过 SC 回包更新客户端镜像。

