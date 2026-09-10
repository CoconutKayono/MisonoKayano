public bool CanMove()
# 返回
bool
true: 可以移动。
false: 不能移动。
# 描述
判断当前 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)是否可以移动。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorCanMoveSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorCanMoveSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    local canMove = actor:CanMove()
    print("--DouyinActor3CSample:CanMove=" .. tostring(canMove))
end
```


