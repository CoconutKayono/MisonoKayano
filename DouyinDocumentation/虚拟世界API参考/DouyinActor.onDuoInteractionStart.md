public UnityEvent<DouyinActor.ActorInteractionType, string, int, int> onDuoInteractionStart
# 描述
[Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)开始播放双人动作事件，参数动作ID，动作名，双人交互的ActorID
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor.onDuoInteractionStart:AddListener(OnDuoInteractionStartCallBack)
end

function OnDuoInteractionStartCallBack(actionId, actionName, actorID1, actorID2)
    print(string.format("--DouyinActorSystemSample:%d和%d播放了%s动作，动作Id是%s", actorID1, actorID2, actionName,
        tostring(actionId)))
end
```


