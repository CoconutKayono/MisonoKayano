public bool IsDuoInteractionWaiting()
# 返回
是否正在等待多人交互。
false：未等待
true：等待中
# 描述
Actor等待多人交互，当发起多人交互，其他Actor没有接受多人交互的时候，会处于等待状态。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        IsDuoInteractionWaitingSample(localActor)
    end
end

function IsDuoInteractionWaitingSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    local isWaiting = actor:IsDuoInteractionWaiting()
    print("--DouyinActorSystemSample:isWaiting=" .. tostring(isWaiting))
end
```

