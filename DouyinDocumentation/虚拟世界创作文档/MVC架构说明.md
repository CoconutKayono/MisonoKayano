# MVC 架构说明

## 1. MVC 是什么

MVC 是 Model、View、Controller 三个英文单词的缩写：

- Model：模型层，负责数据、状态和核心业务规则；
- View：视图层，负责界面展示和用户输入；
- Controller：控制器层，负责接收用户操作、组织业务流程并调用 Model。

MVC 的核心目标是分离数据、业务流程和界面表现。

~~~text
用户操作
   ↓
View
   ↓
Controller
   ↓
Model 修改数据
   ↓
Model 发布数据变化
   ↓
View 刷新界面
~~~

## 2. MVC 各层职责

### 2.1 Model 层

Model 不只是一个普通数据表，它通常包括：

- 业务数据；
- 状态管理；
- 数据读写；
- 数据合法性校验；
- 核心业务规则；
- 数据变化事件。

例如金币 Model 可以负责：

- 查询金币数量；
- 增加或扣除金币；
- 判断金币是否足够；
- 防止金币变成负数；
- 发布金币变化事件。

~~~lua
CoinModel = {
    coin = 0,
    listeners = {},
}

function CoinModel:GetCoin()
    return self.coin
end

function CoinModel:AddCoin(value)
    if type(value) ~= "number" or value <= 0 then
        return false, "invalid value"
    end

    self.coin = self.coin + value
    self:Emit("CoinChanged", self.coin)
    return true
end

function CoinModel:SpendCoin(value)
    if self.coin < value then
        return false, "not enough coin"
    end

    self.coin = self.coin - value
    self:Emit("CoinChanged", self.coin)
    return true
end
~~~

Model 不应该直接操作按钮、文本或页面，也不应该依赖 Unity UI 组件。

### 2.2 View 层

View 负责：

- 显示数据；
- 收集按钮、滑动、输入框等用户操作；
- 调用 Controller 提交用户意图；
- 监听数据变化并刷新界面；
- 处理纯界面表现。

View 不应该负责：

- 直接修改 Model；
- 判断玩家是否满足业务条件；
- 直接写入 DataStore；
- 决定奖励数量；
- 处理复杂业务流程。

~~~lua
RewardView = {}

function RewardView:OnClickReceive()
    self.controller:ReceiveReward(self.rewardId)
end

function RewardView:OnRewardChanged(data)
    self.coinText.text = tostring(data.coin)
    self.receiveButton.interactable = not data.received
end
~~~

### 2.3 Controller 层

Controller 负责：

- 接收 View 的用户操作；
- 组织参数；
- 调用 Model 或业务服务；
- 处理成功、失败和加载状态；
- 控制页面跳转；
- 将结果反馈给 View。

Controller 不应该把所有核心业务规则都写进去。奖励是否已经领取、奖励数量是多少、玩家是否满足条件，应由 Model 或领域服务负责。

~~~lua
RewardController = {}

function RewardController:ReceiveReward(rewardId)
    if self.isRequesting then
        return
    end

    self.isRequesting = true
    self.view:SetLoading(true)

    local result = self.rewardModel:ReceiveReward(rewardId)

    self.isRequesting = false
    self.view:SetLoading(false)

    if not result.success then
        self.view:ShowError(result.message)
    end
end
~~~

Controller 是流程协调者，不应该成为万能类。

## 3. 一个完整的 MVC 流程

以领取成就奖励为例：

~~~text
1. 用户点击领取按钮
       ↓
2. AchievementView 调用 AchievementController
       ↓
3. Controller 调用 AchievementModel
       ↓
4. Model 检查成就是否完成、奖励是否领取
       ↓
5. Model 修改奖励状态
       ↓
6. Model 发布 AchievementChanged 事件
       ↓
7. AchievementView 收到事件
       ↓
8. View 刷新按钮、奖励数量和提示文字
~~~

示意代码：

~~~lua
function AchievementController:ReceiveReward(achievementId)
    local result = self.model:ReceiveReward(achievementId)

    if not result.success then
        self.view:ShowError(result.message)
    end
end

function AchievementModel:ReceiveReward(achievementId)
    local achievement = self:Get(achievementId)

    if achievement == nil then
        return { success = false, message = "achievement not found" }
    end

    if not achievement.completed then
        return { success = false, message = "achievement is not completed" }
    end

    if achievement.received then
        return { success = false, message = "reward already received" }
    end

    achievement.received = true
    self:Emit("AchievementChanged", achievement)

    return { success = true, data = achievement }
end
~~~

## 4. Model 发布事件是否正确

可以。事件驱动 MVC 中常见的数据流是：

~~~text
Model 数据发生改变
    ↓
Model 发布事件
    ↓
View 或 ViewModel 监听事件
    ↓
重新读取 Model 数据并刷新
~~~

MVC 并不强制要求 Model 必须发布事件，也可以由 Controller 在 Model 修改后主动通知 View。但当一个 Model 会影响多个 View，或者数据可能由网络回包、定时器、后台任务修改时，Model 发布事件通常更合适。

推荐事件表达状态变化：

~~~text
CoinChanged
AchievementChanged
PlayerDataLoaded
BuffAdded
BuffRemoved
~~~

不推荐 Model 发布和具体界面绑定的事件：

~~~text
ShowCoinPanel
HideReceiveButton
PlayRewardAnimation
~~~

后者属于 View 或表现层职责。

## 5. Client/Server 架构下的 MVC

联网游戏中，客户端和服务端通常是两套相互协作的 MVC：

~~~text
客户端 View
    ↓
客户端 Controller / System
    ↓ C2S 请求
服务端 Controller / Manager
    ↓
服务端 Model / Data
    ↓
服务端持久化
    ↓ S2C 回包
客户端 Model 更新
    ↓
客户端 View 刷新
~~~

服务端是最终权威，客户端 Model 只是服务端数据的镜像。

结合 DSTemplate，可以大致对应为：

| MVC 概念 | DSTemplate 中的对应模块 |
| --- | --- |
| Model | Server*Data、Client*Data、ServerPlayerData、ClientPlayerData |
| Controller / Application Service | Server*Manager、客户端 *System |
| View | UI、View 脚本、表现逻辑 |
| Event | ClientDataBase 事件、网络回包、同步变量变化 |

推荐数据流：

~~~text
View
  ↓
Client System
  ↓ C2S
Server Manager
  ↓
Server Data
  ↓ Update / Create / Remove
DataStore
  ↓ S2C
Client Data
  ↓ Event
View
~~~

客户端不能直接修改最终业务数据：

~~~lua
-- 不推荐
clientPlayerData.coin = clientPlayerData.coin + 100
~~~

正确方式是客户端发送意图，由服务端校验和修改权威数据，再通过 S2C 回包更新客户端 Model。

## 6. MVC 的优点

### 6.1 关注点分离

数据、业务流程和界面表现各自负责不同内容，降低模块耦合。

### 6.2 便于测试

Model 可以脱离 UI 单独测试，例如成就是否能解锁、金币是否足够、Buff 是否正确添加。

### 6.3 便于更换界面

同一套 Model 和 Controller 可以服务于 PC UI、移动端 UI、调试面板、GM 工具和自动化测试界面。

### 6.4 适合业务边界清晰的系统

成就、背包、排行榜、Buff、商业化等系统都可以使用 MVC 方式拆分。

## 7. MVC 常见问题

### 7.1 Controller 变成万能类

如果 Controller 同时负责业务规则、网络、存档、UI、特效和日志，应该将：

- 领域规则放到 Model 或领域服务；
- 持久化放到 DataStore 或 Repository；
- UI 表现放到 View；
- Controller 保留流程协调。

### 7.2 View 直接修改 Model

下面的写法会绕过权限校验、事件通知和持久化流程：

~~~lua
function RewardView:OnClick()
    self.playerData.coin = self.playerData.coin + 100
end
~~~

应该由 View 调用 Controller 或 System，由业务层修改 Model。

### 7.3 Model 依赖 View

Model 不应该持有 coinText、Button、GameObject 等 UI 引用，否则无法脱离界面测试和复用。

### 7.4 事件订阅没有解绑

View 销毁后仍然收到事件，可能导致重复刷新、空引用和内存泄漏。事件订阅和解绑必须成对出现。

## 8. MVC 适用场景

MVC 适合：

- 业务流程清晰；
- View 数量较少；
- Controller 主要负责流程协调；
- Model 和 UI 之间没有特别复杂的数据转换；
- 需要快速搭建业务系统。

如果客户端界面状态复杂、双向绑定较多，可以考虑 MVVM；如果希望 View 完全被动且 Presenter 可独立测试，可以考虑 MVP。

## 9. MVC 接入清单

- [ ] View 只负责展示和采集用户输入；
- [ ] View 不直接修改 Model；
- [ ] Controller 接收用户操作并协调流程；
- [ ] 核心业务规则位于 Model 或领域服务；
- [ ] Model 不依赖具体 View；
- [ ] Model 数据变化通过事件或统一通知机制传播；
- [ ] 事件订阅和解绑成对出现；
- [ ] 客户端不能绕过服务端修改权威数据；
- [ ] DataStore 读写不放在 View 中；
- [ ] Controller 没有演变成万能类。

