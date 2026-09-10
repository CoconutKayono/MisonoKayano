public UnityEvent onPickup = new();
# 描述
Actor捡起物体时，触发该事件。
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    --如果需要捡起物体，触发某个逻辑，可以在合适的地方监听该事件；
    --例如：捡起某个物体，可以触发某个机关，就可以在机关类中监听该事件
    actor.onPickup:AddListener(OnActorPickupCallBack)
    --actor.onPickup:RemoveListener(OnActorPickupCallBack)
end

function OnActorPickupCallBack()
    print("玩家捡起了物体")
end
```


