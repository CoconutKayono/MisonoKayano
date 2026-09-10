public bool CanHoldHand()
# 返回
bool
true：当前Actor 可以牵手
false：当前 Actor 无法牵手
# 描述
当前 Actor 是否可以牵手
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        CanHoldHandSample(localActor)
    end
end

function CanHoldHandSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    local canHold = actor:CanHoldHand()
    print("--DouyinActorSystemSample:CanHoldHand=" .. tostring(canHold))
end
```


