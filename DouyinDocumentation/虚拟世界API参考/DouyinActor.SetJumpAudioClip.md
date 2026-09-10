public void SetJumpAudioClip(AudioClip clip)
# 描述
设置跳跃的音效
# 参数
| 参数 | 描述 |
| --- | --- |
| clip | 要播放的跳跃音效片段 |
# 代码示例
```Lua
---@var TestBtn:UnityEngine.UI.Button
---@var JumpAudioClip:UnityEngine.AudioClip
---@var FootsAudioClips:UnityEngine.AudioClip[]
---@end

function Start()
    TestBtn.onClick:AddListener(function ()
        SetJumpAudioClipSample()
    end)
end

function SetJumpAudioClipSample()
    local actor = DouyinActorService.GetLocalActor()
    if actor then
        print("--设置跳跃声音")
        actor:SetJumpAudioClip(JumpAudioClip)
    end
end
```


