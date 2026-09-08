# MVVM 架构说明

## 1. MVVM 是什么

MVVM 是 Model、View、ViewModel 三个英文单词的缩写：

- Model：模型层，负责业务数据和业务规则；
- View：视图层，负责界面展示；
- ViewModel：视图模型层，负责把 Model 转换成 View 能直接使用的状态和命令。

MVVM 的核心特点是：

- View 不直接处理业务逻辑；
- View 通过 ViewModel 获取展示数据；
- View 的操作通过 Command 或方法交给 ViewModel；
- ViewModel 监听 Model 的变化；
- View 通常通过数据绑定自动刷新。

~~~text
Model
  ↓ 数据变化
ViewModel
  ↓ 数据绑定
View

View 用户操作
  ↓ Command
ViewModel
  ↓
Model
~~~

## 2. MVVM 各层职责

### 2.1 Model 层

Model 负责真实业务状态和核心规则：

- 玩家数据；
- 商品数据；
- 成就状态；
- Buff 状态；
- 订单状态；
- 数据加载和保存；
- 业务校验；
- 领域事件。

Model 不应该知道 View 的布局、按钮或文本组件。

### 2.2 View 层

View 负责：

- 显示 ViewModel 提供的状态；
- 将按钮、输入框等操作绑定到 ViewModel 的 Command；
- 处理纯表现逻辑；
- 展示 loading、error、empty 等状态。

View 不负责：

- 直接读取 DataStore；
- 直接调用服务端接口；
- 判断能否购买；
- 修改玩家金币；
- 组织复杂业务流程。

View 更接近声明式描述：

~~~text
金币文本绑定到 ViewModel.coinText
领取按钮绑定到 ViewModel.receiveCommand
加载动画绑定到 ViewModel.isLoading
错误提示绑定到 ViewModel.errorMessage
~~~

### 2.3 ViewModel 层

ViewModel 是 View 和 Model 之间的适配层，负责：

- 暴露 View 需要显示的字段；
- 把复杂 Model 数据转换成界面数据；
- 提供按钮命令；
- 管理 loading、empty、error 等页面状态；
- 监听 Model 事件；
- 调用 System、Service 或 Repository；
- 把异步结果转换成可绑定状态。

例如 Model 中的数据是：

~~~lua
{
    coin = 100,
    isVip = true,
    expireTime = 1780000000,
}
~~~

ViewModel 可以转换为：

~~~lua
{
    coinText = "100",
    vipText = "VIP",
    vipVisible = true,
    expireText = "剩余 30 天",
    canReceive = true,
}
~~~

View 不需要知道时间戳、枚举值和底层数据结构。

## 3. MVVM 的核心：可观察状态和绑定

MVVM 通常需要一个可观察状态：

~~~lua
Observable = {}

function Observable:New(value)
    return {
        value = value,
        listeners = {},
    }
end

function Observable:Set(state, value)
    if state.value == value then
        return
    end

    state.value = value

    for _, listener in ipairs(state.listeners) do
        listener(value)
    end
end
~~~

ViewModel 暴露可观察字段：

~~~lua
RewardViewModel = {}

function RewardViewModel:New(model)
    return {
        model = model,
        coinText = Observable:New("0"),
        isLoading = Observable:New(false),
        errorMessage = Observable:New(""),
        canReceive = Observable:New(false),
    }
end
~~~

View 将界面控件绑定到这些字段：

~~~lua
function RewardView:Bind(viewModel)
    viewModel.coinText:Subscribe(function(value)
        self.coinText.text = value
    end)

    viewModel.canReceive:Subscribe(function(value)
        self.receiveButton.interactable = value
    end)

    viewModel.isLoading:Subscribe(function(value)
        self.loading:SetActive(value)
    end)
end
~~~

关键不是所有字段都必须自动绑定，而是：

~~~text
View 只关心界面状态
ViewModel 负责准备界面状态
Model 负责真实业务状态
~~~

## 4. Command：View 如何发起操作

MVVM 通常使用 Command 表示用户操作：

~~~lua
function RewardViewModel:Init()
    self.receiveCommand = {
        Execute = function()
            self:ReceiveReward()
        end,
        CanExecute = function()
            return self.canReceive.value
                and not self.isLoading.value
        end,
    }
end

function RewardViewModel:ReceiveReward()
    if not self.receiveCommand:CanExecute() then
        return
    end

    self.isLoading:Set(true)
    self.errorMessage:Set("")

    local result = self.system:ReceiveReward(self.rewardId)

    self.isLoading:Set(false)

    if not result.success then
        self.errorMessage:Set(result.message)
    end
end
~~~

View 只需要执行命令：

~~~lua
function RewardView:OnClickReceive()
    self.viewModel.receiveCommand:Execute()
end
~~~

按钮是否可点击，由 ViewModel 的状态决定。

## 5. 一个完整的 MVVM 流程

以成就系统为例：

~~~text
服务端回包
    ↓
ClientAchievementData 更新
    ↓
AchievementViewModel 收到 Model 事件
    ↓
重新计算 canReceive、progressText、rewardText
    ↓
View 自动刷新

用户点击领取
    ↓
View 执行 receiveCommand
    ↓
AchievementViewModel 调用 AchievementSystem
    ↓
AchievementSystem 发送 C2S
    ↓
服务端校验并修改权威数据
    ↓
S2C 回包
    ↓
ClientAchievementData 更新
    ↓
ViewModel 再次计算展示状态
    ↓
View 刷新
~~~

ViewModel 不保存一份与 Model 完全重复的业务数据。它主要保存：

- 当前页面选中的 ID；
- 当前页面 loading 状态；
- 当前页面错误提示；
- 由 Model 派生出来的显示字段；
- Command 和 Command 的可执行状态。

## 6. MVVM 与异步网络

联网游戏中的 MVVM 需要处理异步请求：

~~~text
用户点击
  ↓
ViewModel.isLoading = true
  ↓
发送 C2S
  ↓
等待 S2C
  ├─ 成功：Model 更新，ViewModel 重新计算
  ├─ 业务失败：errorMessage 更新
  └─ 超时：显示重试状态
~~~

无论网络回调由 ViewModel 直接接收，还是由 System 统一接收后通知 ViewModel，都应保证：

- 一次操作不会重复提交；
- loading 状态一定有结束路径；
- 失败结果能显示给用户；
- 成功结果以服务端回包为准；
- ViewModel 销毁时解除网络和 Model 监听。

## 7. MVVM 在 DSTemplate 中的对应关系

| MVVM 概念 | DSTemplate 中的对应模块 |
| --- | --- |
| Model | Client*Data、Server*Data、ClientPlayerData、ServerPlayerData |
| ViewModel | 页面级 ViewModel、客户端 System 中的展示状态适配部分 |
| View | UI 脚本、UI Prefab、页面组件 |
| Command | ViewModel 的按钮命令、System 的业务调用方法 |
| 网络服务 | 客户端 System、服务端 Manager |
| 绑定通知 | ClientDataBase 事件、System 事件、Observable 状态 |

推荐客户端链路：

~~~text
Server 回包
    ↓
ClientPlayerData / Client*Data
    ↓
ViewModel
    ↓
View

View 操作
    ↓
ViewModel Command
    ↓
Client System
    ↓
C2S
~~~

Client Data 仍然是服务端数据镜像，不能因为使用 MVVM 就把客户端 ViewModel 当成持久化数据库。

## 8. MVVM 的优点

- 适合复杂界面；
- 可以把复杂业务数据转换成简单的界面状态；
- 降低 View 的业务复杂度；
- 支持 loading、error、empty 等统一状态；
- 状态变化可以自动驱动界面；
- ViewModel 可以复用于多个页面和调试界面；
- 适合测试展示状态和按钮是否可执行。

## 9. MVVM 的常见问题

### 9.1 ViewModel 变成第二个 Model

ViewModel 不应该保存完整的玩家背包、金币、成就和 Buff 数据。建议：

- Model 保存真实业务状态；
- ViewModel 保存页面状态和派生状态；
- ViewModel 通过 Model 查询数据；
- 不维护互相矛盾的双份业务数据。

### 9.2 双向绑定过多

对于金币、订单、成就、Buff 等权威数据，建议使用单向显示：

~~~text
Server → Model → ViewModel → View
~~~

用户操作通过 Command 发起请求，而不是直接双向修改最终数据。

### 9.3 ViewModel 过度依赖 UI

ViewModel 不应该直接访问 Button、Text、GameObject、Transform 或 Animator。它应该输出 isLoading、canReceive、errorMessage 等普通状态，具体表现由 View 决定。

### 9.4 绑定生命周期没有处理

页面关闭时应解除 Model 事件、网络回调、Timer、Command 订阅和 Observable 监听。

## 10. MVVM 适用场景

MVVM 适合：

- 页面状态较多；
- 有大量按钮、进度、倒计时和条件显示；
- 需要统一处理 loading、error、empty；
- 需要较强的 UI 可测试性；
- 需要多个 View 复用一份展示状态；
- 项目已经具备数据绑定或响应式基础设施。

如果页面很简单，MVVM 可能会增加 ViewModel、Observable 和绑定代码，此时 MVC 或 MVP 更直接。

## 11. MVVM 接入清单

- [ ] Model 保存真实业务状态；
- [ ] ViewModel 只保存页面状态和派生状态；
- [ ] View 不直接修改 Model；
- [ ] View 通过 Command 发起用户操作；
- [ ] ViewModel 不直接依赖 UI 组件；
- [ ] Model 数据变化能够通知 ViewModel；
- [ ] ViewModel 能够重新计算完整界面状态；
- [ ] 网络请求有 loading、成功、失败和超时处理；
- [ ] 权威数据以服务端回包为准；
- [ ] 监听关系在 View、ViewModel、Model 销毁时正确解绑。

