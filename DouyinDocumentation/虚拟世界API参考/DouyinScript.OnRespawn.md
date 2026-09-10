function OnRespawn()
# 描述
物体重生时，目前是低于世界配置重生高度时重生。
# 代码示例
Actor调用Respawn()方法之后，会调用DouyinScript上的OnRespawn()方法
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        RespawnSample(localActor)
    end
end

function RespawnSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    print("--DouyinActorSystemSample:RespawnSample")
    actor:Respawn()
end

function OnRespawn()
    print("--DouyinActorSystemSample:玩家重生")
end
```


