public bool StartDuoInteraction(ActorInteractionType type, DouyinActor actor)
# 参数
| 参数 | 描述 |
| --- | --- |
| type | 开始多人交互的类型 |
| actor | 和哪个Actor进行多人交互 |
# 返回
是否开始了多人交互
false：未开始
true：开始
# 描述
Actor A开始开始多人交互，交互的对象是传入的actor
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        local anotherActor = DouyinActorService.GetActorById(anotherActorID)
        if not localActor or not anotherActor then return end
        StartDuoInteractionSample(localActor, anotherActor)
    end
end

function StartDuoInteractionSample(actor, anotherActor)
    if not actor or not actor.isLocal or not anotherActor then
        return
    end

    print("--DouyinActorSystemSample:StartDuoInteraction")
    actor:StartDuoInteraction(CS.DouyinActor.ActorInteractionType.Bump, anotherActor)
end
```


