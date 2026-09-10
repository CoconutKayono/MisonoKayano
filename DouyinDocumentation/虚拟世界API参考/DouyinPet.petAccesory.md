public List<string> petAccesory
# 描述
获取该合养精灵的装扮列表
# 代码示例
调试器模式下，无法获取到合养精灵的装扮列表，可以在扫码调试阶段获取到该列表。
```Lua
---@var logText:UnityEngine.UI.Text
---@end

-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetAccesorySample(pet)
    end
end

function GetPetAccesorySample(pet)
    if not pet or not pet.petAccesory then return end
    logText.text = string.format("--DouyinPetSample:装扮数量=%d", pet.petAccesory.Count)
    print(string.format("--DouyinPetSample:装扮数量=%d", pet.petAccesory.Count))
    for i = 0, pet.petAccesory.Count - 1 do
        logText.text = logText.text .. string.format("--DouyinPetSample:petAccesory[%d]=%s", i, pet.petAccesory[i])
        print(string.format("--DouyinPetSample:petAccesory[%d]=%s", i, pet.petAccesory[i]))
    end
end
```


