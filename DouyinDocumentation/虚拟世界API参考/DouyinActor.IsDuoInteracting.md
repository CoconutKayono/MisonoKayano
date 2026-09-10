public bool IsDuoInteracting()
# 返回
是否正在多人交互。
false：未进行交互
true：交互中
# 描述
Actor正在多人交互交互中。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        IsDuoInteractingSample(localActor)
    end
end

function IsDuoInteractingSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    local isInteracting = actor:IsDuoInteracting()
    print("--DouyinActorSystemSample:IsDuoInteracting=" .. tostring(isInteracting))
end
```

