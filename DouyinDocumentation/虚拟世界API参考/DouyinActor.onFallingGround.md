public UnityEvent onFallingGround ＝ new();
# 描述
Actor 落地的事件。
# 代码示例
```Lua
local localActor

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor

    actor.onFallingGround:AddListener(OnFallingGround)
end

function OnFallingGround()
    print("--DouyinActor3CSample:落地")
end
```


