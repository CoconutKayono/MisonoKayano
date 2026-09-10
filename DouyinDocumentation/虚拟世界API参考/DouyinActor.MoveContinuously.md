public void MoveContinuously(Vector2 speed)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| speed | 移动速度的倍速 |
# 描述
向某个方向移动，参数是移动速度的倍速（相当于一直朝某个方向推动摇杆，只能平面移动），该方法只对本地玩家有效。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorMoveContinuously(localActor, Vector2(5, 5))
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorMoveContinuously(actor, speed)
    if not actor or not actor.isLocal then
        return
    end
    actor:MoveContinuously(speed)
    print("--DouyinActor3CSample:MoveContinuously")
end
```


