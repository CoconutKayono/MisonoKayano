public void StopDuoInteractionWaiting()
# 描述
停止交互等待
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        StopDuoInteractionWaiting(localActor)
    end
end

function StopDuoInteractionWaiting(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:StopDuoInteractionWaiting()
    print("--DouyinActorSystemSample:StopDuoInteractionWaiting=")
end
```

