public static void Error(string message)
# 描述
错误日志。表示发生功能异常或关键流程失败，可能导致部分功能不可用，需要尽快处理。
# 参数
| 参数 | 参数描述 |
| --- | --- |
| message | 要输出的日志内容 |
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        DouyinLogService.Error("---test Error")
    end
end
```


