public void AcceptDuoInteraction(DouyinActor actor)
# 参数
| 参数 | 描述 |
| --- | --- |
| actor | 接受交互的Actor |
# 描述
Actor接受其他Actor发起的交互，调用这个函数的效果和点击其他玩家发起的交互按钮效果是一致的。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        local anotherActor = DouyinActorService.GetActorById(anotherActorID)
        if not localActor or not anotherActor then return end
        AcceptDuoInteractionSample(anotherActor, localActor)
    end
end

--inviteActor：发起交互的Actor，也就是调用InviteDuoInteraction的Actor
--acceptActor：接受交互的Actor，需要AcceptDuoInteraction的Actor
function AcceptDuoInteractionSample(inviteActor, acceptActor)
    if not acceptActor or not acceptActor.isLocal or not inviteActor then
        return
    end
    acceptActor:AcceptDuoInteraction(inviteActor)
    print(string.format("--DouyinActorSystemSample:%s接受了%s的交互邀请", acceptActor.actorID, inviteActor.actorID))
end
```

