public static bool isServer {get;}
# 描述
用于标识当前是否是Dedicated Server
# 代码示例
```Lua
function Start()
    JudgeIsServer()
end

function JudgeIsServer()
    local isServer = DouyinApplication.isServer
    print("---isServer: " .. tostring(isServer))
    return isServer
end
```


