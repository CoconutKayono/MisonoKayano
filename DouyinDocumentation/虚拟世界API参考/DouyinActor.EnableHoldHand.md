public void EnableHoldHand()
# 描述
开启牵手行为
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        EnableHoldHandSample(localActor)
    end
end

function EnableHoldHandSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    actor:EnableHoldHand()
    print("--DouyinActorSystemSample:EnableHoldHand=")
end
```


