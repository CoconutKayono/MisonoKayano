---
title: DouYinDancing 房间设置完整说明
aliases:
  - 房间设置
  - 舞台房间客户端与服务端逻辑
tags:
  - DouYinDancing
  - 房间设置
  - Lua
  - 客户端服务端
created: 2026-09-21
updated: 2026-09-21
source_revision: "68031e6 + 工作区未提交修改"
document_type: 当前实现说明
---

# DouYinDancing 房间设置完整说明

> [!info] 阅读依据
> 本文按 2026-09-21 读取的本地工作区源码整理，包含尚未提交的修改。源码根目录为 `D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate`。
> 文档说明当前代码如何工作、相关模块在哪里，以及与此前需求的差异。静态阅读不能代替 Unity 客户端与实际 DS 的联机验证；“退出和加入队伍无效果”的运行时原因仍未定位。

> [!important] 当前实现的几个关键事实
>
> - 模式选择、选曲确认先保存在设置页，点击“完成设置”才发出配置请求。
> - 完成设置费用仍为服务端硬编码 **100 金币**，带有 TODO。
> - 当前 `RoomSettingDataLib` 的各模式踢人费用都是 **0**，不能再按过去的 10000 金币理解。
> - 房主权限开关为 `false`，但服务端仍保留并维护房主字段。
> - 双人、心动模式完成设置时限制同一性别最多 3 人，超出时先移除后来加入者；开局还有另外的人数条件。
> - 当前选曲和踢人确认弹窗的调用层级为 **layer5**，被踢提示为 **layer6**。此前“前两者也用 layer6”的要求与当前实现不一致。
> - 当前选中的 `musicId` 已用于设置保存和 UI 展示，但正式开局仍走默认 BGM 链路；配置项 `GeQuPath` 尚未接到这条播放链上。

## 导航

- [[#1. 房间、舞台和数据归属]]
- [[#2. 配置表与编号规则]]
- [[#3. 页面职责与按钮入口]]
- [[#4. 模式和音乐的草稿机制]]
- [[#5. 完成设置的完整过程]]
- [[#6. 六个座位与三种设置面板]]
- [[#7. 加入舞台、选队与换座]]
- [[#8. 退出舞台和离场清理]]
- [[#9. 锁位与解锁]]
- [[#10. 手动踢人与金币检查]]
- [[#11. 模式人数整理与自动踢人]]
- [[#12. 机器人管理]]
- [[#13. 开始游戏与音乐播放的衔接]]
- [[#14. 网络协议与数据结构]]
- [[#15. 客户端同步、版本与生命周期]]
- [[#16. 弹窗层级、Prefab 和绑定]]
- [[#17. 提示文案与错误处理]]
- [[#18. 当前边界、差异与待确认项]]
- [[#19. 排查步骤与联机检查场景]]
- [[#20. 相关源码索引]]
- [[#21. 后续维护时需要一起考虑的内容]]

## 1. 房间、舞台和数据归属

### 1.1 本文中的“房间”是什么

项目把一间平台 DS 房间内的舞台维护为若干个独立的舞台房间。当前服务端常量：

| 项目 | 当前值 | 定义位置 |
| --- | --- | --- |
| 舞台数量 | 5 | `ServerStageManager.lua` 的局部常量 `STAGE_COUNT` |
| 每台座位数 | 6 | 服务端和相关 View 的 `SLOT_COUNT` |
| 默认查看舞台 | 1 | `RoomEnterView`、`StageInfoView` |
| 新建舞台默认模式 | 冠军，模式值 4 | `CreateStage` |
| 新建舞台默认音乐 | `musicId = 1` | `CreateStage` |
| 默认难度 | 1 | `CreateStage` |
| 默认阶段 | `idle` | `CreateStage` |
| 默认锁位 | 六格全部未锁 | `CreateLockedFlags` |

`CSStageJoin` / `CSStageLeave` 操作的是这套舞台占位和成员数据。退出舞台并不调用平台“离开整个抖音世界”的接口。

平台玩家进入或重连时，服务端发送舞台列表；**平台进入房间不等于已在舞台占座**。新手邀请界面确认可以通过 `NewbieGuideSystem:EnterChampionStage()` 另外发出入座请求。

### 1.2 谁负责哪些数据

| 层 | 职责 | 不能据此认定的事情 |
| --- | --- | --- |
| 设置页草稿 | 保存尚未提交的模式和音乐选择 | 草稿不表示服务端已改模式或歌曲 |
| 客户端 `StageSystem` | 保存列表、本站详情、本人座位，发送请求，通知 UI | 发包函数返回 `true` 不表示服务端成功 |
| 服务端 `ServerStageManager` | 决定成员、座位、锁位、模式、音乐、踢人和开局资格 | 服务端函数存在不等于当前运行的 DS 已执行了请求 |
| 服务端玩家数据域 | 读取性别，检查并更新金币 | 客户端金币显示不是扣费依据 |
| View / Widget | 展示快照、采集点击、管理弹窗 | 单独隐藏节点不会退出房间 |

舞台列表与占位保存在 **DS 内存**。金币和性别来自玩家数据系统。房间设置处理器没有把整套舞台成员和锁位写入玩家持久化存档。

### 1.3 总体交互

~~~mermaid
flowchart TD
    A["StageInfoView / RoomEnterView / Widget"] --> B["StageSystem：发送操作意图"]
    B --> C["C2S：客户端网络"]
    C --> D["ServerPacketRegister"]
    D --> E["ServerStageManager"]
    E --> F["舞台成员、座位、配置"]
    E --> G["服务端玩家数据：性别、金币"]
    E --> H["SCStageListSync / SCStageDetailSync"]
    H --> I["StageSystem：接受权威快照"]
    I --> J["ListChanged / DetailChanged"]
    J --> A
~~~

按钮 -> 请求 -> 服务端修改 -> 回包 -> UI 刷新，才构成一次完整操作。

## 2. 配置表与编号规则

### 2.1 RoomSettingDataLib

当前配置项只包含既有的业务字段：

| 字段 | 含义 |
| --- | --- |
| `ID` | 房间设置配置项 ID |
| `MoShiName` | 模式显示名称 |
| `ShiFouKaiFang` | 是否开放；数值 1 表示开放 |
| `TiRenJinBiXiaoHao` | 手动踢出真人时的金币消耗 |

表级开关 `EnableHostPermission = false` 控制已接入该开关的房主权限校验。

**配置项 ID 与玩法模式值不是同一组编号。**

| 配置项 ID | 显示名称 | 玩法枚举 | 实际 mode 值 | 当前开放 | 当前踢人费用 |
| --- | --- | --- | --- | --- | --- |
| 1 | 冠军模式 | `GuanJun` | 4 | 是 | 0 |
| 2 | 双人模式 | `ShuangRen` | 3 | 是 | 0 |
| 3 | 心动模式 | `XinDong` | 1 | 是 | 0 |
| 4 | 斗舞模式 | `DouWu` | 2 | 否 | 0 |

映射由 `MODE_BY_SETTING_ID` 根据 `GamePlayDataLib.Mode` 建立，缺失枚举时回退到当前的 4、3、1、2。**配置行没有 `stageModeID` 字段，也不需要新增这个字段。**

| 接口 | 作用 |
| --- | --- |
| `GetByID(settingId)` | 按配置项 ID 查配置 |
| `GetStageModeByID(settingId)` | 配置项 ID 转玩法 mode |
| `GetByMode(mode)` | 根据玩法 mode 查配置行 |
| `GetKickCostByMode(mode)` | 获取非负整数踢人费用；非法或缺失返回 nil |
| `IsModeOpen(mode)` | 查询是否开放；未知模式返回 false |

`RoomEnterView` 的三个 Toggle 使用配置项 1、2、3 查映射，不能直接把 Toggle 顺序当作 `mode` 传给服务端。

当前还有部分既有代码直接使用模式值，例如 `StageInfoView`、`UI_RoomSlot`、`StageSlotWidget` 和服务端枚举。以后调整玩法编号时，需要一起检查这些位置。

### 2.2 MusicDataLib

| 字段 | 含义 | 当前数据示例 |
| --- | --- | --- |
| `ID` | 音乐 ID；数值键与 ID 对齐 | 1、2 |
| `GeQuName` | 歌曲名 | 青花瓷、稻香 |
| `GeQuBPM` | UI 显示 BPM | 130、120 |
| `GeQuPath` | 歌曲资源路径字段 | 两首歌目前均为空字符串 |

当前两条数据：

| ID | 歌曲 | BPM | GeQuPath |
| --- | --- | --- | --- |
| 1 | 青花瓷 | 130 | 空 |
| 2 | 稻香 | 120 | 空 |

| 接口 | 作用 |
| --- | --- |
| `Get(id, defaultValue)` | 查歌曲，兼容点号和冒号调用 |
| `GetSortedMusicData()` | 返回按 ID 升序排序的歌曲数组 |
| `GetMusicData()` | 返回配置表本身 |
| `GetMusicNum()` | 返回歌曲条目数量 |

UI 使用排序后的条目生成列表，服务端通过 `MusicDataLib.Get(musicId)` 判断请求歌曲是否存在。

> [!note] 扩展配置时
> 保持数值键与 `ID` 对齐。当前 `Get()` 直接按数值键索引，不会扫描全表寻找相同的 `ID`。
> 选曲 UI 的列表在首次构建后复用；修改运行中的配置表不会自动重建已创建的条目。

### 2.3 相关配置和加载顺序

`Scripts/Common/index.lua` 先加载 `GamePlayDataLib`，再加载 `MusicDataLib`、`RoomSettingDataLib`，之后加载网络协议。

相关配置还有：

- `GamePlayDataLib`：玩法模式、站位、回合等数据。
- `StageDanceRules`：准备后的音乐与节奏规则、默认 BGM 等。
- `DanceDataLib`：正式对局评分相关；不决定设置页的金币消耗。

完成设置的 100 金币来自 `ServerStageManager.lua` 中的 `FINISH_SETTING_COST`，**目前未从上述配置表读取**。

## 3. 页面职责与按钮入口

### 3.1 RoomEnterView：房间设置页

| 绑定变量 | 当前职责 |
| --- | --- |
| `GuanJunToggle` | 选择冠军模式草稿 |
| `ShuangRenToggle` | 选择双人模式草稿 |
| `HeartToggle` | 选择心动模式草稿 |
| `BtnMusicSwitcher` | 打开 `UI_MusicSwitchView` |
| `TextMusicName` | 显示音乐草稿或当前已生效歌曲名 |
| `BtnFinishSetting` | 提交模式、音乐草稿 |
| `AddRobotBtn` | 立即请求添加机器人 |
| `BtnClose` | 清空模式/音乐草稿，关闭设置页并打开主菜单 |
| `BtnCancel` | 与 `BtnClose` 共用 `OnClose` |
| `UI_RoomSlotPanel` | 冠军座位容器的脚本绑定 |
| `UI_ChampionPanel` | 冠军面板显隐 |
| `UI_DoublePanel` | 双人面板显隐和座位脚本解析 |
| `UI_HeartPanel` | 心动面板显隐和座位脚本解析 |

当前脚本及 Prefab 使用的拼写是 **`BtnCancel`**。此前提到的 `BtnCancle` 不是当前变量名。

`SpectateBtn`、`MusicChooseDropdown`、`JoinPlayerBtn` 已不在当前 `RoomEnterView` 的绑定和操作入口中。设置页的入座入口是空座位控件。

`BindCloseBtn(callback)` 目前是空函数，不会保存或执行回调。

### 3.2 StageInfoView：主界面的房间信息区

主菜单上的房间模式、歌曲、BPM 和座位主要由 `StageInfoView` 负责。`UI_MainMenuView.prefab` 内嵌舞台信息 Prefab；当前 `MainMenuView.lua` 主要是其他菜单按钮及 TODO，不承担房间摘要同步。

| 场景节点名称 | StageInfoView 的脚本绑定 | 文本来源 |
| --- | --- | --- |
| `TextMode` | `TextStageMode` | `RoomSettingDataLib.GetByMode(stage.mode).MoShiName` |
| `TextMusicName` | `TextStageMusicName` | `MusicDataLib.Get(stage.musicId).GeQuName` |
| `TextBPM` | `TextStageBPM` | `MusicDataLib.Get(stage.musicId).GeQuBPM` |

当前显示格式为 `模式：名称`、`歌曲：名称`、`BPM 数值`。设置草稿不写入这里使用的权威模式/歌曲；完成设置后收到列表才同步更新。

| 按钮 | 显示条件 | 点击行为 |
| --- | --- | --- |
| `BtnSetting` | 不由 `RefreshJoinedActions` 控制 | 打开设置页，关闭主菜单 |
| `BtnJoin` | 本人不在当前查看的舞台 | 请求服务端自动分配可用座位 |
| `BtnStartGame` | 本人在当前查看的舞台 | 发起开局流程 |
| `BtnExit` | 始终显示 | 请求退出本人实际所在舞台 |
| `BtnJoinBlue` | 当前模式为双人或心动 | 选择蓝队，teamId=1 |
| `BtnJoinRed` | 当前模式为双人或心动 | 选择红队，teamId=2 |
| `BtnJoinGreen` | 当前模式为双人或心动 | 选择绿队，teamId=3 |

三色按钮在已经入座时也保留，可以作为同房间换队入口。是否允许操作仍由目标模式、阶段和服务端校验决定。

### 3.3 三类弹窗

| 界面 | 使用者 | 功能 |
| --- | --- | --- |
| `UI_KickPlayerTipView` | 发起踢人的玩家 | 显示对象与费用，确认后检查金币并发请求 |
| `UI_KickedTipView` | 被踢的本人 | 说明已被踢出及原因；确认只关闭提示 |
| `UI_PlayerLeaveStageTipView` | 收到离场通知的客户端 | 区分“已经离开房间”和“执行者将目标踢出房间” |

选曲界面 `UI_MusicSwitchView` 是另一种操作弹窗，由设置页打开，确认后把选择交回设置页。

## 4. 模式和音乐的草稿机制

### 4.1 三种状态需要分清

| 状态 | 保存位置 | 什么时候改变 |
| --- | --- | --- |
| 已生效模式、歌曲 | DS 的 `stage.info.mode/musicId`，以及客户端列表缓存 | 服务端接受配置并同步 |
| 房间设置草稿 | `RoomEnterView.pendingMode/pendingMusicId` | Toggle 选择或选曲确认 |
| 选曲弹窗当前高亮 | `MusicSwitchView.selectedMusicId` | 点击歌曲条目 |

`draftStageId` 表示草稿属于哪个已加入的舞台。`viewingStageId` 是当前展示的舞台，两者不能代替服务端成员身份。

### 4.2 切换模式

`SelectMode(mode)` 按以下顺序执行：

1. 确认本人属于当前查看的舞台，否则提示“请先加入房间”。
2. 确认配置中的模式开放，否则提示“当前模式暂未开放”。
3. 选择与已生效模式相同的模式时，把 `pendingMode` 清成 nil；否则保存新模式。
4. 回填 Toggle，并显示对应设置面板。
5. 根据缓存重新生成六个座位的展示数据。

回填 Toggle 时使用 `applyingToggles`，避免程序设置 `isOn` 再次触发选择逻辑。

**这一步不发 `CSStageSetConfig`。** 设置页立即切换的是面板预览，服务端模式及主界面摘要仍保持原值。

模式草稿不同于已生效模式时：

- 设置页把锁位显示为未锁；
- 暂停这些草稿面板上的空位加入和锁位操作；
- 踢其他人的入口会因 `canJoinRoom=false` 被拦住；
- 点击本人对应的离座入口仍可走退出；
- 加机器人按钮没有按模式草稿禁用，它仍操作服务端当前模式的房间。

### 4.3 选曲

打开弹窗后：

1. 首次通过 `MusicDataLib.GetSortedMusicData()` 构建列表。
2. 将 `UI_MusicSlotWidget` Prefab 实例化到 `TfContent`。
3. 用 `InitItem(music, OnMusicSelected, false)` 填充条目。
4. 选中优先级：设置页已保存的歌曲草稿 -> 当前房间歌曲 -> 配置中的第一首歌曲。
5. 点击条目只修改 `selectedMusicId` 并更新高亮。

确认时再次检查当前房间、可选的房主权限以及 `idle` 阶段，然后调用：

~~~lua
roomView.SetPendingMusic(selectedMusicId)
~~~

设置页验证歌曲 ID，保存 `pendingMusicId`，更新自己的 `TextMusicName`。随后选曲弹窗关闭，尚未发出服务端配置请求。

关闭或取消选曲弹窗不会应用本次高亮，也不会清除之前已经保存在设置页的音乐草稿。再次打开时重新读取草稿和当前房间。

### 4.4 音乐条目图片

`UI_MusicSlotWidget` 的绑定包括：

- `BtnMusicSlot`：条目点击入口。
- `ImgMusicSlot`：切换显示图片的 Image。
- `SpriteSelected`、`SpriteUnselected`：选中和未选中两张图片。
- `TextSlotNum`、`TextMusicName`、`TextBpm`：ID、歌曲名、BPM。

`SetSelected()` 设置 `ImgMusicSlot.sprite`，并把 Image 颜色重置成白色。它没有替换 Button 的整套 `spriteState`；需要 Inspector 把 `ImgMusicSlot` 指向预期的按钮图片。

### 4.5 取消设置究竟取消什么

`OnClose()` 清空模式和音乐草稿，然后：

~~~lua
UISys:CloseUI("UI_RoomEnterView")
UISys:OpenUI("UI_MainMenuView", UISystem.UILayers.layer4)
~~~

> [!important] 取消并非撤销整个房间操作记录
> 锁位、解锁、加机器人、入座、换座、退出、手动踢人都属于立即发请求的操作，关闭设置页不会撤销它们。
> 关闭设置页本身不调用 `StageSystem:Leave()`。

草稿还会在本人离开房间或当前所属舞台变化时被清空。仅由其他代码隐藏设置页时，`OnDisable` 只退订事件，不等同于执行 `OnClose`。

## 5. 完成设置的完整过程

### 5.1 客户端入口

`RoomEnterView.OnFinishSetting()`：

1. 确认本人仍在当前舞台。
2. 获取 `pendingMode`、`pendingMusicId`。
3. 两者都为 nil 时直接返回，不发包、不扣费、不提示成功。
4. 组装包含 `stageId` 和 `finishSetting=true` 的请求，只带需要提交的模式或音乐。
5. 如果模式实际变化，另外携带六个座位的 `locked=false`。
6. 调用 `StageSystem:SetConfig(config)`。
7. 该方法返回 true 后立即清空两个草稿。

示例：

~~~lua
{
    stageId = 1,          -- 舞台房间 ID
    mode = 3,             -- 双人玩法值；不是配置项 ID 2
    musicId = 2,
    finishSetting = true,
    locked = {
        { slotIndex = 1, locked = false },
        { slotIndex = 2, locked = false },
        { slotIndex = 3, locked = false },
        { slotIndex = 4, locked = false },
        { slotIndex = 5, locked = false },
        { slotIndex = 6, locked = false },
    },
}
~~~

`StageSystem:SetConfig` 确认本人在目标舞台，并用 `finishSettingPending` 阻止尚未收到结果时重复发送完成设置。完成设置请求不会乐观写入客户端列表里的模式和歌曲。

> [!warning] 当前清草稿时机
> 草稿是在“发出请求”后清空，并非“收到成功结果”后清空。金币不足或服务端拒绝后，用户需要重新选择；当前没有失败恢复草稿的机制。
> 等待标记也没有请求超时处理；如果结果始终没有到达，后续完成设置可能持续被本地拦截。

### 5.2 服务端校验和扣费

入口是 `ServerStageManager.HandleSetConfig(player, packet)`。真实操作者取自网络事件的 `player`，不是客户端传来的 openId。

处理顺序：

1. 找到目标舞台和操作者在 `occupancy` 中的实际座位。
2. 确认操作者就在目标舞台。
3. 确认房间处于 `idle`；否则回 `stage_busy`。
4. `finishSetting=true` 时，必须包含模式、音乐、难度、标题中的至少一项；否则回 `invalid_finish_setting`。
5. 按权限开关检查一般配置的房主权限。
6. 验证请求模式开放、歌曲 ID 存在。
7. 预校验锁位数据，并还原预校验期间的锁位变化。
8. 完成设置请求读取操作者服务端背包，检查已加载及金币数。
9. 余额足够时更新为 `currency - 100`。
10. 写入模式、音乐、难度、标题；真实模式变化时清空全部锁位。
11. 有效模式为双人或心动时，按条件执行性别人数上限整理，再规范队伍座位。
12. 刷新成员角色和站位元数据；广播自动踢出事件。
13. 向操作者同步背包余额，广播房间列表和本站详情。
14. 单独给操作者发 `msg="finish_setting_success"`，附 `finishSettingKickedCount`。

费用定义：

~~~lua
local FINISH_SETTING_COST = 100
-- TODO: 房间设置配置表补齐后，从配置表读取完成设置消耗。
~~~

完成设置使用服务端背包扣费。设置页没有用本地金币提前禁止点击完成设置。

### 5.3 一次提交的消息过程

~~~mermaid
sequenceDiagram
    participant U as 玩家
    participant V as RoomEnterView
    participant C as StageSystem
    participant S as ServerStageManager
    participant B as 服务端背包
    U->>V: 完成设置
    V->>C: SetConfig，finishSetting=true
    C->>S: CSStageSetConfig
    Note over V,C: 发包后清草稿，等待服务端结果
    S->>S: 校验成员、阶段、配置、锁位
    S->>B: 检查并扣除100金币
    alt 校验或金币检查失败
        S-->>C: 错误及当前房间快照
        C-->>U: 显示失败提示
    else 通过
        S->>S: 写配置，必要时解锁和自动踢人
        S-->>C: S2CRefreshCurrency
        S-->>C: 房间列表和本站详情
        S-->>C: finish_setting_success
        C-->>V: ListChanged，刷新已生效设置
        C-->>U: 成功或自动踢人提示
    end
~~~

### 5.4 提示与结果判断

`ResolveFinishSettingResult` 只在 `finishSettingPending=true` 时识别完成设置结果；带 `roomAction` 的加入/退出回包不作为设置结果。

| 结果 | 显示文本 |
| --- | --- |
| `finish_setting_success`，未自动踢人 | 完成设置成功 |
| `finish_setting_success`，自动踢出人数大于 0 | 系统已自动踢人，达到模式开始游戏要求。 |
| `stage_busy` | 游戏已开始，请稍后重试 |
| `no_currency` | 金币不足，完成设置失败 |
| 其他负状态结果 | 完成设置失败 |

“达到模式开始游戏要求”是当前提示原文。代码在这里处理的是性别人数上限，不保证队伍已完整或心动已满六人；真正能否开局见 [[#13. 开始游戏与音乐播放的衔接]]。

### 5.5 完成设置与一般配置请求的区别

| 请求 | 是否带 finishSetting | 是否收取 100 | 是否立即乐观更新客户端配置 |
| --- | --- | --- | --- |
| 设置页提交模式/音乐 | true | 是，服务端通过校验后 | 否 |
| 点击锁位/解锁 | 不带 | 否 | 是，随后用服务端快照修正 |
| 其他调用方直接提交一般配置 | 不带 | 当前处理器不扣这笔费用 | 可更新模式、音乐、标题、锁位 |

当前服务端只有在 `finishSetting=true` 时收取完成设置费。若未来要求“所有模式/音乐变更必扣费”，还需要明确并收紧一般配置入口；本文记录的是现状。

同一首当前歌曲经“选曲确认”仍可被写入 `pendingMusicId`，随后完成设置也会发包并扣费；代码未做歌曲未变化时的免提交判断。

## 6. 六个座位与三种设置面板

### 6.1 展示数据流

~~~text
SCStageListSync
  → StageSystem.OnSCStageListSync
  → StageSystem.Events.ListChanged
  → RoomEnterView.RefreshFromStage
  → ForEachSlotPanel
  → 各容器.RefreshRoomSlot(playerInfos)
  → UI_RoomSlot.Bind / SetOccupied / SetEmpty
~~~

`ForEachSlotPanel` 会刷新已绑定的冠军、双人、心动面板，并对同一脚本去重。非当前显示的面板也能接收数据，切换面板时便可显示最新占位。

实际容器源码为：

- 冠军通用容器：`UI_RoomSlotPanel.lua`。
- 双人容器：`UI_DoubleRoomSlotsWidget.lua`。
- 心动容器：`UI_HeartBeatRoomSlotsWidget.lua`。

冠军 Prefab 名为 `UI_ChampionRoomSlotsWidget`。Prefab 名称、查找字符串与源码文件名并非始终相同；当前脚本绑定通常经 `binding.script` 直接解析。

三个容器都保留 `lastPlayerInfos`，在 `Start()` 时重放最后一次数据，兼容父面板先刷新、子控件稍后启动的情况。

### 6.2 单座位展示数据

~~~lua
{
    stageId = 1,
    slotIndex = 3,
    mode = 3,                -- 设置页可传入预览中的模式
    openId = "player-open-id",
    name = "玩家名字",
    gender = 1,
    isRobot = false,
    isMine = false,
    teamId = 2,
    locked = false,
    canOperateRoom = true,
    canLockRoom = true,
    canJoinRoom = true,
    isHost = true,            -- 当前展示权限含义，见下方说明
}
~~~

| 字段 | 用途 |
| --- | --- |
| `openId` | 非空表示占用；空字符串表示空位 |
| `isMine` | 当前占位者是否本人 |
| `canOperateRoom` | 本人是否属于当前舞台 |
| `canLockRoom` | 有房间身份且没有未提交的模式切换 |
| `canJoinRoom` | 当前面板不是尚未提交的模式布局 |
| `locked` | 真实锁定状态，或模式预览期间的未锁展示 |
| `isHost` | 在此展示载荷中用于操作权限；开关关闭时会为 true，并不表示所有人都成了真实房主 |

空位在服务端列表中也有记录，不能只看槽位 table 是否存在。当前客户端兼容数值键、字符串键以及条目内 `slotIndex`。

### 6.3 两种座位控件

| 控件 | 页面 | 主要功能 |
| --- | --- | --- |
| `UI_RoomSlot` | 房间设置页 | 占位展示、空位加入、锁位/解锁、踢人弹窗 |
| `StageSlotWidget` | 主界面舞台信息区 | 占位展示、空位加入、本人头像离座、性别和底图 |

`UI_RoomSlot.SetOccupied` 填入完整身份；旧接口 `SetPlayerInfo(icon, name)` 只作兼容，openId 为空，不能代替完整身份数据。

`StageSlotWidget` 在双人模式按 1–2 蓝、3–4 红、5–6 绿显示底图。当前心动模式未复用双人的三色底图分支；不能从底图颜色推断心动模式是否已成功分队。


## 7. 加入舞台、选队与换座

### 7.1 三种加入方式

| 入口 | 客户端调用 | 服务端如何选座 |
| --- | --- | --- |
| 主界面加入舞台 | `Join(stageId, nil)` | 自动查找可用座位 |
| 红、蓝、绿队按钮 | `JoinTeam(stageId, teamId)` | 根据队伍和服务端性别算出座位 |
| 点击某个空位 | `Join(stageId, slotIndex)` | 验证指定座位是否合法、空闲、未锁 |

以上入口最终统一发送 `CSStageJoin`，没有三套独立的选队协议。

`StageInfoView.GetJoinableStage` 会先确认系统存在、舞台列表已就绪且房间为 `idle`。普通加入若发现本人已在当前舞台，会提示“您已经加入当前舞台”。

### 7.2 队伍和性别座位

真人性别由服务端读取玩家档案字段 `XingBie`：

- 1：男。
- 2：女。
- 其他或档案缺失：未知，`ResolveGender` 返回 0。

双人、心动模式共享以下入座约定：

| 队伍 | teamId | 男性座位 | 女性座位 | 颜色按钮 |
| --- | --- | --- | --- | --- |
| 蓝队 | 1 | 1 | 2 | `BtnJoinBlue` |
| 红队 | 2 | 3 | 4 | `BtnJoinRed` |
| 绿队 | 3 | 5 | 6 | `BtnJoinGreen` |

计算公式：

~~~lua
slotIndex = (teamId - 1) * 2 + gender
teamId = math.ceil(slotIndex / 2)
~~~

用户点击红队不代表能占红队任意空格。例如男性的红队目标是 3 号位；3 号位被占、4 号位空着时，仍不能加入红队。

未指定队伍或座位时，服务端从对应性别的 1/3/5 或 2/4/6 中寻找未锁空位。冠军模式则查普通未锁空位，不按性别限制座位。

### 7.3 服务端 Join 的主要校验

`ServerStageManager.Join` 依次检查：

1. 网络发送者和 openId 有效。
2. 目标舞台存在且空闲。
3. 目标模式在配置中开放。
4. 若本人已有舞台，原舞台也必须空闲才能直接换座/换台。
5. 指定 `slotIndex` 时，必须是 1–6 的整数。
6. 指定 `teamId` 时，必须是 1–3 的整数。
7. 双人/心动模式必须有合法服务端性别，指定座位必须符合性别和队伍。
8. 非组队模式拒绝携带 `teamId` 的选队请求。
9. 目标有空位、未锁定，且没有被其他成员占用。

客户端不能通过请求冒充机器人：该入口强制 `extras.isRobot=false`，也不接收客户端声明的真人性别作为最终依据。

### 7.4 已入座时的处理

| 场景 | 当前行为 |
| --- | --- |
| 已在该舞台，又普通加入且未指定座位/队伍 | 成功返回，保留原座位 |
| 请求的正是本人当前座位 | 更新必要姓名、性别、队伍信息，不新建成员 |
| 同一舞台换到另一合法空位 | 移动槽位和 occupancy，保留进入顺序、准备状态、积分等成员记录 |
| 换到另一个舞台 | 先验证目标，再清除旧占位，在新舞台创建成员记录 |
| 原舞台正在准备或对局 | 不允许用 Join 直接换台；先按允许的离场流程处理 |

新成员记录会生成 `joinedOrder`。同房换队不更新它，因此不能通过换座变成“刚进房的人”；重新退出再加入会得到新的进入顺序。

服务端成功后广播列表，单独给操作者发送带 `roomAction="join"` 的结果，再推送相关舞台详情。跨舞台时旧舞台详情也会刷新。

## 8. 退出舞台和离场清理

### 8.1 设置页关闭与退出舞台的区别

| 操作 | 是否发 CSStageLeave | 是否清除服务端占位 |
| --- | --- | --- |
| 设置页关闭/取消 | 否 | 否 |
| 主界面 `BtnExit` | 是 | 服务端接受后清除 |
| 主界面点击本人头像座位 | 是 | 服务端接受后清除 |
| 设置页点击本人对应的踢人入口 | 是，走普通离开 | 服务端接受后清除 |
| 踢出其他成员 | 发 `CSStageKick` | 服务端验证后调用 Leave |
| 平台玩家离开 DS | 服务端生命周期直接处理 | 清除该玩家舞台占位 |

设置页的 `OnSlotClick` 也有“本人则 Leave”分支，但已占用状态会隐藏空位加入按钮。实际是否可从这一按钮点击到本人分支取决于节点绑定；当前自己的踢人按钮另有明确的离座分支。

### 8.2 BtnExit 请求链

~~~text
StageInfoView.OnBtnExitClick
  → StageSystem:Leave()
  → 创建 CSStageLeave，data={}
  → ClientEventNetwork.FireServer
  → ServerEventNetwork.OnC2SEventHandle
  → NetPacketManager.Handle
  → ServerStageManager.HandleLeave
  → ServerStageManager.Leave(实际发送者 openId)
~~~

请求不需要指定待退出的 stageId，服务端通过 `occupancy[openId]` 查实际房间，避免客户端指定其他人的座位来退出。

客户端 `Leave()` 发送请求后直接返回 true，没有提前清空 `myStageId`、座位或舞蹈表现。因此这个返回值表示本地调用走到发包之后，不表示服务端已完成离场。

### 8.3 服务端实际删除的内容

`ClearOccupancy(openId)` 清除：

- `stage.slots` 中对应座位。
- `stage.players[openId]` 成员记录。
- 尚未结束的 `stage.danceMatch.players[openId]`，同时增加对局版本。
- `stage.teams` 的成员列表中的该 openId。
- 全房间索引 `ServerStageManager.occupancy[openId]`。
- 必要时转移仍保留的房主字段。

随后 `Leave`：

- 如果已没有真人，清除残留机器人 occupancy，并重建默认空舞台。
- 如果还有成员，空闲阶段刷新角色/站位元数据。
- 若正在倒计时且人数/队伍不再满足开局要求，取消准备，恢复 `idle`。

`HandleLeave` 成功后广播列表、推送旧舞台详情，并给本人发送 `roomAction="leave"` 的列表结果。若服务端找不到本人占位，返回 `not_on_stage`。

### 8.4 客户端收到退出结果后

`OnSCStageListSync` 在新列表中重新寻找本人：

1. 找不到本人则清空 `myStageId`、`mySlotIndex`。
2. 清理旧详情及准备倒计时。
3. 先发 `ListChanged` 刷新 UI 身份、座位、加入/开始按钮。
4. 根据离场信息显示普通离开或被踢提示。
5. 在离房或换房等条件下调用 `StopNetworkDance`。
6. 更新舞台镜头和机器人表现。

`StopNetworkDance` 会分别尝试清理碰撞、BGM、角色站位锚点、动画、飘字及联机舞蹈界面；某一项 Unity 表现清理报错时，仍继续其他清理。

`StageDanceClient.AcceptDanceState` 会拒绝不属于本人当前舞台的对局包，避免迟到的比赛快照把已退出玩家重新带进对局。

### 8.5 退出后的可见结果

`BtnExit` 按当前产品规则一直显示，退出不会让它消失，也没有“退出成功必须关闭 StageInfoView”的实现。

更可靠的成功判据：

- 服务端 occupancy 已没有本人。
- 客户端 `myStageId/mySlotIndex` 为空。
- 原座位清空。
- 开始按钮隐藏、加入按钮显示。
- 正在联机舞蹈时，对应表现清理完成。

另一个退出入口位于 `StageMainMenuView.BtnQuitClick`。它经 `GameManager:ExitDanceMode()`，联机模式下再调用 `StageSystem:Leave()`。完成一局的 `BtnEndDanceClick` 则走 `FinishDance`；结束一局和离开舞台是不同操作。

## 9. 锁位与解锁

### 9.1 模式规则

| 模式 | 可以锁什么 | 失败条件 |
| --- | --- | --- |
| 冠军 | 一个空座位 | 目标座位已有人 |
| 双人 | 一整队两个空座位 | 该队任意一格已有人 |
| 心动 | 不显示锁/解锁按钮，不允许锁定 | 提交任何 true 锁位都被服务端拒绝 |
| 斗舞 | 当前未开放；通用代码有非组队单格处理 | 不作为已开放 UI 功能使用 |

双人模式按 1–2、3–4、5–6 成对操作。点击 3 号位锁定，服务端最终同时锁定 3、4；点击其中一格解锁也会作用于整队。

双人队内有人时，当前提示为：

> 同队伍中空位已经有人，锁定失败。

### 9.2 客户端与服务端检查

客户端 `UI_RoomSlot` 先确认：

- 本人在目标房间。
- 当前没有待提交的模式切换。
- 点击的是空位。
- 模式允许锁位。
- 双人队内没有任何占用者。

随后先更新锁位 UI，再调用 `SetSlotLocked`。它根据**已生效模式**生成一格或一对座位的 `locked` 请求，复用 `SetConfig`，不带 `finishSetting`。

服务端 `ApplyModeLockedFlags` 重新验证模式、座位及双人配对数据。不允许同一队两格提交相互矛盾的锁状态；失败返回权威列表以修正客户端预览。

支持的锁位数据形式：

~~~lua
-- 条目数组
locked = {
    { slotIndex = 1, locked = true },
    { slotIndex = 2, locked = true },
}

-- 座位索引表；也兼容字符串键
locked = {
    [1] = true,
    [2] = true,
}
~~~

当前布尔解析接受 `true`、`1`、`"1"`、`"true"` 为锁定。

### 9.3 切换模式时清锁的时机

- 选择 Toggle：设置页预览为全未锁，不立即修改服务端。
- 完成设置且服务端接受真实模式变化：`stage.info.locked = CreateLockedFlags()`。
- 取消草稿：仍显示原模式、原锁位。
- 只换歌曲或重复提交相同模式：不触发“模式变化清全部锁”。

纯锁位请求要求同房间与空闲阶段。目前它不经过一般配置的房主权限分支；如果将来启用房主开关，不能假设纯锁位也已自动变为房主专属。

## 10. 手动踢人与金币检查

### 10.1 打开确认弹窗

`UI_RoomSlot.OnKickClick`：

1. 确认有占位者，且本人可以操作当前房间。
2. 如果绑定了外部 `kickCallback`，优先调用外部回调并返回。
3. 若目标是自己，直接 `Leave()`，不走付费踢人。
4. 未提交模式切换期间，拦截对他人的踢出入口。
5. 打开 `UI_KickPlayerTipView`，调用 `SetKickTarget(stageId, slotIndex, openId, playerName, isRobot)`。

**入口没有金币检查。** 金币不足也能打开弹窗。`SetKickTarget` 明确设置 `BtnConfirm.interactable=true`。

当前确认文案保留了原字符串，包括两个乘号：

~~~text
是否花费金币×<color=#FFD700>×%s</color>，将{<color=#FFA500>%s</color>}踢出房间！
~~~

这是 Unity 富文本，文档中放在代码块里显示原样。

### 10.2 点击确认后的客户端检查

`KickPlayerTipView.OnBtnConfirmClick` 重新获取费用：

- 目标在弹窗载荷中标记为机器人：费用 0，不检查本地金币。
- 真人：按当前舞台模式读 `GetKickCostByMode`。
- 费用不可用：提示“踢人配置未加载”，保留弹窗。
- 本地背包已知余额且不足：提示“金币不足”，保留弹窗，确认按钮仍可点。
- 本地余额尚未加载：不把未知余额当成 0，继续交服务端判断。

通过后调用 `StageSystem:Kick`，然后清除弹窗目标并关闭弹窗；目前不会等服务端成功才关闭。因此服务端拒绝时，错误提示可能发生在弹窗已经关闭之后。

头像和边框设置函数 `SetAvatarImage`、`SetBorderImage` 目前仍是 TODO。

### 10.3 服务端目标校验

`ValidateKickTarget` 会确认：

- 目标舞台存在。
- 发起者确实属于同一舞台。
- 舞台为 `idle`。
- 权限开关启用时，发起者是房主。
- 目标 openId 和座位存在于该舞台。
- 请求携带座位时，目标当前座位仍与请求一致。

最后一项可以防止“弹窗打开后，该人已换座”仍按旧座位误操作其他成员。

### 10.4 服务端费用与撤销

`HandleKick` 从 `stage.players[targetOpenId].isRobot` 判断目标是否机器人，**不信任客户端传来的免费标记**。

| 目标 | 服务端动作 |
| --- | --- |
| 机器人 | 不读取或扣除操作者金币，直接走目标移除 |
| 真人 | 必须读取已加载的服务端背包，按模式配置检查金币并扣费 |

真人费用即使当前配置为 0，仍会执行服务端背包已加载等检查。踢机器人不受这一步影响。

费用通过后调用 `KickFromSlot`，再次验证目标并经 `Leave` 移除。移除失败会把本次已扣金币恢复成此前数值。

成功后：

1. 若涉及背包，发送 `S2CRefreshCurrency`。
2. 广播带 `leaveEvent = { reason="kicked", openId=..., kickerName=... }` 的列表；手动踢人会附带执行者姓名。
3. 推送剩余在座成员详情。
4. 被踢真人在线时，再给其补一份列表。

### 10.5 被踢者与其他客户端的提示

本人匹配 `leaveEvent.openId` 时打开 `UI_KickedTipView`：

| 文本 | 当前内容 |
| --- | --- |
| 标题 | 您已被踢出房间 |
| 手动踢出原因 | 您已被房间成员移出房间。 |
| 系统整理原因 | 因双人模式人数限制，系统已将您移出房间。／因心动模式人数限制，系统已将您移出房间。 |

`BtnConfirm` 只关闭提示，不再发送一次 Leave。

其他客户端通过 `UI_PlayerLeaveStageTipView.ShowPlayerName(name, wasKicked, kickerName, automatic)` 显示：

- 普通离开：`名字已经离开房间！`
- 手动踢人：`[执行者]已成功将{目标}踢出房间。`
- 系统自动移除：`目标被踢出房间！`

该提示显示 3 秒，再用 0.5 秒淡出，使用不受 TimeScale 影响的时间。重复显示会重置计时。

## 11. 模式人数整理与自动踢人

### 11.1 生效范围

完成设置的有效模式为双人或心动，并满足“完成设置”或“模式实际发生变化”时，服务端执行 `EnforceGenderLimitForMode`。

这里的有效模式是本次提交模式，或未提交模式时的房间原模式。因此在双人/心动房间中只提交音乐，也会在完成设置分支检查人数上限。

规则明确为：

~~~text
男性人数 <= 3
女性人数 <= 3
~~~

即 4 男不允许，4 女不允许。2 男 3 女通过这项检查，但不代表现在就可以按“开始游戏”。

### 11.2 移除谁

`CountStageGenders` 统计 `stage.players` 中 gender=1/2 的成员。机器人也包含在成员表里，不做排除；未知性别不计入男/女人数。

发现某性别超额后：

1. 从六个座位中收集该性别成员。
2. 按 `joinedOrder` **降序**排列，最晚加入的排前面。
3. 进入顺序相同则座位号较大的排前面。
4. 移除第一个，再重新统计，直到满足上限。

例子：

~~~text
男1 → 男2 → 男3 → 男4 依次加入
切换双人或心动并完成设置
→ 先踢男4
→ 留下男1、男2、男3
~~~

当前算法不豁免操作者。若发起完成设置的人正好是超额性别中最晚加入者，也可能被系统移出。

### 11.3 自动踢人的费用

自动整理通过 `ServerStageManager.Leave` 移除超额成员，不经过手动 `HandleKick` 扣费。因此不按每个人另收手动踢人费用，只处理本次完成设置本身的 100 金币。

### 11.4 整理后的座位

`NormalizeTeamSlots`：

1. 尽量保留已在性别匹配座位上的成员。
2. 把男玩家放到空闲奇数位，把女玩家放到空闲偶数位。
3. 未知性别成员再填剩余空位。
4. 重建 `stage.slots`，更新每人的 `teamId` 和全局 occupancy。

该过程优先保留合法原位，**不负责把每个残缺队伍自动凑成完整队伍**。因此人数上限通过后，双人模式仍可能需要用户换队才能开局。

当自动移除导致最后一名真人离场时，`Leave` 会重置空舞台并清除机器人；处理器随后会重新取得舞台。重置后的房间可能回到冠军、音乐 1 的默认设置。

### 11.5 自动踢人消息

服务端为每个自动移出的 openId 广播：

~~~lua
leaveEvent = {
    reason = "kicked",
    openId = "目标openId",
    automatic = true,
    mode = 3, -- 或心动模式1
}
~~~

本人根据这条明确事件显示系统移出的原因。完成设置操作者另外收到 `finishSettingKickedCount`，用于选择成功提示文案。

## 12. 机器人管理

### 12.1 添加入口及限制

`AddRobotBtn` 的可交互条件包括：

- 已存在舞台快照，本人在此舞台。
- 房间空闲。
- 至少有一个未锁空位。
- 权限开关启用时，本人满足房主要求。

点击后立即发送 `CSStageAddRobot`，不等待完成设置，也不在 View 中直接创建机器人数据。

服务端 `AddRobot` 重做身份、阶段、权限和空位检查。机器人 ID 为 DS 生命周期内递增的 `robotN`，还会检查与已有 occupancy、在线玩家的冲突。

### 12.2 机器人记录

| 属性 | 当前行为 |
| --- | --- |
| `isRobot` | true |
| `ready` | 自动 true |
| 名字 | 使用 robotN |
| 队伍模式性别 | 根据目标槽位奇偶决定 |
| 非队伍模式性别 | 按已有男女数量倾向补较少的一方 |
| teamId | 队伍模式为座位对编号 |
| 真人存档/平台连接 | 不为机器人创建 |
| 进入顺序 | 同样生成 joinedOrder |
| 手动踢出费用 | 0 |
| 真人全部离开后 | 从舞台和 occupancy 清除 |

### 12.3 机器人表现

`StageRobotClient.SyncStageRobots` 根据本人当前舞台列表或对局成员：

- 删除已经离场的机器人模型。
- 创建缺失模型，性别变化时重建。
- 大厅中就近展示。
- 准备/对局阶段按 `standPk/startLocation` 更新位置。
- 资源未就绪时在后续调用中重试。

真实成员、占位和得分由 DS 处理；客户端机器人模型不是成员身份来源。房间快照已经删除机器人但模型残留时，应检查表现回收链路。

## 13. 开始游戏与音乐播放的衔接

### 13.1 完成设置与开局是两步

| 模式 | 完成设置中的性别上限 | 当前服务端开局条件 |
| --- | --- | --- |
| 冠军 | 不走双人/心动人数整理 | 1–6 人 |
| 双人 | 男最多 3、女最多 3 | 至少一队两格全满；每个其他队伍必须全空或全满 |
| 心动 | 男最多 3、女最多 3 | 六格全部占满 |
| 斗舞 | 当前未开放 | 代码保留 6 人的开局人数判断 |

双人模式示例：

| 占位情况 | 能否开始 |
| --- | --- |
| 蓝队2人，其他全空 | 可以 |
| 蓝队2人，红队2人，绿队全空 | 可以 |
| 三队全满 | 可以 |
| 蓝队2人，红队1人 | 不可以 |
| 蓝队1人，红队1人 | 不可以，即使总人数是2 |
| 全空 | 不可以 |

客户端 `StartRequirementError` 做双人和心动的预检查，服务端 `CanStart(mode, stage)` 根据实时座位再检查。当前服务端不是单看总人数为 2/4/6 就允许双人开始。

### 13.2 开局链

~~~text
BtnStartGame
  → StageSystem:Start()
  → 校验本人及本地队伍条件
  → 本地5秒准备倒计时 / 请求校时
  → 获取默认BGM时长
  → CSStageStart
  → ServerStageManager.HandleStart
  → 确认真实成员、idle、模式开局条件
  → BeginStartCountdown
  → ServerStageDance.Tick 到期
  → CompleteStartCountdown
  → BuildMatchSnapshot 再校验
  → ServerStageDance.Begin
~~~

当前服务端允许在座成员发起开始，不检查所有人 `ready=true`，也不在 `HandleStart` 中按房主开关限制开始。

重复开始请求若房间已在 `countdown`，服务端只重发状态，不重新计时。倒计时期间离场使条件不再满足时，回到 `idle`。

### 13.3 阶段与可操作性

| 操作 | idle | countdown / 对局中 |
| --- | --- | --- |
| 加入、选队、换座 | 按座位规则允许 | 服务端拒绝 |
| 模式/音乐/锁位配置 | 按权限、参数允许 | 服务端拒绝 |
| 加机器人 | 允许 | 服务端拒绝 |
| 手动踢人 | 允许 | 服务端拒绝 |
| 本人退出 | 允许 | Leave 没有 idle 限制，允许清理 |
| 已在 countdown 再点开始 | 不适用 | 重发状态，不重置计时 |

客户端某按钮可点只代表允许尝试，不替代 DS 阶段判断。例如模式 Toggle 的禁用条件没有完整包含游戏阶段，玩家可能先做了预览，到完成设置时才收到“游戏已开始”。

### 13.4 当前 musicId 与真正播放的 BGM

当前选曲链负责：

~~~text
MusicDataLib.ID
  → 设置页 pendingMusicId
  → stage.info.musicId
  → 房间列表 musicId
  → 主界面歌曲名和BPM
~~~

当前开局播放链则是：

~~~text
StageDanceRules.DefaultBgmKey（airen）
  → StageSystem:Start() 读取BGM时长
  → CSStageStart.bgmKey / bgmDuration
  → stage.pendingBgmKey
  → 对局快照
  → StageDanceClient.SyncDanceBgm()
~~~

两条链还没有通过 `MusicDataLib.GeQuPath` 连起来。配置中的 BPM 目前是这些房间界面的显示信息，不能据此认定正式节奏计算或音频播放已跟随所选歌曲变化。

### 13.5 准备态表现

服务端开始倒计时时分配开场角色和站位。空闲阶段 `RefreshOccupancyStands` 主要刷新角色/队伍元数据并清理正式站位坐标；客户端空闲状态主要绑定舞台中心镜头。

UI 座位号、队伍编号、角色实际世界坐标分别有不同用途。主界面看到座位已入房，不代表角色一定立即移动到正式对局站位。

## 14. 网络协议与数据结构

### 14.1 协议注册与分发

协议类型和数据包类位于 `Scripts/Common/NetworkPacket`，通过共享 index 加载。

~~~text
客户端
NetPacketManager.CreatePacket
  → BaseNetPacket.Serialize
  → ClientEventNetwork.FireServer
  → DouyinRemoteEvent("C2S")

服务端
ServerEventNetwork.OnC2SEventHandle(player, ...)
  → CreatePacket / Deserialize
  → NetPacketManager.Handle(type, player, packet)
  → ServerPacketRegister 已注册的处理器

回包
ServerEventNetwork.SendToPlayer / BroadcastAll
  → DouyinRemoteEvent("S2C")
  → ClientEventNetwork.OnS2CEventHandle
  → ClientPacketRegister
  → StageSystem 对应入口
~~~

服务端 `GameServerModule.Start` 负责初始化网络及调用 `ServerPacketRegister.RegisterAll`。客户端 `PlayerSystemRegister.Awake` 初始化网络并创建、注册 `StageSystem`。

`ClientPacketRegister` 向业务入口传的是 **`packet.data`**，不是整个 BaseNetPacket 对象。

### 14.2 C2S 操作清单

| 协议 | data 中主要字段 | 服务端入口 |
| --- | --- | --- |
| `CSStageRequest` | 空表 | `HandleRequest` |
| `CSStageJoin` | stageId，slotIndex可选，teamId可选 | `HandleJoin` |
| `CSStageLeave` | 空表；身份取发送者 | `HandleLeave` |
| `CSStageSetConfig` | stageId、mode、musicId、difficulty、title、locked、finishSetting | `HandleSetConfig` |
| `CSStageKick` | stageId、slotIndex、openId | `HandleKick` |
| `CSStageAddRobot` | stageId | `HandleAddRobot` |
| `CSStageReady` | ready | `HandleReady` |
| `CSStageStart` | bgmKey、bgmDuration、introSeconds | `HandleStart` |
| `CSStageDance` | 对局 action，如 clock / beat / finish | `ServerStageDance.Handle` |
| `CSGMAddCurrency` | amount | `ServerGMManager.HandleGMAddCurrency` |

通用配置支持 `difficulty/title`，但当前设置页没有相应编辑控件。不要把协议支持的字段全部当作已完成的 UI 功能。

### 14.3 S2C 清单

| 协议 | 接收内容 | 分发/用途 |
| --- | --- | --- |
| `SCStageListSync` | 全房舞台摘要、六槽、revision，可带 roomAction/leaveEvent/设置结果 | 更新成员身份与主要 UI |
| `SCStageDetailSync` | 本站 info、players、teams、slots、timeline、danceMatch、revision | 本站详情和对局衔接 |
| `SCStageDance` | 对局状态、时钟、节奏结果 | `StageDanceClient` |
| `S2CRefreshCurrency` | 最新 bagData | 客户端背包镜像刷新 |
| `SCGMAddCurrency` | 测试加钱结果和 bagData | 客户端背包镜像刷新 |

失败并不都有独立协议。很多加入、退出、设置、锁位、踢人失败通过 `SCStageListSync` 携带负 `code` 返回；部分阶段/权限失败使用 `SCStageDetailSync`。

### 14.4 BaseNetPacket 与业务载荷

网络外壳示例：

~~~lua
{
    version = 1.0,
    type = "SCStageListSync",
    data = {
        code = 0,
        msg = "",
        data = {
            revision = 42,
            roomAction = "join",
            stages = { -- 舞台摘要数组
                -- ...
            },
        },
    },
}
~~~

业务方法 `StageSystem:OnSCStageListSync(payload)` 收到的是里面的：

~~~lua
{
    code = 0,
    msg = "",
    data = { revision = 42, stages = { --[[ ... ]] } },
}
~~~

因此业务入口中的 `payload.data.stages` 才是列表；把包外壳和业务载荷层级混淆会导致刷新入口提前返回。

### 14.5 服务端舞台内存结构

示意省略非房间操作核心字段：

~~~lua
ServerStageManager.stages[1] = {
    info = {
        stageId = 1,
        title = "",
        mode = 4,
        musicId = 1,
        difficulty = 1,
        phase = "idle",
        hostOpenId = "",
        locked = { false, false, false, false, false, false },
    },
    slots = {
        [1] = { openId = "player-a" },
        -- 空座位在服务端内存中为nil
    },
    players = {
        ["player-a"] = {
            openId = "player-a",
            joinedOrder = 10,
            gender = 1,
            isRobot = false,
            isHost = true,
            teamId = 0,
            ready = false,
            score = 0,
            role = "",
            standPk = "",
            startLocation = { x = 0, y = 0, z = 0 },
            -- 还有playerID、name、coin、judges等字段
        },
    },
    teams = {},
    timeline = nil,
    round = { index = 0 },
}

ServerStageManager.occupancy["player-a"] = {
    stageId = 1,
    slotIndex = 1,
}
~~~

三个索引必须一致：`slots` 表示座位是谁、`players` 保存成员数据、`occupancy` 从 openId 反查所在舞台与座位。

不要只清客户端 UI，也不要只改服务端其中一张表。

### 14.6 列表与详情差异

列表中的单个舞台包含：

`stageId/title/mode/phase/musicId/playerCount/slotCount/hostOpenId/countdownEndsAt/countdownRemain/slots`。

列表的每个座位固定包含：

`slotIndex/openId/name/gender/ready/isRobot/locked/role/standPk/startLocation`。

服务端内存的空槽为 nil，而**列表会生成固定六条槽位记录，空位 openId 为 ""**。这是占用判断应检查 openId 的原因。

详情包含：

`info/slotCount/slots/players/teams/timeline/danceMatch/round/revision`。

详情的 `players` 还包含分数、评级统计、队伍等信息。列表并没有直接为每个座位发送 `teamId`，常见 UI 通过座位对编号推导队伍；完整成员记录可从详情读取。

## 15. 客户端同步、版本与生命周期

### 15.1 客户端主要缓存

| 字段 | 含义 |
| --- | --- |
| `stages` | 全房舞台列表 |
| `detail` | 本人当前舞台详情 |
| `myOpenId` | 本地玩家身份缓存 |
| `myStageId`、`mySlotIndex` | 从列表重新定位的本人占位 |
| `listRevision`、`detailRevision` | 已接受快照版本 |
| `finishSettingPending` | 正在等待完成设置结果 |
| `localCountdownEnd`、`countdownDisplay` | 本地倒计时显示数据 |
| `danceMatch` | 已接受的联机对局状态 |
| `robotVisualIds` | 已创建机器人表现的跟踪集合 |

这些客户端缓存不持久化房间，也不取代服务端 occupancy。

### 15.2 接收列表的顺序

`OnSCStageListSync`：

1. 检查载荷类型、列表结构和 revision。
2. 解析设置结果、普通操作错误。
3. 比较前后占位，准备离场提示信息。
4. 替换 `stages`，执行 `RefreshMySeat`。
5. 身份变化或已无房间时清理详情和倒计时。
6. 发送 `ListChanged`。
7. 处理被踢弹窗或离场提示。
8. 必要时停止旧局，更新镜头、倒计时和机器人。

`RefreshMySeat` 遍历所有舞台所有座位，以 openId 匹配本人；找不到就清空本人房间身份。它不从“当前 UI 正在展示哪个舞台”推断自己已入房。

### 15.3 版本规则

`NextSnapshotRevision()` 是 DS 内的递增计数，列表和详情构建都使用它。

- 列表 revision 小于已接受 `listRevision` 时丢弃。
- 相同 revision 的列表不会仅因相等而丢弃。
- 详情版本若旧于列表或已接受详情则丢弃。
- 详情还必须属于本人当前已确认舞台，否则直接返回。
- 详情不会重新建立本人占位。
- 对局另外有 matchId/version 等检查。

当前没有 DS 会话标识参与版本比较。若服务端重建后 revision 从头开始，而客户端保留旧版本，需要联机检查重连和系统重建是否能正确重置缓存；不能仅凭递增比较就保证跨 DS 重启恢复。

### 15.4 本地事件

| 事件 | 主要作用 |
| --- | --- |
| `StageSystem.Events.ListChanged` | 设置页、主舞台信息区刷新 |
| `DetailChanged` | 本站详情变化 |
| `CountdownChanged` | 准备倒计时 UI |
| `DanceChanged` | 联机舞蹈表现和结束通知 |

这些是客户端 `EvtMsgSystem` 内的事件，不是网络协议。

### 15.5 生命周期与资源复用

| 脚本 | 初始化/显示 | 隐藏/销毁 |
| --- | --- | --- |
| `PlayerSystemRegister` | Awake 创建 StageSystem；本人进入、重连、Actor生成时请求快照 | 销毁时删除系统和缓存 |
| `RoomEnterView` | Awake尝试订阅；Start绑定按钮；OnEnable缓存刷新并请求列表 | OnDisable退订；OnDestroy清理按钮与Toggle监听 |
| `StageInfoView` | OnEnable和Start补齐绑定、座位、事件；显示时请求列表 | 当前在OnDestroy退订并移除监听 |
| 三种设置座位容器 | RefreshRoomSlot保存最后数据；Start重放 | 随父UI生命周期 |
| `MusicSwitchView` | Start构建条目；再次OnEnable刷新选择 | 缓存复用，OnDestroy清理监听和记录 |
| `UI_MusicSlotWidget` | InitItem填数据；Start绑定点击 | OnDestroy解除点击 |
| `UISystem` | 首次CreateUI，后续OpenUI复用缓存 | CloseUI只SetActive(false)，不销毁 |

`StageInfoView` 没有对应的 OnDisable 退订逻辑，因此隐藏时仍可能接收列表刷新；再次显示通过先移除再添加回调避免按钮监听重复。

平台离房走服务端 `OnPlayerLeft` 删除占位；重连会补发列表。是否保留重连前舞台占位，取决于平台在断开时是否已触发离房清理，不能只看客户端重新请求快照这一动作。


## 16. 弹窗层级、Prefab 和绑定

### 16.1 当前层级定义

`UISystem.UILayers` 存的是 Canvas 的 `sortingOrder`，不是 Unity GameObject 的 Layer 编号：

| 名称 | sortingOrder |
| --- | --- |
| layer1 | 0 |
| layer2 | 50 |
| layer3 | 100 |
| layer4 | 150 |
| layer5 | 200 |
| layer6 | 250 |

所以要求 layer6 时应传 `UISystem.UILayers.layer6`，其值是 250；直接传数字 6 不代表第六层。

当前代码的实际调用：

| 界面 | 打开处 | 传入层级 |
| --- | --- | --- |
| `UI_MainMenuView` | 设置页关闭、GameManager返回主菜单 | layer4 |
| `UI_RoomEnterView` | StageInfoView设置按钮 | 未显式传层级 |
| `UI_MusicSwitchView` | RoomEnterView.OnMusicSwitcher | **layer5** |
| `UI_KickPlayerTipView` | UI_RoomSlot.OnKickClick | **layer5** |
| `UI_KickedTipView` | StageSystem.ShowKickedTip | **layer6** |
| `UI_PlayerLeaveStageTipView` | StageSystem.ShowPlayerLeaveTip | 未显式传层级 |

当前 `UISystem:OpenUI` 没有按界面 key 强制把前两种操作弹窗改成 layer6。调用方显式给 layer5 时，根 Canvas 若存在就被设置为 200。

不传层级时保留 Prefab 或缓存实例当前的 sortingOrder。若根对象没有 Canvas，这个函数也不会帮子 Canvas 设置层级。

### 16.2 界面注册

相关 UI key 已在 `Prefabs/Client.prefab` 的 UI 注册表中出现：

`UI_StageInfoView`、`UI_RoomEnterView`、`UI_MusicSwitchView`、`UI_KickedTipView`、`UI_KickPlayerTipView`、`UI_PlayerLeaveStageTipView`。

`UISystem:GetUI(key)` 在对象尚未缓存时会调用 `CreateUI`；它不是保证只读的查询。当前选曲弹窗通过它取得设置页，再解析 `RoomEnterView` 脚本。

### 16.3 需要维护的 Prefab

| Prefab | 需要核对的绑定 |
| --- | --- |
| `UI_RoomEnterView` | 三Toggle、三个模式面板、座位脚本、音乐标题、关闭/取消/完成/加机器人/选曲按钮 |
| `UI_ChampionRoomSlotsWidget` | 六个 UI_RoomSlot 脚本 |
| `UI_DoubleRoomSlotsWidget` | 六个 UI_RoomSlot，顺序对应队伍两格 |
| `UI_HeartBeatRoomSlotsWidget` | 六个 UI_RoomSlot |
| `UI_RoomSlotWidget` | 锁、解锁、踢人、姓名、头像、锁提示及加入按钮子节点 |
| `UI_StageInfoView` | 三色队伍按钮、加入/退出/开始/设置、三项摘要、六个座位和倒计时 |
| `UI_StageSlotWidget` | 空位按钮、头像Button、姓名、性别、锁图标、冠军/队伍底图 |
| `UI_MusicSwitchView` | 条目Prefab、TfContent、确认/取消/关闭 |
| `UI_MusicSlotWidget` | 条目按钮、Image、两张Sprite、ID/歌名/BPM |
| `UI_KickPlayerTipView` | 正文、确认/取消；头像与边框功能仍待实现 |
| `UI_KickedTipView` | 标题、原因、确认 |
| `UI_PlayerLeaveStageTipView` | 正文、用于淡出的CanvasGroup |
| `UI_MainMenuView` | 内嵌舞台信息实例及可能的Prefab覆盖值 |

当前 `StageInfoView` 的退出和三个颜色按钮在 Prefab 中均有 Button 引用，源码也有对应 AddListener。这个静态事实不能排除运行时实例被遮挡、引用覆盖或生命周期执行失败。

几个绑定细节：

- 当前 `BtnJoinTeam` 绑定与普通 `BtnJoin` 指向同一个 Button。`GetTeamJoinRoot` 有显式判断，遇到这个情况会退回从颜色按钮查父节点，而不是把普通加入按钮当队伍容器。
- 队伍父节点 `TeamJoinTeam` 初始不激活，由模式刷新控制。
- `UI_RoomSlot` 声明了 `BtnRoomSlot`，但实际加入按钮通过根节点下名为 `BtnRoomSlot` 的子节点查找并缓存；仅修改 Inspector 字段不一定改变这条查找路径。
- `StageSlotWidget` 的本人退出入口还会从 `AvatorImg.gameObject` 取得 Button。只有 Image、没有 Button 时，不会有该头像点击监听。
- `SetEmpty/SetOccupied` 的 `visualApplied` 标记防止子脚本 Start 把早到的占位刷新覆盖为空位。

## 17. 提示文案与错误处理

### 17.1 常见服务端原因

状态码只大致区分成功/失败，某些负数在不同入口含义不同，例如 `mode_closed` 在 Join 与 SetConfig 中的 code 不一致。排查时应同时看 **协议、code、msg**，不要只查数字。

| msg | 当前通常显示的提示/含义 |
| --- | --- |
| `not_on_stage` | 请先加入舞台；退出操作回包专用提示为“您当前不在房间中” |
| `stage_not_found` | 房间不存在，请刷新后重试 |
| `stage_busy` | 舞台正在准备或游戏中；完成设置等待期间会显示“游戏已开始，请稍后重试” |
| `mode_closed` | 当前模式暂未开放 |
| `stage_full` | 没有可用空位（舞台已满或空位已锁定） |
| `invalid_gender` | 请先完成性别设置，再加入房间 |
| `bad_team` | 队伍无效，请重新选择 |
| `team_not_supported` | 当前模式不支持选队，请使用加入舞台 |
| `slot_gender_mismatch` | 该位置与您的性别不符，请选择同队对应位置 |
| `slot_occupied` | 该位置已有人，请选择其他队伍或位置 |
| `slot_locked` | 该位置已锁定 |
| `bad_slot` | 座位无效，请重新选择 |
| `team_has_player` | 同队伍中空位已经有人，锁定失败。 |
| `lock_not_allowed` | 当前模式不允许锁定 |
| `invalid_lock_pair` | 队伍锁位数据无效 |
| `invalid_music` | 所选音乐不存在 |
| `kick_config_missing` | 踢人配置未加载 |
| `no_currency` | 金币不足；完成设置时为“金币不足，完成设置失败” |
| `not_host` | 此操作仅限房主 |
| `people_count_invalid` | 当前人数不符合所选舞蹈模式 |
| `duo_teams_incomplete` | 双人模式至少需要一队满员，且不能有未满员的队伍 |
| `heart_teams_incomplete` | 心动模式需要三队全满（6人）才能开始 |

另外还可能返回 `player_data_not_ready`、`invalid_finish_setting`、`gender_limit_unsatisfied`、`invalid_slot`、`slot_empty`、`no_target`、`no_player`、`invalid_open_id` 等原因。它们并非都有单独的中文映射，普通错误会回退为：

~~~text
舞台操作失败：原始msg
~~~

完成设置等待期间的其他错误可能被统一显示成“完成设置失败”，所以排查时仍应保留原始回包内容。

### 17.2 金币与档案更新

- 踢真人与完成设置都从 `ServerPlayerDataManager.Get(openId).bagData` 读取余额。
- 检查 `IsLoaded()`，用 `Get("currency")` 获取余额。
- 通过 `Update("currency", 新值)` 更新玩家数据域；持久化由既有玩家数据系统负责。
- 通过 `S2CRefreshCurrency` 将 `bagData:Get()` 返回客户端。
- `ClientPacketRegister` 取 `ClientPlayerData.bagData`，调用 `ApplyServerData` 更新镜像。
- 真人加入的性别读取服务端档案 `XingBie`；其设置入口由 `ServerNewbieGuideManager.HandleSetPlayerGender` 处理。

只改客户端显示金币或本地性别，不会改变服务端扣费与队伍分配的依据。

### 17.3 测试加钱热键

`TestSystemRegister.lua` 当前定义：

~~~text
键盘主数字区7（Alpha7） → 服务端增加100000金币
~~~

路径：

~~~text
AddTestCurrency
  → CSGMAddCurrency { amount = 100000 }
  → ServerGMManager.HandleGMAddCurrency
  → 服务端背包更新
  → SCGMAddCurrency携带bagData
  → 客户端背包镜像更新
~~~

这个按钮入口没有加房间身份或金币条件；仍走既有 GM 服务端处理器。处理器本身会校验金额正数、上限和玩家数据是否加载。

同脚本里的 8、9 键是测试道具的添加和消耗，与完成设置费用无关。脚本已有“发布前移除测试脚本与协议”的注释；后续清理测试入口时一并核对 GM 注册链。

## 18. 当前边界、差异与待确认项

以下内容是阅读代码得出的现状或风险，不表示本次整理文档已修改这些实现。

| 类型 | 当前事实 | 对使用/维护的影响 |
| --- | --- | --- |
| 与此前层级要求不同 | 选曲与踢人确认当前传layer5 | 需要layer6时应改具体调用或统一策略；当前没有强制覆盖 |
| 配置已变化 | 当前各模式踢人费为0 | 金币不足踢人场景不能再按10000费用预期验证 |
| 待配置化 | 完成设置费用仍为100硬编码 | 配置表补字段后需要替换服务端费用来源 |
| 功能衔接未完成 | 选曲musicId未连接正式BGM，GeQuPath为空 | 歌名/BPM变化不等于实际播放曲目变化 |
| 草稿处理 | 发出完成设置后立即清草稿 | 服务端失败后没有恢复选择 |
| 请求等待 | finishSettingPending没有超时或请求ID | 丢回包可能持续等待；非roomAction的其他失败还可能被当成设置失败 |
| 重复内容提交 | 确认当前歌曲仍形成草稿 | 没有实际换歌也可能按完成设置扣费 |
| 协议规则 | 不带finishSetting的一般配置不扣100 | 严格统一收费需要进一步明确协议入口 |
| 回滚边界 | 后半段失败分支可退金币，但未保存整套配置/成员事务快照 | 不应宣称模式、锁位、已移除成员在异常时全部原子回滚 |
| 房主关闭方式 | 关闭校验开关，仍保留hostOpenId/isHost | 启用时应逐个审核操作；纯锁位、开始不完全受同一分支控制 |
| 人数提示 | 自动踢人提示说达到开局要求 | 实际还需满足完整队伍或心动满6人的开局校验 |
| 未知性别 | 上限统计不计gender=0；规范座位会放入剩余空位 | 存量/异常数据需单独检查，不能把统计通过等同男女合法 |
| 心动展示 | 主界面底图三色分支只判断双人 | 心动入队成功不一定显示对应三色底图 |
| 离场提示范围 | 对全DS列表做占位差异和leaveEvent处理 | 当前未按“观看的同一舞台”过滤所有离场提示 |
| 批量离场提示 | 一次快照只选取一个departedName，自动踢人先移除再逐人广播 | 多人同时离场的其他客户端提示可能不完整 |
| 瞬时事件与版本 | leaveEvent附着在带revision的快照里，无独立确认/重放 | 丢包或被更新版本淘汰时，提示不保证重放 |
| 跨DS重建 | revision只有递增计数，无会话标识 | 需要确认旧客户端缓存遇到新DS时能恢复 |
| 未完成UI | 踢人头像/边框、BindCloseBtn等仍为空实现 | 不应写成已完整实现的交互 |
| 待定位现象 | 用户反馈退出、三色选队无效果 | 静态代码显示有注册和处理；运行时根因尚不能确定 |

部分源码注释仍沿用旧行为，例如“仅房主”“选曲确认保存到服务端”“内容未实现”等。本文按函数体和当前数据整理，不把这些过时注释当作最终行为。

## 19. 排查步骤与联机检查场景

### 19.1 退出或选队无效果时，如何判定卡在哪里

已经能静态确认：

- `StageInfoView.BindClicks` 绑定了退出和三色按钮。
- `CSStageJoin/CSStageLeave` 已在服务端注册。
- 服务端有 `HandleJoin/HandleLeave`，且成功后会推送列表。
- 客户端注册了列表接收与界面刷新链。

下一步应使用同一次点击的运行时证据定位：

| 检查点 | 需要观察 | 没有到达或不一致时的方向 |
| --- | --- | --- |
| 1. 按钮回调 | OnBtnExitClick或JoinSelectedTeam是否执行 | 实际运行Prefab、Button引用、遮挡、interactable、Start/OnEnable报错 |
| 2. 客户端请求 | 协议类型；加入的stageId/teamId/slotIndex | 客户端提前return、系统未就绪、旧脚本实例 |
| 3. DS收包 | OnC2SEventHandle收到协议和真实player | 运行环境、网络事件初始化、客户端/DS版本 |
| 4. DS分发 | 对应Handle是否执行 | handler注册、反序列化、启动阶段异常 |
| 5. 业务结果 | ok/code/msg，操作前后occupancy与slots | 实际性别、模式、阶段、占位/锁定拒绝 |
| 6. 回包 | SCStageListSync的code/msg/revision/stages | 服务端中途异常、发送失败或运行版本差异 |
| 7. 客户端应用 | myOpenId匹配、revision是否接受、myStageId是否变化 | 身份/结构/旧版本过滤问题 |
| 8. UI刷新 | ListChanged、RefreshSlots、SetOccupied/SetEmpty | 订阅、脚本解析、Prefab覆盖和显示异常 |
| 9. 世界表现 | 座位已正确但人物/镜头仍停留 | 单独检查GameManager及舞蹈清理/站位链 |

退出要检查原座位和本人身份是否清空。选队要检查本人被放到了对应性别的目标格；同队重复加入成功时，画面本来就可能没有变化。

现有日志入口包括 `BaseNetPacket.Deserialize`、`ServerEventNetwork.OnC2SEventHandle`、`NetPacketManager.Handle` 的未注册提示，以及 `UISystem` 打开/关闭日志。它们不能单独证明整条业务处理已成功。

### 19.2 建议的联机检查清单

下面是文档整理出的检查场景，**本次没有启动Unity/DS执行这些场景**。

- [ ] 未加入舞台时，可以普通加入；服务端分配座位，开始按钮随后出现。
- [ ] 男、女分别加入蓝/红/绿队，落到1/2、3/4、5/6正确座位。
- [ ] 目标队伍同性别位置被占时，返回占用错误，不占异性格。
- [ ] 未选择性别时，双人/心动加入被明确拒绝。
- [ ] 同房换队保留joinedOrder，旧位清空、新位占用。
- [ ] 退出后服务端occupancy与客户端myStageId均清空。
- [ ] 倒计时及对局中退出能清理，不被迟到详情/对局包重新入房。
- [ ] 仅关闭设置页不会退房。
- [ ] 模式Toggle和选曲确认不会立即改主界面已生效配置。
- [ ] 设置页取消丢弃草稿，不撤销已完成的锁位或踢人等操作。
- [ ] 无草稿点击完成设置不发包；重复确认当前歌曲的现状符合产品预期。
- [ ] 99金币完成设置失败，100金币成功后为0。
- [ ] 游戏已开始时完成设置返回明确失败文案。
- [ ] 双人和心动分别验证4男/4女：优先移除同一性别最晚加入者。
- [ ] 验证操作者恰好是最晚超额成员时的行为。
- [ ] 验证2男3女通过人数上限，但仍不能错误地直接开局。
- [ ] 冠军只锁一空位；双人一键锁/解锁两格。
- [ ] 双人队内已有任意成员时锁队失败；心动没有锁按钮。
- [ ] 模式草稿期间不误发新布局的换座/锁位请求。
- [ ] 模式真正生效后全部锁打开；只换音乐不清全部锁。
- [ ] 任意金币余额均可打开踢人弹窗，确认按钮不按余额禁用。
- [ ] 使用明确的非零测试费用验证“确认才提示金币不足”；当前0费用无法覆盖该分支。
- [ ] 踢机器人免费，且不要求操作者背包数据加载。
- [ ] 弹窗打开后目标换座或离开，再确认不误踢其他人。
- [ ] 被踢本人显示UI_KickedTipView，其他人文案为“被踢出房间”。
- [ ] 最后一名真人离开后机器人消失，房间恢复默认配置。
- [ ] 双人全空、残队、1/2/3完整队伍分别检查开局条件。
- [ ] 心动不足6人不能开始，6格全满才能开始。
- [ ] 主界面的模式、歌曲、BPM跟随权威列表；实际音频播放另行确认。
- [ ] 选曲、踢人确认、被踢提示的Canvas排序符合当前产品层级要求。
- [ ] 断线重连、服务端重建、回包乱序后能恢复正确成员身份。
- [ ] 连续打开/关闭页面不会重复绑定，单次点击不会发出重复请求。

## 20. 相关源码索引

目录和章节引用使用 Obsidian 内部链接。源码索引指向笔记库外的本机绝对路径，能否直接打开取决于查看器对外部文件链接的处理；也可以复制路径定位。项目迁移后应更新路径。定位函数时优先搜索函数名，避免后续修改导致行号变化。以下索引涵盖核心实现及其配置、网络、数据、表现、Prefab依赖。


### 20.1 View 和座位控件

| 文件 | 重点入口与职责 |
| --- | --- |
| [RoomEnterView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/RoomEnterView.lua>) | SelectMode、OnFinishSetting、SetPendingMusic、RefreshFromStage、OnClose；设置草稿和三模式面板 |
| [MusicSwitchView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/MusicSwitchView.lua>) | BuildMusicSlots、RefreshCurrentSelection、OnBtnConfirmClick；选曲列表及草稿交回 |
| [UI_MusicSlotWidget.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/UI_MusicSlotWidget.lua>) | InitItem、SetSelected；歌曲文字、回调和两张图片 |
| [UI_RoomSlotPanel.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/UI_RoomSlotPanel.lua>) | RefreshRoomSlot、ApplyRoomSlot；冠军/通用六座位容器 |
| [UI_DoubleRoomSlotsWidget.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/UI_DoubleRoomSlotsWidget.lua>) | RefreshRoomSlot、ApplyRoomSlot；双人六座位容器 |
| [UI_HeartBeatRoomSlotsWidget.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/UI_HeartBeatRoomSlotsWidget.lua>) | RefreshRoomSlot、ApplyRoomSlot；心动六座位容器 |
| [UI_RoomSlot.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/UI_RoomSlot.lua>) | Bind、SetEmpty、SetOccupied、OnSlotClick、OnLockClick、OnUnlockClick、OnKickClick |
| [StageInfoView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/StageInfoView.lua>) | ApplyStageHeader、RefreshSlots、RefreshJoinedActions、JoinSelectedTeam、OnBtnExitClick、BindClicks |
| [StageSlotWidget.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/Widget/StageSlotWidget.lua>) | Bind、SetEmpty、SetOccupied、ApplyRankBg、OnSlotClick；主界面座位 |
| [MainMenuView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/MainMenuView.lua>) | 其他主菜单按钮；房间信息由内嵌StageInfoView负责 |
| [KickPlayerTipView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/KickPlayerTipView.lua>) | SetKickTarget、GetKickCost、GetLocalCurrency、OnBtnConfirmClick |
| [KickedTipView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/KickedTipView.lua>) | ShowKickReason、OnConfirmClick；被踢者提示 |
| [PlayerLeaveStageTipView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/PlayerLeaveStageTipView.lua>) | ShowPlayerName、Update；离场文案与淡出 |
| [StageMainMenuView.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/View/StageMainMenuView.lua>) | BtnQuitClick、BtnEndDanceClick；对局中的退出与结束入口 |

### 20.2 客户端系统与表现衔接

| 文件 | 重点入口与职责 |
| --- | --- |
| [StageSystem.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/StageSystem/StageSystem.lua>) | Join、JoinTeam、Leave、SetConfig、SetSlotLocked、Kick、AddRobot、Ready、Start、两类快照入口 |
| [StageDanceClient.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/StageSystem/StageDanceClient.lua>) | AcceptDanceState、StopNetworkDance、ShowDanceError、SyncDanceBgm、FinishDance |
| [StageRobotClient.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/StageSystem/StageRobotClient.lua>) | SyncStageRobots、ClearStageRobots；机器人模型生命周期 |
| [UISystem.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/UISystem/UISystem.lua>) | UILayers、OpenUI、CloseUI、GetUI、CreateUI、SetLayer；缓存与Canvas排序 |
| [PlayerSystemRegister.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/PlayerSystem/PlayerSystemRegister.lua>) | Awake、OnPlayerJoined、OnPlayerRejoined、OnActorSpawned、OnDestroy；StageSystem注册与同步 |
| [NewbieGuideSystem.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/NewbieGuideSystem/NewbieGuideSystem.lua>) | EnterChampionStage；新手邀请后的入座入口 |
| [GameManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/GameManager/GameManager.lua>) | ExitDanceMode、舞台相机和站位入口；联机退出后的表现 |
| [AudioSystem.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/AudioSystem/AudioSystem.lua>) | BGM资源播放与时长查询；后续选曲播放衔接需要检查 |
| [TestSystemRegister.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/TestSystem/TestSystemRegister.lua>) | Alpha7、AddTestCurrency；测试加100000金币 |
| [index.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/System/index.lua>) | StageSystem、StageDanceClient、StageRobotClient加载顺序 |
| [ClientPlayerData.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/Model/ClientPlayerData.lua>) | 客户端玩家聚合与档案访问 |
| [ClientBagData.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/Model/ClientBagData.lua>) | 本地金币读取、ApplyServerData等背包镜像能力 |

### 20.3 服务端与玩家数据

| 文件 | 重点入口与职责 |
| --- | --- |
| [ServerStageManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/ServerStageManager.lua>) | 舞台内存、所有Handle入口、Join/Leave、锁位、费用、自动踢人、机器人、CanStart |
| [ServerStageDance.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/ServerStageDance.lua>) | Begin、Tick、Handle、Snapshot；准备结束后的联机对局推进 |
| [GameServerModule.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/GameServerModule.lua>) | Start、Update、OnPlayerJoined、OnPlayerRejoined、OnPlayerLeft；DS生命周期 |
| [ServerPlayerManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/ServerPlayerManager.lua>) | 在线玩家查询与玩家数据生命周期；踢人/详情推送依赖GetPlayer |
| [ServerNewbieGuideManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/ServerNewbieGuideManager.lua>) | HandleSetPlayerGender；服务端XingBie写入入口 |
| [ServerGMManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/ServerGMManager.lua>) | HandleGMAddCurrency；测试金币请求 |
| [ServerPlayerDataManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Data/ServerPlayerDataManager.lua>) | Get(openId)；服务端玩家聚合查询 |
| [ServerBagData.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Data/ServerBagData.lua>) | 服务端背包数据域；金币校验与更新依赖 |
| [index.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Logic/index.lua>) | 服务端业务模块加载 |

### 20.4 共享配置与网络

| 文件 | 重点入口与职责 |
| --- | --- |
| [RoomSettingDataLib.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/Config/RoomSettingDataLib.lua>) | 模式配置、开放状态、踢人费、ID映射、房主权限开关 |
| [MusicDataLib.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/Config/MusicDataLib.lua>) | 音乐配置、按ID查询和排序 |
| [GamePlayDataLib.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/Config/GamePlayDataLib.lua>) | 玩法mode枚举、站位与回合配置 |
| [StageDanceRules.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/Config/StageDanceRules.lua>) | DefaultBgmKey、准备与节奏参数 |
| [index.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/index.lua>) | 共享配置和网络模块加载 |
| [NetPacketType.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacketType.lua>) | CS/SC协议名称 |
| [BaseNetPacket.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/BaseNetPacket.lua>) | Serialize、Deserialize；外层包结构 |
| [NetPacketManager.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacketManager.lua>) | CreatePacket、RegisterHandle、Handle；注册与分发 |
| [index.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/index.lua>) | 协议包类加载 |
| [ClientEventNetwork.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/Network/ClientEventNetwork.lua>) | C2S发送、S2C接收与初始化 |
| [ClientPacketRegister.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Client/Network/ClientPacketRegister.lua>) | SCStageListSync、SCStageDetailSync、SCStageDance及金币回包分发 |
| [ServerEventNetwork.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Network/ServerEventNetwork.lua>) | OnC2SEventHandle、SendToPlayer、BroadcastAll；真实发送者与回包 |
| [ServerPacketRegister.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Server/Network/ServerPacketRegister.lua>) | CSStage系列处理器注册 |

### 20.5 房间协议包类

| 文件 | 重点入口与职责 |
| --- | --- |
| [CSStageRequest.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageRequest.lua>) | 请求快照 |
| [CSStageJoin.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageJoin.lua>) | 普通加入、选队、换座 |
| [CSStageLeave.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageLeave.lua>) | 本人离场 |
| [CSStageSetConfig.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageSetConfig.lua>) | 一般配置、完成设置、锁位 |
| [CSStageKick.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageKick.lua>) | 手动踢人 |
| [CSStageAddRobot.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageAddRobot.lua>) | 添加机器人 |
| [CSStageReady.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageReady.lua>) | 准备标志 |
| [CSStageStart.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageStart.lua>) | 开始倒计时 |
| [CSStageDance.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSStageDance.lua>) | 对局动作 |
| [SCStageListSync.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/SCStageListSync.lua>) | 列表及房间操作结果 |
| [SCStageDetailSync.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/SCStageDetailSync.lua>) | 本站详情 |
| [SCStageDance.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/SCStageDance.lua>) | 对局状态 |
| [S2CRefreshCurrency.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/S2CRefreshCurrency.lua>) | 费用后的金币同步 |
| [CSGMAddCurrency.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/CSGMAddCurrency.lua>) | 测试加钱请求 |
| [SCGMAddCurrency.lua](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Scripts/Common/NetworkPacket/NetPacket/SCGMAddCurrency.lua>) | 测试加钱结果 |

### 20.6 Prefab 与界面注册

| 文件 | 重点入口与职责 |
| --- | --- |
| [Client.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/Client.prefab>) | UI key、Prefab及客户端系统绑定 |
| [UI_MainMenuView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_MainMenuView.prefab>) | 主菜单，包含舞台信息实例 |
| [UI_StageInfoView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_StageInfoView.prefab>) | 主界面舞台控件绑定 |
| [UI_RoomEnterView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_RoomEnterView.prefab>) | 房间设置页控件绑定 |
| [UI_MusicSwitchView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_MusicSwitchView.prefab>) | 音乐弹窗 |
| [UI_KickPlayerTipView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_KickPlayerTipView.prefab>) | 踢人确认弹窗 |
| [UI_KickedTipView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_KickedTipView.prefab>) | 被踢提示 |
| [UI_PlayerLeaveStageTipView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_PlayerLeaveStageTipView.prefab>) | 其他玩家离场提示 |
| [UI_StageMainMenuView.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/View/UI_StageMainMenuView.prefab>) | 对局菜单及退出按钮 |
| [UI_ChampionRoomSlotsWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_ChampionRoomSlotsWidget.prefab>) | 冠军六槽 |
| [UI_DoubleRoomSlotsWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_DoubleRoomSlotsWidget.prefab>) | 双人六槽 |
| [UI_HeartBeatRoomSlotsWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_HeartBeatRoomSlotsWidget.prefab>) | 心动六槽 |
| [UI_RoomSlotWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_RoomSlotWidget.prefab>) | 设置页单槽 |
| [UI_StageSlotWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_StageSlotWidget.prefab>) | 主界面单槽 |
| [UI_MusicSlotWidget.prefab](<D:/Work Env/work/douyin/DouYinDancing/Assets/DSTemplate/Prefabs/UI/Widget/UI_MusicSlotWidget.prefab>) | 歌曲条目及选中/未选中图片 |

## 21. 后续维护时需要一起考虑的内容

### 21.1 新增或调整模式

- 更新配置项、开放状态和配置ID到玩法mode的映射，不新增未经约定的配置字段。
- 同步检查服务端Mode枚举、客户端直接使用模式数值的位置。
- 检查Toggle、面板、座位布局、锁位、性别座位、人数上限、开局条件。
- 检查队伍角色、站位、对局评分和主界面底图。
- 明确模式变化是否清锁，原成员如何保留、重排或移除。
- 保持设置预览与真正提交的时间边界。

### 21.2 补全音乐播放

- 补齐配置资源字段，明确音乐ID到AudioSystem资源key的转换。
- 让服务端根据已保存musicId决定正式BGM，核对当前CSStageStart参数的可信范围。
- 同步音乐时长、回合计算、BPM展示与实际节奏设计。
- 处理资源不存在、加载未完成、音乐ID失效和默认回退。
- 同时验证主界面文字变化及实际听到的音频，不能只验证其中一项。

### 21.3 完成设置费用配置化

- 确定RoomSettingDataLib中的正式费用字段及缺失时策略。
- 替换服务端FINISH_SETTING_COST，不重新加入未经约定的硬编码回退。
- 明确没有实际变化、重复提交、同房并发设置、自动踢出操作者的收费规则。
- 明确一般配置与finishSetting请求的边界，避免不同入口费用规则不同。
- 考虑失败恢复草稿、请求超时、请求ID及重复处理。
- 若要求整体失败不改变任何房间状态，应增加真正覆盖配置、锁位、成员的回滚设计。

### 21.4 调整离场或踢人

- 保持slots、players、occupancy、teams及danceMatch成员一致。
- 区分主动离开、手动踢出、系统模式整理与平台断线离房。
- 检查最后一名真人离开后的机器人及默认房间重置。
- 检查退出途中收到旧列表、旧详情、旧对局消息的行为。
- 区分房间身份清理、UI显隐和世界角色/镜头清理。
- 若修改通知范围或多人离场展示，需一起处理leaveEvent与普通列表差异推断。

### 21.5 文档维护

后续源码修改后，优先复核本文中的配置数值、层级表、完成设置时序、开局条件和“当前边界”表。函数注释与函数体冲突时，应以已核实的实现为准，并记录尚待实现的需求。

相关笔记：

- [[DSTemplate模板框架与Scripts目录说明]]
- [[客户端与服务端网络通信说明]]
- [[DSTemplate数据存储详解]]
- [[DSTemplate业务系统接入指南]]

本文只新增说明文档，没有修改房间逻辑、服务端脚本、配置表或Prefab；检查场景是待执行清单，不是测试通过报告。
