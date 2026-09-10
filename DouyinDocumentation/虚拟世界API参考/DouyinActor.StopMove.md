public void StopMove()
# 描述
停止移动，相当于取消上个 API 的持续移动效果。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorStopMoveSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorStopMoveSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:StopMove()
    print("--DouyinActor3CSample:StopMove")
end
```


