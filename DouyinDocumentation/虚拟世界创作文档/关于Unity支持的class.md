问：目前SDK支持哪些Unity class，struct支持吗？
答：目前SDK仅支持只支持从UnityEngine.Object集成下来的Class，意味着只有这些class才能使用 ---@ 这样的格式来定义变量。
如果要对 struct（结构体）变量定义数组，可以参考下方的定义方式。

```Lua
local raycastResults = CS.System.Array.CreateInstance(typeof(UnityEngine.RaycastHit), checkNum)
```


