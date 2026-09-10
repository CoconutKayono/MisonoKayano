public UnityEvent onFlyStop ＝ new();
# 描述
[Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)结束飞行的事件。
# 代码示例
```Lua
local localActor

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor

    actor.onFlyStop:AddListener(OnFlyStopCallBack)
end

function OnFlyStopCallBack()
    print("--DouyinActor3CSample:停止飞行")
end
```


