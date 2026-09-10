function OnPlayerRejoined(DouyinPlayer player)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 进入房间的玩家 |
# 描述
当有玩家断线重连时触发。

1. 如果`DouyinScript`中定义`OnPlayerRejoined` ，断线重连时不再触发 `OnPlayerJoined`事件。
2. 如果`DouyinScript` 中未定义 `OnPlayerRejoined` ，断线重连时会触发 `OnPlayerJoined`事件。此时，您可以通过判断 `OnPlayerJoined(player, evt)` 的evt值是否为 `CS.PlayerJoinEvent.RejoinRoom` 来区分首次进房和断线重连。

# 注意事项
该事件用于监听玩家重新加入房间的事件，如果要监听火人加入游戏使用[DouyinScript.OnActorSpawned](unknown)。使用该事件前，建议先阅读 [玩家与合养精灵](unknown) 章节，理解世界SDK中Actor和Player的差异。
# 代码示例
```Lua

function OnPlayerJoined(player, evt)
    if evt == CS.PlayerJoinEvent.JoinRoom then
        print("---OnPlayerJoined JoinRoom")
    elseif evt == CS.PlayerJoinEvent.RejoinRoom then
        print("---OnPlayerJoined RejoinRoom")
    else
        print("---OnPlayerJoined unknown")
    end
end


function OnPlayerRejoined(player)
    print("---OnPlayerRejoined")
end
```

