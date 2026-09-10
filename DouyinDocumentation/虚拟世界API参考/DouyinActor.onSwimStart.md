public UnityEvent onSwimStart = new();
# 描述
Actor开始游泳时，触发该事件。
# 代码示例
```Lua
local localActor

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor

    actor.onSwimStart:AddListener(OnSwimStartCallBack)
end

function OnSwimStartCallBack()
    print("--DouyinActor3CSample:开始游泳")
end
```


