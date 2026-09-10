public int petID
# 描述
火人的ID，进入房间时会变化
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetIDSample(pet)
    end
end

function GetPetIDSample(pet)
    if not pet then return end
    print("--DouyinPetSample:petID=" .. pet.petID)
end
```


