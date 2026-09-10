public static void Info(string message)
# 描述
信息日志，用于记录关键流程、状态变化与重要事件，便于追踪与排查问题。
# 参数
| 参数 | 参数描述 |
| --- | --- |
| message | 要输出的日志内容 |
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        DouyinLogService.Info("---test Info")
    end
end
```


