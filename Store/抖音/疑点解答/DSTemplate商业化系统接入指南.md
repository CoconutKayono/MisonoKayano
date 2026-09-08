# DSTemplate 商业化系统接入指南

本文档根据 DSTemplate 商业化快速上手资料整理，说明商品购买、平台支付回调、发货、订单幂等和补单/退款的完整接入方式。商业化链路的核心原则是：客户端只发起购买，服务端根据平台回调和服务端配置决定是否发货。

## 1. 商业化系统的整体链路

~~~text
客户端
  CommercialSystem:PurchaseProduct(productId)
      ↓
平台支付 / 订单创建
      ↓
ServerCommercialManager.OnOrderPaymentCallBack(...)
      ↓
CommercialDataLib：productId → type
      ↓
对应 Deliver Handler
      ↓
业务校验、发奖、ServerReceiptData 幂等记录
      ↓
DouyinMarketingService.ConfirmOrder(...)
      ↓
成功 / 补单 / 退款
~~~

客户端不能根据按钮点击结果直接增加金币、道具或权益。支付成功和业务到账是服务端流程，必须等待平台回调和发货逻辑完成。

## 2. 目录和模块职责

典型目录如下：

~~~text
Commercial/
├─ ServerCommercialManager.lua
├─ ServerCommercialDeliverManager.lua
└─ AircraftShopDeliverHandler.lua

Client/System/CommercialSystem/
├─ CommercialSystem.lua
└─ CommercialSystemRegister.lua

Common/Config/
├─ CommercialDataLib.lua
└─ ShopDataLib.lua

Server/Data/
└─ ServerReceiptData.lua
~~~

| 模块 | 职责 |
| --- | --- |
| CommercialSystem | 客户端发起购买，不直接发奖 |
| ServerCommercialManager | 接收平台订单回调，分发发货 |
| ServerCommercialDeliverManager | 根据商品类型选择 Handler |
| CommercialDataLib | 维护 productId → type 映射 |
| ShopDataLib | 维护商品展示和业务配置所需信息 |
| BaseDeliverHandler 子类 | 校验订单并执行具体业务发货 |
| ServerReceiptData | 订单幂等、防重、补单和终态清理 |

这些模块属于 DS 模板的商业化基础能力。新增商品时优先在配置和 Handler 入口扩展，不要在客户端写一套独立的到账逻辑。

## 3. 商品配置原则

### 3.1 productId 必须按字符串处理

商品 ID 可能较长，不能在 Lua 或配置转换过程中依赖普通数值类型。推荐：

~~~lua
local productId = tostring(productId)
local productType = CommercialDataLib[tostring(productId)]
~~~

配置表、协议和日志中都应保持同一套字符串形式。否则可能出现：

- 映射查找不到；
- 长数字精度丢失；
- 客户端显示 ID 与服务端回调 ID 不一致；
- 同一订单被识别成不同商品。

### 3.2 CommercialDataLib 只做商品类型映射

CommercialDataLib 的核心职责是：

~~~text
productId → type
~~~

它用于决定订单由哪个 Handler 处理，不应把每个商品的具体奖励堆进这个映射表。商品的奖励数量、道具 ID、权益时长等业务信息，应放在对应的业务配置表中，通常通过 ShopDataLib 或玩法自己的配置表读取。

推荐分层：

~~~text
CommercialDataLib：商品属于哪一类
ShopDataLib / 业务配置：这一类商品具体发什么
Deliver Handler：如何校验并发放
ServerReceiptData：订单是否已处理
~~~

## 4. 客户端发起购买

客户端通过 CommercialSystem 发起购买：

~~~lua
local commercialSystem = GetSys("CommercialSystem")
commercialSystem:PurchaseProduct(productId)
~~~

客户端应传递：

- 配置中定义的 productId；
- 当前购买场景需要的业务参数（如果平台流程允许携带）；
- 必要的 UI 状态。

客户端不应传递或决定：

- 最终到账数量；
- 订单是否已经支付成功；
- 是否跳过服务端校验；
- 是否重复领取。

CommercialSystemRegister.lua 负责 System 的创建、IOC 注册、生命周期和回调解绑。包含裸生命周期函数的 Register/Host Script 按模板规则自动挂载，不要在普通 index.lua 中重复 require。

## 5. 服务端订单回调与商品分发

ServerCommercialManager.OnOrderPaymentCallBack 接收平台订单回调后，推荐按以下顺序处理：

1. 提取并规范化 playerOpenId、orderId、productId；
2. 将 productId 转成字符串；
3. 查询 CommercialDataLib 得到商品类型；
4. 根据类型获取对应 BaseDeliverHandler；
5. 读取 ServerReceiptData，判断订单是否已经完成、补单或正在处理；
6. 调用 Handler 执行校验和发货；
7. 根据结果调用 DouyinMarketingService.ConfirmOrder；
8. 按终态清理或保留收据记录。

不要相信客户端传来的“已支付”字段，也不要在找不到商品配置时直接发放默认奖励。

## 6. Deliver Handler 的实现

每一种业务商品类型使用一个 Handler。示例目录中有：

~~~text
AircraftShopDeliverHandler.lua
~~~

Handler 继承 BaseDeliverHandler，至少实现：

~~~lua
function AircraftShopDeliverHandler:IsComplete(playerOpenId)
    -- 判断业务奖励是否已经到账
end

function AircraftShopDeliverHandler:Deliver(
    receiptInfo,
    callback,
    targetPlayer
)
    -- 校验订单、发放业务奖励、回调结果
end
~~~

### 6.1 IsComplete

IsComplete 用于补单和重试场景：

- 如果奖励已经到账，返回已完成，避免重复发奖；
- 如果订单记录存在但业务数据还没到账，允许继续发货；
- 如果玩家当前不在房间，按照业务能力决定是延迟、离线写入还是返回可重试；
- 判断应基于服务端数据，不应只看客户端 UI。

### 6.2 Deliver

Deliver 中应完成：

1. 从 receipt 读取玩家、订单、商品及业务参数；
2. 服务端重新校验商品配置和奖励内容；
3. 判断该订单是否已发货；
4. 通过服务端业务数据域发放奖励并标脏；
5. 成功后通过 callback 返回成功；
6. 失败时返回可重试或不可恢复错误。

发货操作必须具备幂等性。对于“增加数量”类奖励，要先用订单记录或业务流水保证同一 orderId 不会重复增加。

## 7. 订单结果和恢复策略

资料中约定的 receipt code：

| receipt code | 含义 | 处理 |
| --- | --- | --- |
| 0 | 发货成功 | 确认订单，清理或归档终态收据 |
| 1 | 暂时无法完成/补单 | 保留记录并允许平台或系统重试 |
| -1 | 不可恢复/退款 | 不发货或回滚可回滚操作，确认退款 |

回调中的 errorCode 约定：

- errorCode == -10000：不可恢复，应走退款；
- 其他错误或 nil：通常视为可重试，进入补单；
- 业务已完成：应返回成功，不能因为重复回调而再次发奖。

错误分类必须谨慎。网络超时、玩家暂时不在线、数据域未加载、服务端暂时不可用，通常不能直接退款；配置缺失、商品非法或无法安全确认奖励，才更接近不可恢复错误。

## 8. ServerReceiptData 的作用

ServerReceiptData 负责把平台订单回调变成可恢复的服务端状态，主要承担：

- 记录订单和 receipt；
- 防止重复回调重复发货；
- 支持发货失败后的补单；
- 记录成功、补单、退款等终态；
- 在确认订单后清理不再需要的临时记录；
- 为 Handler 的 IsComplete 提供依据。

建议按订单维度设计幂等键，通常至少包含平台订单号 orderId。不要只使用 productId 或玩家 ID，否则同一玩家购买同一商品的两笔订单可能互相覆盖。

ServerReceiptData 本身也应遵循服务端数据域的加载、标脏和 Flush 机制。详情可参考：[DSTemplate 数据存储详解](DSTemplate数据存储详解.md)。

## 9. 新增一种商品类型的步骤

### 9.1 配置

- 在 CommercialDataLib 增加 productId → type；
- 确保 productId 按字符串保存和查找；
- 在 ShopDataLib 或业务配置中添加奖励内容；
- 检查商品配置与平台后台商品 ID 一致。

### 9.2 Handler

- 新建 XxxDeliverHandler.lua；
- 继承 BaseDeliverHandler；
- 实现 IsComplete；
- 实现 Deliver；
- 在 ServerCommercialDeliverManager 注册该类型；
- 确认玩家不在线、数据未加载、重复回调和异常回调的策略。

### 9.3 订单数据

- 确认 ServerReceiptData 已纳入玩家数据聚合或模板规定的订单数据入口；
- 订单写入使用数据域接口，正确设置 dirty；
- 成功、补单、退款的记录状态可区分；
- 订单回调重复触发时不会重复发奖。

### 9.4 联调

至少验证：

1. 正常支付并成功发货；
2. 平台重复回调同一个订单；
3. 回调时玩家不在当前房间；
4. 发货过程中数据域未加载；
5. 发货后确认订单超时；
6. Handler 返回 errorCode == -10000；
7. 临时错误后再次补单；
8. 不存在的 productId；
9. 长数字 productId 的字符串映射；
10. 客户端重开页面后，权益仍由服务端数据决定。

## 10. 安全与一致性检查

商业化链路中，以下规则必须坚持：

- 客户端点击成功不等于支付成功；
- 平台支付成功不等于业务奖励已经成功写入；
- 最终奖励由服务端配置和 Handler 决定；
- 所有发奖逻辑必须可幂等；
- 订单确认应在发货结果明确后执行；
- 可重试错误不要误判为退款；
- 不可恢复错误不要无限重试；
- 商品配置缺失时宁可补单/人工处理，也不要发放默认奖励；
- productId、orderId 的日志要能串起整条链路，但不要记录不必要的敏感信息。

## 11. 商业化接入清单

- [ ] 客户端仅调用 CommercialSystem:PurchaseProduct；
- [ ] productId 全链路按字符串处理；
- [ ] CommercialDataLib 完成商品类型映射；
- [ ] 奖励内容位于业务配置，而不是散落在客户端；
- [ ] Handler 继承 BaseDeliverHandler；
- [ ] Handler 实现 IsComplete 和 Deliver；
- [ ] ServerReceiptData 支持幂等和补单；
- [ ] ServerCommercialDeliverManager 注册 Handler；
- [ ] errorCode == -10000 和其他错误分类正确；
- [ ] receipt code 0/1/-1 的确认策略经过联调；
- [ ] 重复回调不会重复发奖；
- [ ] 正常、失败、超时、玩家离线和补单场景均已验证。

