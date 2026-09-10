public float jumpHeight
# 描述
获取或设置当前Actor的跳跃高度
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorJumpHeightSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorJumpHeightSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    print("--DouyinActor3CSample:jumpHeight=" .. actor.jumpHeight)
    actor.jumpHeight = 10
end
```


