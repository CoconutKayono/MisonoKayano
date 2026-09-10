public int petLevel
# 描述
调用 DouyinService.Proxy.GetPetLevel 方法，获取合养精灵等级。
如果为 null，返回 0。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetLevelSample(pet)
    end
end

function GetPetLevelSample(pet)
    if not pet then return end
    print("--DouyinPetSample:petLevel=" .. pet.petLevel)
end
```


