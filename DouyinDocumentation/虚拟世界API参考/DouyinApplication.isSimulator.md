public static bool isSimulator {get}
# 描述
获取当前是否为调试器环境。
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        IsSimulatorSample()
    end
end

function IsSimulatorSample()
    if DouyinApplication.isSimulator then
        DouyinUtility.Toast("当前是模拟器环境")
    else
        DouyinUtility.Toast("当前不是模拟器环境")
    end
end
```


