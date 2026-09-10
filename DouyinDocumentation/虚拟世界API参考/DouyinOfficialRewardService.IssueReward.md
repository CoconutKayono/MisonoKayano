IssueReward(long rewardID, Action<IssueRewardResponse> callback)
# 描述
该方法用于官方合养精灵形象等奖励的发放。该方法调用仅支持线上环境。
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| rewardID | 用于标识当前奖励的唯一ID（非后台形象的唯一ID），该ID的获取方式请尝试联系运营 |
| callback | 回调函数，返回奖励发放的相关信息，返回内容 <br>  <br> 1. code：int类型，返回0，发放成功，返回其他code则发放失败 <br> 2. message：string类型，返回发放失败的原因 <br> 3. RewardInfo rewardInfo：返回奖励的具体信息的list，包含以下信息 <br>    1. long id： 形象或装扮id <br>    2. string name：奖励名 <br>    3. string imageUrl：缩略图的url <br>    4.  int rewardType：奖励类型，2为形象，3为装扮 |
# 错误码
| 错误码 | 错误原因 |
| --- | --- |
| 10001 | 内部参数错误，请联系运营排查 <br> 可能原因：奖励ID不存在、世界不一致、奖励物品不存在 |
| 10002 | 鉴权失败 |
| 20801  | 当前装扮/非UGC形象已经存在 |
| 20802  | 奖励配置错误 / 奖励ID无效 |
| 20803 | 当前形象奖励数量领取到达上限 |

