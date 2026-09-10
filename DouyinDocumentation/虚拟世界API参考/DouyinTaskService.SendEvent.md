public static void SendEvent(DouyinTaskEvent eventName, string eventData = "")
# 描述
通知任务平台完成任务
# 参数
| 参数 | 参数描述 |
| --- | --- |
| eventName | 表示任务的类型。根据不同的任务类型，`eventData` 参数需要传入不同的值： <br>  <br> * **`DouyinTaskEvent.Terminal`**：此时 `eventData` 参数应留空。 <br> * **`DouyinTaskEvent.UGCTask`**：此时 `eventData` 参数应传入在创作者后台配置的任务 ID。 |
| eventData | 创作者后台后台配置的任务ID |
# 代码示例
```Lua
-- 后台配置的任务ID
local customTaskID = "customTaskID"

function TaskTest()
    DouyinTaskService.SendEvent(CS.DouyinTaskEvent.UGCTask, customTaskID)
end
```


