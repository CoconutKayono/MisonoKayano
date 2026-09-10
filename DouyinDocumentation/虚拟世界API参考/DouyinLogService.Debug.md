public static void Debug(string message)
# 描述
开发阶段使用的调试日志，用于辅助定位问题；不会上报到后台。
# 参数
| 参数 | 参数描述 |
| --- | --- |
| message | 要输出的日志内容 |
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        DouyinLogService.Debug("---test Debug")
    end
end
```


