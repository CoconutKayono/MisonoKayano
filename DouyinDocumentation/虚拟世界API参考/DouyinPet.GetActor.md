public DouyinActor GetActor()
# 参数
无。
# 返回
DouyinActor
如果 ID 存在，返回玩家的 Actor 实例。
否则返回 null。
# 描述
通过合养精灵的 ID 获取玩家。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetActorSample(pet)
    end
end

function GetActorSample(pet)
    if not pet then return end
    local actor = pet:GetActor()
    if actor and actor.gameObject then
        print("--DouyinPetSample:gameObjectName=" .. actor.gameObject.name)
    end
end
```


