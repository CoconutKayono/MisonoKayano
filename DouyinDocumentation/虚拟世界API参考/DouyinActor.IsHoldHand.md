public bool IsHoldHand()
# 返回
bool
true：当前Actor处于牵手状态
false：当前Actor未处于牵手状态
#  描述
当前Actor是否处于牵手状态
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        IsHoldHandSample(localActor)
    end
end

function IsHoldHandSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    local isHold = actor:IsHoldHand()
    print("--DouyinActorSystemSample:IsHoldHand=" .. tostring(isHold))
end
```


