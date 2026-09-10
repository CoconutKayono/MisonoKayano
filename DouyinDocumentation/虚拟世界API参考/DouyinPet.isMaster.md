public bool isMaster。
# 描述
判断当前本地用户是不是控制者，属性为只读。仅当前本地端使用时，该属性为true。该API仅对本地玩家生效。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetMasterSample(pet)
    end
end

function GetPetMasterSample(pet)
    if not pet then return end
    print("--DouyinPetSample:isMaster=" .. tostring(pet.isMaster))
end
```


