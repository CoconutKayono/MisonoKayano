public bool isServer { get; }
# 描述
是否是Dedicated Server的DouyinPlayer；Dedicated Server 是特殊的DouyinPlayer；
# 代码示例
```Lua
function OnPlayerJoined(player, evt)
    if player.isServer then
        print("---DSApiTest: 玩家加入房间, player: " .. player.playerOpenID)
    end
end
```


