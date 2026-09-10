public UnityEvent onStandUp = new();
# 描述
Actor站起时，触发该事件。
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    --如果需要Actor坐下时，触发某个逻辑，可以在合适的地方监听该事件；
    actor.onStandUp:AddListener(OnActorStandUpCallBack)
    --actor.onStandUp:RemoveListener(OnActorStandUpCallBack)
end

function OnActorStandUpCallBack()
    print("玩家站起")
end
```


