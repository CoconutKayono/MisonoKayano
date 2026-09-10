public UnityEvent onHoldHandStop
# 描述
[Actor](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)结束牵手状态时从触发该事件
AvatarHoldHandStateType.None 的时候触发该事件
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor.onHoldHandStop:AddListener(HoldHandStopCallBack)
end

function HoldHandStopCallBack()
    print("--DouyinActorSystemSample:结束牵手")
end
```


