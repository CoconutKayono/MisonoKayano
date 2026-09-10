public UnityEvent onDrop = new();
# 描述
Actor丢弃某个物体时，触发该事件。
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    --如果需要丢弃物体，触发某个逻辑，可以在合适的地方监听该事件；
    actor.onDrop:AddListener(OnActorDropCallBack)
    --actor.onDrop:RemoveListener(OnActorDropCallBack)
end

function OnActorDropCallBack()
    print("玩家丢弃了物体")
end
```


