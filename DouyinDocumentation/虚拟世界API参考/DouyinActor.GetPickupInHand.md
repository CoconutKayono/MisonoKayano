public GameObject GetPickupInHand(HandType handType ＝ HandType.Right)
# 参数
| 参数  | 参数描述 |
| --- | --- |
| handType | 可选参数，默认为 HandType.Right。该参数用于指定要查询的手的类型 |
# 返回
GameObject
非 null: 指定手正在拾取的游戏对象。
没有拾取对象时返回 null。
# 描述
获取指定手正在拾取的物体。
# 代码示例

```Lua
local localActor

function OnActorTriggerEnter(actor)
    if not actor or not actor.isLocal then
        return
    end
    if not localActor then
        localActor = actor
    end
end

--玩家点击弹出的交互按钮时，会执行该函数
--index表示点击的是第几个按钮
function OnInteractorButtonClick(index)
    if index == 1 then
        local pickupObj = localActor:GetPickupInHand()
        if pickupObj then
            print("手中已有物体:name=" .. pickupObj.name)
        end
    end
end
```


