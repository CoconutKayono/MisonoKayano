public static void Quit()
# 描述
退出游戏
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        QuitSample()
    end
end

function QuitSample()
    DouyinApplication.Quit()
end
```


