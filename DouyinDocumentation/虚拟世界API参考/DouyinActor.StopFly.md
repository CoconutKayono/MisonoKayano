public void StopFly()
# 描述
当前 Actor 停止飞行。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        StopFlySample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function StopFlySample(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:StopFly()
    print("--DouyinActor3CSample:StopFly")
end
```


