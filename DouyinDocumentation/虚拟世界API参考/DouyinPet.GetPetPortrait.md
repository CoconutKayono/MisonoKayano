public void GetPetPortrait(bool original, Action<Sprite> callback)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| original | true: 获取原始头像 / false: 获取装扮的形象 |
| callback | 回调方法 |
# 描述
获取该DouyinPet的头像
# 代码示例
调试器模式下可以获取到原始头像，但无法获取到装扮的形象。也就是说，如果参数original为true，可以获取到原始头像，并显示在调试器中；如果参数original为false，获取到的头像数据为null，调试器中也无法显示。
```Lua
-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    local pet = actor.douyinPet
    if pet then
        GetPetAccesorySample(pet)
    end
end

function GetPetPortraitSample(pet, original)
    if not pet then return end
    print("--DouyinPetSample:开始加载头像")
    pet:GetPetPortrait(original, function(portrait)
        if portrait then
            if original then
                oPortraitImg.sprite = portrait
            else
                aPortraitImg.sprite = portrait
            end
            print("--DouyinPetSample:头像加载完成")
        else
            print("--DouyinPetSample:portrait is nil")
        end
    end)
end
```


