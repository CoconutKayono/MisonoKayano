public string petAppearance
# 描述
获取该合养精灵的形象，返回合养精灵当前形象的名称
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetAppearanceSample(pet)
    end
end

function GetPetAppearanceSample(pet)
    if not pet then return end
    print("--DouyinPetSample:petAppearance=" .. pet.petAppearance)
end
```


