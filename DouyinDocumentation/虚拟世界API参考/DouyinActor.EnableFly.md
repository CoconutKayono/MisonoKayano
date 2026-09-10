public void EnableFly(bool showUI = true)
# 参数
| 参数 | 描述 |
| --- | --- |
| showUI | 是否显示飞行按钮。该参数非必填参数，不具备UI显隐功能。 |
# 描述
开启飞行/悬浮
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        EnableFlySample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function EnableFlySample(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:EnableFly()
    print("--DouyinActor3CSample:EnableFly")
end
```


