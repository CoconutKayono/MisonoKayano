public UnityEvent onActorLoaded ＝ new();
# 描述
当用户在世界内进行了切换[合养精灵](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da2cedba73204fe90a455?docLang=zh&bv=67e3b8b8505b920501ed9219)形象时的回调。调试器内是没有切换[合养精灵](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da2cedba73204fe90a455?docLang=zh&bv=67e3b8b8505b920501ed9219)形象的功能都，开发者可以在扫码调试阶段进行测试。
# 代码示例
```Lua
---@var logText:UnityEngine.UI.Text
---@end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    actor.onActorLoaded:AddListener(SwichActorCallBack)
end

function SwichActorCallBack(actor)
    if not actor then
        return
    end
    logText.text = string.format("--DouyinActorSystemSample:%s切换了精灵形象", actor.actorID)
    print(string.format("--DouyinActorSystemSample:%s切换了精灵形象", actor.actorID))
end
```


