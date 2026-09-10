public static DouyinPet GetPet(int petID)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| petID | 要获取的合养精灵的 ID |
# 返回
DouyinPet
非 null：该合养精灵的实例。
null：报错找不到对应的实例。
# 描述
通过 PetID，获取当前场景内的合养精灵。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetSample(pet)
    end
end

function GetPetSample(petID)
    local pet = DouyinPetService.GetPet(petID)
    if pet then
        print("--DouyinPetServiceSample:GetPet():petName=" .. pet.petName .. pet.petOpenID)
    end
    return pet
end
```


