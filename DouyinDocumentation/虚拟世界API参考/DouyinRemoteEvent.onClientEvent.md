public UnityEvent<object[]> onClientEvent
# 描述
客户端事件，用于接收并处理从服务器发送的远程事件。
您需要在客户端通过 `AddListener` 方法为该事件注册回调函数。当服务器调用 `DouyinRemoteEvent` 实例的 `FireClient` 或 `FireAllClients` 方法时，该事件将被触发，您所注册的回调函数也会被执行，同时接收到服务器传递的参数。
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


