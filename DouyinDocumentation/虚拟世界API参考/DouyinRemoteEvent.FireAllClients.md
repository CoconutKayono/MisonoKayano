public void FireAllClients(object[] args)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| args | 服务器广播时，发送给所有客户端的参数 |
# 描述
在服务器端调用，向所有已连接的客户端广播一个远程事件。调用时可以传递任意数量和类型的参数（`args`）。所有客户端都会接收到该事件，并通过监听 `onClientEvent` 事件来获取并处理这些参数。此方法常用于需要同步信息给所有用户的场景，例如发送全服公告、同步游戏状态等。
# 代码示例
客户端
```Lua
local Input = UnityEngine.Input

local ServerToClientEvent = DouyinRemoteEvent("ServerToClient")
local ClientToServerEvent = DouyinRemoteEvent("ClientToServer")

function Start()
    if not DouyinApplication.isServer then
        --服务器通知客户端执行逻辑，客户端添加事件监听，执行对应逻辑
        ServerToClientEvent.onClientEvent:AddListener(OnClientEventHandle)
    end
end

--服务器通知客户端事件回调
function OnClientEventHandle(...)
    local args = {...}
    if args ~= nil then
        for _, arg in pairs(args) do
            print("---DSApiTest_1: 客户端收到事件, args: ", arg)
        end
    else
        print("---DSApiTest_1: 客户端收到事件, args is nil")
    end
end

function Update()
    if Input.GetKeyDown("1") then
        if DouyinApplication.isServer then
            return
        end
        local actor = DouyinActorService.GetLocalActor()
        if actor then
            FireServer(actor.actorID)
        end
    end
end

--客户端通知服务器执行逻辑
function FireServer(...)
    ClientToServerEvent:FireServer(...)
end

function OnDestroy()
    if not DouyinApplication.isServer then
        ServerToClientEvent.onClientEvent:RemoveListener(OnClientEventHandle)
    end

    if ServerToClientEvent ~= nil then
        ServerToClientEvent:Dispose()
        ServerToClientEvent = nil
    end
    if ClientToServerEvent ~= nil then
        ClientToServerEvent:Dispose()
        ClientToServerEvent = nil
    end
end

```

服务器
```Lua
local Input = UnityEngine.Input

local ServerToClientEvent = DouyinRemoteEvent("ServerToClient")
local ClientToServerEvent = DouyinRemoteEvent("ClientToServer")

local playerOpenID

function Start()
    if DouyinApplication.isServer then
        --客户端通知服务器执行逻辑，服务器添加事件监听，执行对应逻辑
        ClientToServerEvent.onServerEvent:AddListener(OnServerEventHandle)
    end
end

--客户端通知服务端事件回调
function OnServerEventHandle(player, args)
    if args ~= nil then
        print("---DSApiTest_1: 服务端收到事件, player: ", player.playerOpenID)
        print("---DSApiTest_1: 服务端收到事件, args: ", args)
    else
        print("---DSApiTest_1: 服务端收到事件, args is nil")
    end
end

function Update()
    if Input.GetKeyDown("2") then
        if not DouyinApplication.isServer then
            return
        end
        local targetPlayer = DouyinPlayerService.GetPlayerByOpenID(playerOpenID)
        FireClient(targetPlayer, "参数1", "参数2")
    elseif Input.GetKeyDown("3") then
        if not DouyinApplication.isServer then
            return
        end
        FireAllClients("参数3")
    end
end

---@param player DouyinPlayer 进入房间的玩家
---@param evt PlayerJoinEvent PlayerJoinEvent 的枚举值
function OnPlayerJoined(player, evt)
    if not DouyinApplication.isServer or player.isServer then
        return
    end
    if playerOpenID == nil then
        playerOpenID = player.playerOpenID
    end
end

--服务器通知指定客户端执行逻辑
function FireClient(player, ...)
    ServerToClientEvent:FireClient(player, ...)
end

--服务器通知所有客户端执行逻辑
function FireAllClients(...)
    ServerToClientEvent:FireAllClients(...)
end

function OnDestroy()
    if DouyinApplication.isServer then
        ClientToServerEvent.onServerEvent:RemoveListener(OnServerEventHandle)
    end

    if ServerToClientEvent ~= nil then
        ServerToClientEvent:Dispose()
        ServerToClientEvent = nil
    end

    if ClientToServerEvent ~= nil then
        ClientToServerEvent:Dispose()
        ClientToServerEvent = nil
    end
end
```


