public UnityEvent<string> onEmotionPlay
# 描述
[Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)使用表情事件，参数表情名
# 代码示例
```Lua
function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor.onEmotionPlay:AddListener(PlayEmojiCallBack)
end

function PlayEmojiCallBack(emotion)
    print("--DouyinActorSystemSample:emotion=" .. emotion)
end
```


