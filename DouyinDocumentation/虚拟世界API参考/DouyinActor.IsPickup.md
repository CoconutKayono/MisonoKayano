public bool IsPickup()
# 返回
bool
true：当前手中有物体。
false：当前手中没有物体。
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
        --判断手中是否有物体，有物体丢弃，没有物体捡起
        if localActor:IsPickup() then
            localActor:Drop(self.gameObject)
        else
            localActor:Pickup(self.gameObject, CS.HandType.Right)
        end
    end
end
```


