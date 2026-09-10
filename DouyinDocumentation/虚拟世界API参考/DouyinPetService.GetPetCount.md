public static int GetPetCount()
# 返回
int
当前场景内合养精灵数量。
# 描述
获取当前场景内合养精灵的数量。
# 代码示例
```Lua
local Input = UnityEngine.Input

-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function Update()
    if Input.GetKeyDown("space") then
        GetPetCountSample()
    end
end

function GetPetCountSample()
    local count = DouyinPetService.GetPetCount()
    print("--DouyinPetServiceSample:GetPetCount():petCount=" .. count)
    return count
end
```


