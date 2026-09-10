public float minSlopeAngleLimit
# 描述
获取或设置当前 Actor 在斜坡上最小能站立的角度。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorminSlopeAngleLimit(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorminSlopeAngleLimit(actor)
    if not actor or not actor.isLocal then
        return
    end
    print("--DouyinActor3CSample:ActorminSlopeAngleLimit" .. actor.minSlopeAngleLimit)
end
```


