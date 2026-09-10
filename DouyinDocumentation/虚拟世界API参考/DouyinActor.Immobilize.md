public void Immobilize(bool immobile)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| immobile | true：玩家无法通过摇杆移动 <br> false：玩家可以通过摇杆移动 |
# 描述
设置为 True 时玩家无法通过摇杆移动；只对本地玩家有效。
设置为 False 后解除该效果；设置时不改变玩家当前状态，只对后续输入生效。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorImmobilize(localActor, true)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorImmobilize(actor, immobile)
    if not actor or not actor.isLocal then
        return
    end
    actor:Immobilize(immobile)
    print("--DouyinActor3CSample:Immobilize")
end
```


