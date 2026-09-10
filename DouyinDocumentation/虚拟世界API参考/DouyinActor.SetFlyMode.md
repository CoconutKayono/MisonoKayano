public void SetFlyMode(int mode)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| mode | mode：1  正常飞行 <br> mode：0 悬浮 |
# 描述
设置飞行模式。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorSetFlyModeSample(localActor, 0)
        --ActorSetFlyModeSample(localActor, 1)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorSetFlyModeSample(actor, flymode)
    if not actor or not actor.isLocal then
        return
    end
    print("--DouyinActor3CSample:SetFlyMode")
    actor:SetFlyMode(flymode)
end
```


