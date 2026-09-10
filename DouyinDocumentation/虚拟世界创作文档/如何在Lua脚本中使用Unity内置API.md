问：如何在Lua脚本中使用Unity内置的API？
答：在Douyin Script脚本中使用Unity内置的API需要通过Unity API完整的命空间来使用。
比如：在Update函数中累加时间

```Go
local timer = 0

function Start()
end

function Update()
    timer = timer + UnityEngine.Time.deltaTime
end
```


