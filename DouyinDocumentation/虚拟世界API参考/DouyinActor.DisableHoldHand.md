public void DisableHoldHand()
# 描述
禁止牵手行为
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        DisableHoldHandSample(localActor)
    end
end

function DisableHoldHandSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    actor:DisableHoldHand()
    print("--DouyinActorSystemSample:DisableHoldHand=")
end
```


