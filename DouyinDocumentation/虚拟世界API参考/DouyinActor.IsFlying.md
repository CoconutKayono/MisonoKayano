public bool IsFlying()
# 返回
bool
true：当前正在飞行。
false：当前不在飞行。
# 描述
获取 Actor 当前是否在飞行。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        IsFlyingSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function IsFlyingSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    local isflying = actor:IsFlying()
    print("--DouyinActor3CSample:isflying" .. tostring(isflying))
end
```


