public float speed
# 描述
获取或设置当前 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)的移动速度。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorSpeedSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorSpeedSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    local curSpeed = actor.speed
    print("--DouyinActor3CSample:curSpeed=" .. curSpeed)
    actor.speed = 5
end
```


