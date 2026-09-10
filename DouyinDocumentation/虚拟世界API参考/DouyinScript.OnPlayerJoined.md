function OnPlayerJoined(DouyinPlayer player, PlayerJoinEvent evt)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 进入房间的玩家 |
| evt | PlayerJoinEvent 的枚举值 |
# 描述
## 触发时机

1. 当玩家首次加入房间时会触发该事件。
2. 当玩家断线重连时：
   1. 如果`DouyinScript`中定义`OnPlayerRejoined` ，不再触发 `OnPlayerJoined`事件。
   2. 如果`DouyinScript` 中未定义 `OnPlayerRejoined` ，会触发 `OnPlayerJoined`事件。此时，您可以通过判断 `evt` 的值是否为 `CS.PlayerJoinEvent.RejoinRoom` 来区分首次进房和断线重连。

## 事件类型
evt 类型为 PlayerJoinEvent。包括：JoinRoom，RejoinRoom；

1. 玩家首次进入房间时，evt 参数将返回 PlayerJoinEvent.JoinRoom；
2. 玩家重连成功时，evt 参数将返回 PlayerJoinEvent.RejoinRoom；
3. 玩家进入房间时，本客户端和远程客户端触发 OnPlayerJoined 时返回的 evt 参数保证一致。

# 注意事项
该事件用于监听玩家加入房间的事件，如果要监听火人加入游戏使用[DouyinScript.OnActorSpawned](unknown)。使用该事件前，建议先阅读 [玩家与合养精灵](unknown) 章节，理解世界SDK中Actor和Player的差异。
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

