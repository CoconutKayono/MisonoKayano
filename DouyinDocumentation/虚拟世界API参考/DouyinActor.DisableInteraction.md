public void DisableInteraction()
# 描述
把当前对象移除掉可交互对象
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
    localActor:DisableInteraction()
end
```


