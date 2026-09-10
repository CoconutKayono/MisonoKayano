public int petOpenID
# 描述
合养精灵的唯一标识符，在创建合养精灵对象时进行初始化，属性为只读。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetOpenIDSample(pet)
    end
end

function GetPetOpenIDSample(pet)
    if not pet then return end
    print("--DouyinPetSample:petOpenID=" .. pet.petOpenID)
end
```


