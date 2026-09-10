public AvatarHoldHandStateType GetHoldHandState()
# 返回
返回牵手状态的枚举类型
```C#
public enum AvatarHoldHandStateType
{
    None = 1, // 未牵手
    Front, // 队首
    Rear, // 队尾
    Middle, // 队中间
}
```

# 描述
获取Actor牵手状态
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        local localActor = DouyinActorService.GetLocalActor()
        if not localActor then return end
        GetHoldHandStateSample(localActor)
    end
end

function GetHoldHandStateSample(actor)
    if not actor or not actor.isLocal then
        return
    end

    local state = actor:GetHoldHandState()
    print("--DouyinActorSystemSample:GetHoldHandState=" .. tostring(state))
end
```


