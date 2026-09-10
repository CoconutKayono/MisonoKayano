public static void Log(string message)
# 描述
通用日志，用于记录常规运行信息、简单流程节点与基础状态，内容轻量无特殊优先级。
# 参数
| 参数 | 参数描述 |
| --- | --- |
| message | 要输出的日志内容 |
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        DouyinLogService.Log("---test Log")
    end
end
```


