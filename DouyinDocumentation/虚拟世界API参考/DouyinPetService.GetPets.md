public static DouyinPet[] GetPets()
# 返回
DouyinPet[]
一个包含所有 DouyinPet 实例（合养精灵）的数组。
# 描述
获取当前场景内所有的合养精灵。
# 代码示例

```Lua
local Input = UnityEngine.Input

-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function Update()
    if Input.GetKeyDown("space") then
        GetPetsSample()
    end
end

function GetPetsSample()
    local petArr = DouyinPetService.GetPets()
    if petArr then
        for i = 0, petArr.Length - 1 do
            print(string.format("--DouyinPetServiceSample:GetPetsSample():petArr[%d]=%s", i, petArr[i].petName) ..
                petArr[i].petOpenID)
        end
    end
    return petArr
end
```


