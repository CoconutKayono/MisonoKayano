public static DouyinPet GetLocalPet()

# 参数
无。
# 返回
DouyinPet
玩家存在且找到对应的合养精灵实例，返回该合养精灵实例。
玩家为 null 或找不到相应的实例，返回 null 并报错。
# 描述
获取当前玩家控制的合养精灵。
# 代码示例

```Lua
local Input = UnityEngine.Input

-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function Update()
    if Input.GetKeyDown("space") then
        GetLocalPetSample()
    end
end

function GetLocalPetSample()
    local pet = DouyinPetService.GetLocalPet()
    if pet then
        print("--DouyinPetServiceSample:GetLocalPet():petName=" .. pet.petName .. pet.petOpenID)
    end
    return pet
end
```


