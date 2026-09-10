public void StopDuoInteraction(ActorInteractionType type, DouyinActor actor)
# 参数
| 参数 | 描述 |
| --- | --- |
| type | 多人交互类型 |
| actor | 停止多人交互的Actor对象 |
# 描述
退出双人交互，如果是引导者，停止所有的双人交互；如果是跟随者，停止跟随者后续的所有双人交互
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        StopDuoInteractionSample(localActor)
    end
end

function StopDuoInteractionSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    print("--DouyinActorSystemSample:StopDuoInteraction")
    actor:StopDuoInteraction(function()
        print("--DouyinActorSystemSample:多人交互回调")
    end)
end
```

