public void PlayEmoji(int emojiIndex)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| emojiIndex | 代表要播放的表情的索引 |
# 描述
播放表情。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        PlayEmojiSample(localActor)
    end
end

function PlayEmojiSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    print("--DouyinActorSystemSample:PlayEmojiSample")
    actor:PlayEmoji(1)
end
```


