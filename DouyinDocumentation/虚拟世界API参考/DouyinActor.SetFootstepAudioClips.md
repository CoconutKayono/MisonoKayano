public void SetFootstepAudioClips(AudioClip[] clips)
# 描述
设置脚步声。传入的数组应包含两个音效，分别对应：左脚的声音、右脚的声音。
# 参数
| 参数 | 描述 |
| --- | --- |
| clips | 脚步声数组。应包含两个音效，分别对应：左脚的声音、右脚的声音。 |
# 代码示例
```Lua
---@var TestBtn:UnityEngine.UI.Button
---@var JumpAudioClip:UnityEngine.AudioClip
---@var FootsAudioClips:UnityEngine.AudioClip[]
---@end

function Start()
    TestBtn.onClick:AddListener(function ()
        SetFootstepAudioClipsSample()
    end)
end

function SetFootstepAudioClipsSample()
    local actor = DouyinActorService.GetLocalActor()
    if actor then
        print("--设置脚步声音")
        local arr = CS.System.Array.CreateInstance(typeof(CS.UnityEngine.AudioClip), 2)
        arr[0] = FootsAudioClips[0]
        arr[1] = FootsAudioClips[1]
        actor:SetFootstepAudioClips(arr)
    end
end
```


