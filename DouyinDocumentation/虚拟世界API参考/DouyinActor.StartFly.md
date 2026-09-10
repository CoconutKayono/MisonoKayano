public void StartFly(float initHeight ＝ 1.5)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| initHeight | 初始的离地高度，默认 1.5m |
# 描述
开始飞行，可设置初始的离地高度，默认为 1.5m。
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        StartFlySample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function StartFlySample(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor:StartFly()
    print("--DouyinActor3CSample:StartFly")
end
```


