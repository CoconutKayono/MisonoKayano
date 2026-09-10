public static void Warning(string message)
# 描述
警告日志。表示出现了需要关注的异常或潜在风险，但通常不会立即中断当前流程。
# 参数
| 参数 | 参数描述 |
| --- | --- |
| message | 要输出的日志内容 |
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        DouyinLogService.Warning("---test Warning")
    end
end
```


