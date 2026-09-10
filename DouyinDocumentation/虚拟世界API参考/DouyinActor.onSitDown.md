public UnityEvent onSitDown = new();
# 描述
Actor坐下时，触发该事件。
# 代码示例

```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    --如果需要Actor坐下时，触发某个逻辑，可以在合适的地方监听该事件；
    actor.onSitDown:AddListener(OnActorSitDownCallBack)
    --actor.onSitDown:RemoveListener(OnActorSitDownCallBack)
end

function OnActorSitDownCallBack()
    print("玩家坐下")
end
```


