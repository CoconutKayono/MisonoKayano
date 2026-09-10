public void DisableFly(bool hideUI)
# 参数
| 参数 | 描述 |
| --- | --- |
| hideUI | 是否隐藏飞行按钮，true：隐藏飞行按钮，false：将飞行按钮置灰 |
# 描述
禁止飞行/悬浮
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        DisableFlySample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function DisableFlySample(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:DisableFly()
    print("--DouyinActor3CSample:DisableFly")
end
```


