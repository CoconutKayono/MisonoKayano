public void StopHoldHand()
# 描述
结束当前 Actor 的牵手状态
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        StopHoldHandSample(localActor)
    end
end

function StopHoldHandSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    actor:StopHoldHand()
    print("--DouyinActorSystemSample:StopHoldHand")
end
```


