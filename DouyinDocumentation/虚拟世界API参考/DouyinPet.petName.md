public string petName
# 描述
调用 DouyinService.Proxy.GetpetName 获取合养精灵的名称。
如果为 null，返回空字符串。
# 代码示例
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetNameSample(pet)
    end
end

function GetPetNameSample(pet)
    if not pet then return end
    print("--DouyinPetSample:petName=" .. pet.petName)
end
```


