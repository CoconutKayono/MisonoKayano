public static void OnNetworkSettled(Action callback)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| callback | 用于在房间数据同步完成时执行特定的操作 |
# 描述
处理房间数据同步完成后的回调逻辑。
当数据同步后，会立即执行传入的回调函数，
若未同步，将回调函数添加到委托链中等待数据同步后再执行。
