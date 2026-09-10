public void EnableInteraction()
# 描述
把当前对象设置为可交互对象
# 代码示例
```Lua
local localActor

function OnActorTriggerEnter(actor)
    if not actor or not actor.isLocal then
        return
    end
    if not localActor then
        localActor = actor
    end
    localActor:EnableInteraction()
end
```


