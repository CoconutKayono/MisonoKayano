public void InviteDuoInteraction(ActorInteractionType type)
# 参数
| 参数 | 描述 |
| --- | --- |
| type | 多人交互类型 |
# 描述
Actor发起一次多人交互，调用这个函数的效果和点击多人交互按钮效果是一致的。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        InviteDuoInteractionSample(localActor)
    end
end

function InviteDuoInteractionSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    print("--DouyinActorSystemSample:InviteDuoInteraction")
    actor:InviteDuoInteraction(CS.DouyinActor.ActorInteractionType.Bubbles)
end
```


