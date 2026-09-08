# MVP 架构说明

## 1. MVP 是什么

MVP 是 Model、View、Presenter 三个英文单词的缩写：

- Model：模型层，负责数据和业务规则；
- View：视图层，负责显示和采集输入；
- Presenter：表示层，负责连接 View 和 Model，并组织页面逻辑。

MVP 与 MVC 的主要区别是：

- MVC 中 Controller 通常接收用户操作并调用 Model；
- MVP 中 Presenter 通常持有 View 接口，并主动调用 View 更新界面；
- View 在 MVP 中更加被动，只负责执行 Presenter 要求的显示操作；
- Presenter 可以在没有真实 UI 的情况下使用 Mock View 测试。

~~~text
用户操作
   ↓
View 调用 Presenter
   ↓
Presenter 调用 Model / Service
   ↓
Model 返回结果或发布变化
   ↓
Presenter 处理结果
   ↓
Presenter 调用 View 接口刷新
~~~

## 2. MVP 各层职责

### 2.1 Model 层

Model 负责：

- 业务数据；
- 数据加载和保存；
- 核心业务规则；
- 远程接口或本地数据访问；
- 业务结果和错误信息。

Model 不直接操作 View，不应该调用 UI 控件。

### 2.2 View 层

MVP 中的 View 通常是被动 View，主要负责：

- 展示 Presenter 提供的数据；
- 将用户操作转发给 Presenter；
- 执行 Presenter 要求的 UI 操作；
- 管理 UI 控件的具体表现。

View 可以通过接口暴露显示方法：

~~~lua
RewardView = {}

function RewardView:ShowLoading()
    self.loading:SetActive(true)
end

function RewardView:HideLoading()
    self.loading:SetActive(false)
end

function RewardView:ShowReward(data)
    self.coinText.text = tostring(data.coin)
    self.receiveButton.interactable = not data.received
end

function RewardView:ShowError(message)
    self.errorText.text = message
end

function RewardView:OnClickReceive()
    self.presenter:ReceiveReward(self.rewardId)
end
~~~

View 不负责直接操作 Model、判断业务是否成功、组织复杂流程或处理持久化。

### 2.3 Presenter 层

Presenter 负责：

- 接收 View 的用户操作；
- 调用 Model、System 或 Service；
- 处理加载状态；
- 处理成功和失败；
- 把 Model 数据转换成 View 所需数据；
- 通过 View 接口主动刷新 UI；
- 页面销毁时解除监听和回调。

~~~lua
RewardPresenter = {}

function RewardPresenter:New(view, model)
    return {
        view = view,
        model = model,
        disposed = false,
    }
end

function RewardPresenter:ReceiveReward(rewardId)
    if self.disposed then
        return
    end

    self.view:ShowLoading()

    local result = self.model:ReceiveReward(rewardId)

    self.view:HideLoading()

    if not result.success then
        self.view:ShowError(result.message)
        return
    end

    self.view:ShowReward(result.data)
end

function RewardPresenter:Dispose()
    self.disposed = true
    self.view = nil
    self.model = nil
end
~~~

Presenter 是页面逻辑的集中位置，但不应该变成整个项目的万能业务层。

## 3. 一个完整的 MVP 流程

以成就详情页为例：

~~~text
用户打开页面
    ↓
AchievementView 创建 Presenter
    ↓
Presenter 请求 AchievementModel 加载数据
    ↓
Model 返回成就数据
    ↓
Presenter 将数据转换成 View 所需结构
    ↓
Presenter 调用 View.ShowAchievement
    ↓
View 刷新界面

用户点击解锁
    ↓
View 调用 Presenter.Unlock
    ↓
Presenter 调用 Model / System
    ↓
服务端返回结果
    ↓
Presenter 判断成功或失败
    ↓
Presenter 调用 View.ShowSuccess / ShowError
~~~

示意代码：

~~~lua
function AchievementPresenter:Load(achievementId)
    self.view:ShowLoading()

    self.model:GetAchievement(
        achievementId,
        function(result)
            if self.disposed then
                return
            end

            self.view:HideLoading()

            if result.code ~= 0 then
                self.view:ShowError(result.msg)
                return
            end

            self.view:ShowAchievement({
                title = result.data.title,
                progress = result.data.current .. "/" .. result.data.target,
                canUnlock = result.data.current >= result.data.target,
                received = result.data.received,
            })
        end
    )
end

function AchievementPresenter:Unlock(achievementId)
    self.view:ShowLoading()

    self.system:CSUnLockAchievement(
        achievementId,
        function(result)
            if self.disposed then
                return
            end

            self.view:HideLoading()

            if result.code == 0 then
                self.view:ShowAchievement(result.data)
                self.view:ShowToast("解锁成功")
            else
                self.view:ShowError(result.msg)
            end
        end
    )
end
~~~

实际项目中，网络回调也可以由客户端 System 统一接收，再通过事件通知 Presenter。核心思想是 Presenter 把业务结果翻译成 View 能执行的显示操作。

## 4. View 接口与被动 View

MVP 的重要实践是定义 View 接口：

~~~lua
IRewardView = {
    ShowLoading = function() end,
    HideLoading = function() end,
    ShowReward = function(data) end,
    ShowError = function(message) end,
}
~~~

Presenter 只依赖这个接口，而不依赖具体 Unity 页面实现。

真实 View：

~~~lua
UnityRewardView = {}

function UnityRewardView:ShowReward(data)
    self.coinText.text = tostring(data.coin)
end
~~~

测试 View：

~~~lua
MockRewardView = {}

function MockRewardView:ShowReward(data)
    self.lastReward = data
end

function MockRewardView:ShowError(message)
    self.lastError = message
end
~~~

这样可以在不启动 Unity 场景的情况下测试 Presenter：

~~~lua
local view = MockRewardView:New()
local model = FakeRewardModel:New()
local presenter = RewardPresenter:New(view, model)

presenter:ReceiveReward(1001)

assert(view.lastReward ~= nil)
~~~

## 5. MVP 中的事件处理

### 5.1 Presenter 接收 Model 回调

~~~text
Model 数据变化
    ↓
Presenter 收到回调
    ↓
Presenter 调用 View 刷新
~~~

~~~lua
function RewardPresenter:OnEnable()
    self.model:On("RewardChanged", self.OnRewardChanged, self)
end

function RewardPresenter:OnRewardChanged(data)
    if self.disposed then
        return
    end

    self.view:ShowReward(data)
end

function RewardPresenter:OnDisable()
    self.model:Off("RewardChanged", self.OnRewardChanged, self)
end
~~~

### 5.2 Presenter 主动拉取 Model

~~~text
用户操作或页面生命周期
    ↓
Presenter 查询 Model
    ↓
Presenter 调用 View 刷新
~~~

这种方式适合页面数据量小、数据变化来源少或页面只在打开和操作后刷新。对于 Buff、玩家属性、背包、在线状态等实时变化数据，通常使用 Model 事件加 Presenter 转发更合适。

## 6. MVP 在 DSTemplate 中的对应关系

| MVP 概念 | DSTemplate 中的对应模块 |
| --- | --- |
| Model | Client*Data、Server*Data、ClientPlayerData、ServerPlayerData |
| Presenter | 页面 Presenter、客户端 *System 中的页面协调部分 |
| View | UI 脚本、UI Prefab、页面控件 |
| Model Service | Server*Manager、客户端网络 System |
| Model Event | ClientDataBase 事件、S2C 回包、同步变量事件 |

推荐客户端流程：

~~~text
View
  ↓ 用户操作
Presenter
  ↓
Client System
  ↓ C2S
Server Manager
  ↓
Server Data
  ↓ S2C
Client Data
  ↓ 事件
Presenter
  ↓
View
~~~

在这种结构中：

- Client*Data 保存服务端同步过来的客户端镜像；
- Client System 负责发送请求和接收协议；
- Presenter 将 Client Data 转换为页面数据；
- View 只执行显示动作；
- Server Manager 和 Server Data 保证最终业务权威。

## 7. MVP 与 MVC 的区别

| 对比项 | MVC | MVP |
| --- | --- | --- |
| UI 更新方式 | View 可监听 Model，也可由 Controller 协调 | Presenter 主动调用 View |
| View 的主动程度 | View 通常可以参与一定展示逻辑 | View 更被动 |
| 中间层 | Controller | Presenter |
| 是否持有 View 引用 | Controller 不一定持有 | Presenter 通常持有 View 接口 |
| 测试难度 | 取决于 View 与 Model 的耦合程度 | Presenter 很容易使用 Mock View 测试 |
| 适合场景 | 传统页面和业务流程 | UI 逻辑复杂、希望强测试的页面 |
| 常见问题 | Controller 变成万能类 | Presenter 变成万能类或直接操作具体控件 |

MVC 和 MVP 的边界并不绝对。很多项目会把 Controller、ViewModel、Presenter 和 System 混合使用。判断重点应放在依赖方向和职责，而不是类名。

## 8. MVP 的优点

- View 更容易测试；
- UI 与业务流程隔离；
- 适合复杂交互页面；
- 适合异步请求和页面生命周期管理；
- UI 平台或控件变化时，Presenter 通常不需要大幅修改；
- Presenter 可以统一管理成功、失败、超时和重试。

## 9. MVP 的常见问题

### 9.1 Presenter 直接操作具体控件

不推荐：

~~~lua
function RewardPresenter:Refresh()
    self.view.coinText.text = tostring(self.model.coin)
    self.view.receiveButton.interactable = true
end
~~~

更推荐：

~~~lua
function RewardPresenter:Refresh()
    self.view:ShowReward({
        coin = self.model.coin,
        canReceive = true,
    })
end
~~~

### 9.2 Presenter 变成万能类

Presenter 不应该同时负责业务规则、网络协议、DataStore、UI 控件、埋点、音效和动画。

建议：

- 业务规则放在 Model 或领域服务；
- 网络交互放在 System 或 Service；
- Presenter 只负责当前页面流程；
- 动画和特效放在 View。

### 9.3 异步回调没有检查页面生命周期

页面已经销毁时，网络回调仍然调用 View，会产生空引用或旧页面刷新。回调中应检查 disposed 状态，页面关闭时应解绑监听和取消请求。

### 9.4 View 接口过于庞大

如果一个 View 接口包含几十个方法，说明页面职责可能过多，可以拆分 HeaderView、RewardView、ErrorView、LoadingView 和 ListView。

## 10. MVP 适用场景

MVP 适合：

- 页面交互复杂；
- 需要强单元测试；
- UI 平台或控件经常变化；
- 希望 View 尽量被动；
- 异步请求和页面生命周期较多；
- 团队习惯接口驱动开发。

如果项目已经使用大量自动数据绑定，MVVM 可能更合适；如果页面简单、业务流程清晰，MVC 更轻量。

## 11. MVP 接入检查清单

- [ ] View 通过接口向 Presenter 暴露显示能力；
- [ ] View 的用户操作交给 Presenter；
- [ ] Presenter 不直接依赖具体 UI 控件；
- [ ] Presenter 负责页面流程和结果转换；
- [ ] 核心业务规则不堆在 Presenter；
- [ ] Model 不直接依赖 View；
- [ ] 网络回调检查页面是否已销毁；
- [ ] Model 事件监听和解绑成对出现；
- [ ] 可以使用 Mock View 测试 Presenter；
- [ ] Presenter 没有演变成页面之外的万能业务类。

