public DouyinActor GetActor()
# 参数
无。
# 返回
DouyinActor
非null：返回玩家当前控制的对象实例。
null：当前玩家尚未控制任何对象。
# 描述
获取当前玩家所控制的对象实例。若玩家尚未创建对象实例，则返回 `null`。
# 代码示例
使用GetActor()方法时，需要判空，有可能获取到的对象为null。
注意：OnPlayerJoined()方法和OnActorSpawned()方法之间是乱序的。假设有两个玩家进入了世界，这个时候会调用两次OnPlayerJoined()方法时，会创建两个的DouyinPlayer对象。之后调用OnActorSpawned()方法创建DouyinActor对象，这个时候可能会先创建玩家2的DouyinActor对象，然后再创建玩家1的DouyinActor对象。也就是说，您需要判断创建出的DouyinActor对象是属于玩家1还是玩家2的。
```Lua
local localPlayer

-- 玩家进入世界会触发OnPlayerJoined
-- player:DouyinPlayer 加入世界的玩家
-- evt:PlayerJoinEvent 玩家进入世界类型
-- 注意:evt在Lua侧输出是:CreateRoom:0 JoinRoom:1 ReJoinRoom:2
function OnPlayerJoined(player, evt)
    if IsLocalPlayerSample(player) then
        localPlayer = player
    end
end

-- 创建DouyinActor对象实例时会触发OnActorSpawned
-- actor:DouyinActor
function OnActorSpawned(actor)
    -- 可以通过DouyinActor.isLocal判断该对象是否是属于本地玩家的
    if actor.isLocal then
        -- 本地玩家对应的DouyinActor创建出来了，此时调用GetActor()方法就不会返回null了
        GetPlayerActorSample(localPlayer)
    end
    -- 可以使用DouyinActor.UID==DouyinPlayer.playerOpenID判断Actor和Player是否一一对应
    if localPlayer and actor.UID == localPlayer.playerOpenID then
        -- TODO
    end
end

function IsLocalPlayerSample(player)
    if not player then return end
    print("--DouyinPlayerSample--" .. "isLocal=" .. tostring(player.isLocal))
    return player.isLocal
end

function GetPlayerActorSample(player)
    if not player then return end
    local actor = player:GetActor()
    if actor and actor.gameObject then
        print("--DouyinPlayerSample--" .. "DouyinActor.name=" .. actor.gameObject.name)
    end
end
```


