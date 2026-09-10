public GameObject gameObject;
# 描述
与 DouyinPlayer 关联的游戏对象 GameObject。
# 代码示例
玩家进入世界会触发OnPlayerJoined()方法，您可以在该方法中获取加入房间的玩家，并处理相关业务逻辑。玩家离开世界会触发OnPlayerLeft()方法，您可以在该方法中获取离开房间的玩家，并处理相关业务逻辑。

```C#
//玩家加入世界类型
public enum PlayerJoinEvent : int
{
    CreateRoom,
    JoinRoom,
    ReJoinRoom,
}
//玩家离开世界类型
public enum PlayerLeftEvent : int
{
    Disconnect,
    ExitRoom,
}
```

```Lua
-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
-- 注意:evt在Lua侧输出是:CreateRoom:0 JoinRoom:1 ReJoinRoom:2
function OnPlayerJoined(player, evt)
    GetPlayerGameObjectSample(player)
end
-- 玩家离开世界会触发OnPlayerLeft
-- player:DouyinPlayer 离开世界的玩家
-- evt:PlayerJoinEvent 玩家离开世界类型
-- 注意:evt在Lua侧输出是:Disconnect:0 ExitRoom:1
function OnPlayerLeft(player, evt)
    GetPlayerGameObjectSample(player)
end

function GetPlayerGameObjectSample(player)
    if not player or not player.gameObject then return end
    print("--DouyinPlayerSample--" .. "GameObject.name=" .. player.gameObject.name)
end
```


