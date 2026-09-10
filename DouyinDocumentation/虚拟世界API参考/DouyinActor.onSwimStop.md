public UnityEvent onSwimStop = new();
# 描述
Actor停止游泳时，触发该事件。
# 代码示例
```Lua
local localActor

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
    actor.onSwimStop:AddListener(OnSwimStopCallBack)
end

function OnSwimStopCallBack()
    print("--DouyinActor3CSample:停止游泳")
end
```


