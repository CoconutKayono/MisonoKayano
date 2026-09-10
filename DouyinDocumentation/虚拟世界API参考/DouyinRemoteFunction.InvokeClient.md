public void InvokeClient(DouyinPlayer player, Action<DouyinPlayer, object[]> response, object[] args)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| response | 用于处理服务器响应的回调函数 |
| args | 客户端向服务器传递的参数 |
# 描述
服务器向指定客户端发起异步远程调用。服务器可以通过 `args` 参数向客户端传递数据，并注册一个 `response` 回调函数，用于处理客户端的返回值。客户端接收到调用后执行相应逻辑，并将结果返回给服务器。
# 代码示例
客户端
```Lua
local Input = UnityEngine.Input

local CSToCFunction = DouyinRemoteFunction("ClientToServerToClient")
local SCToSFunction = DouyinRemoteFunction("ServerToClientToServer")

function Start()
    if not DouyinApplication.isServer then
        --服务器通知客户端执行逻辑，客户端添加事件监听，执行对应逻辑
        SCToSFunction.onClientInvoke:AddListener(OnClientResponseHandle)
    end
end

function Update()
    if Input.GetKeyDown("1") then
        ClientRequestServer("Client-Request-参数1", "Client-Request-参数2")
    end
end

--服务器通知客户端执行逻辑，客户端添加事件监听，执行对应逻辑，返回结果给服务器
function OnClientResponseHandle(...)
    local requestArgs = {...}
    for _, arg in ipairs(requestArgs) do
        print("---DSApiTest_3: 客户端收到服务器请求, arg: " .. arg)
    end
    return "Server-Response-参数1", "Server-Response-参数2"
end

function ClientRequestServer(...)
    CSToCFunction:InvokeServer(function (...)
        local responseArgs = {...}
        for _, arg in ipairs(responseArgs) do
            print("---DSApiTest_3: 服务器返回结果, arg: " .. arg)
        end
    end, ...)
end

function OnDestroy()
    if not DouyinApplication.isServer then
        SCToSFunction.onClientInvoke:RemoveListener(OnClientResponseHandle)
    end

    if SCToSFunction ~= nil then
        SCToSFunction:Dispose()
        SCToSFunction = nil
    end

    if CSToCFunction ~= nil then
        CSToCFunction:Dispose()
        CSToCFunction = nil
    end
end
```

服务器
```Lua
local Input = UnityEngine.Input

local CSToCFunction = DouyinRemoteFunction("ClientToServerToClient")
local SCToSFunction = DouyinRemoteFunction("ServerToClientToServer")

function Start()
    if DouyinApplication.isServer then
        --客户端通知服务器执行逻辑，服务器添加事件监听，执行对应逻辑
        CSToCFunction.onServerInvoke:AddListener(OnServerResponseHandle)
    end
end

function Update()
    if Input.GetKeyDown("2") then
        local allPlayers = DouyinPlayerService.GetPlayers()
        if allPlayers and allPlayers.Length > 0 then
            local player = allPlayers[1]
            print("---DSApiTest_4: ServerRequestClient, player: " .. player.playerOpenID)
            ServerRequestClient(player, "Server-Request-参数1", "Server-Request-参数2")
        end
    end
end

--客户端通知服务器执行逻辑，服务器添加事件监听，执行对应逻辑，返回结果给客户端
function OnServerResponseHandle(player, ...)
    local requestArgs = {...}
    print("---DSApiTest_4: 服务器收到客户端请求, player: " .. player.playerOpenID)
    for _, arg in ipairs(requestArgs) do
        print("---DSApiTest_4: 服务器收到客户端请求, arg: " .. arg)
    end
    return "Server-Response-参数1", "Server-Response-参数2"
end

function ServerRequestClient(targetPlayer, ...)
    SCToSFunction:InvokeClient(targetPlayer, function (player, ...)
        local responseArgs = {...}
        print("---DSApiTest_4: 客户端响应，返回结果, player: " .. player.playerOpenID)
        for _, arg in ipairs(responseArgs) do
            print("---DSApiTest_4: 客户端响应，返回结果, arg: " .. arg)
        end
    end, ...)
end

function OnDestroy()
    if DouyinApplication.isServer then
        CSToCFunction.onServerInvoke:RemoveListener(OnServerResponseHandle)
    end

    if SCToSFunction ~= nil then
        SCToSFunction:Dispose()
        SCToSFunction = nil
    end

    if CSToCFunction ~= nil then
        CSToCFunction:Dispose()
        CSToCFunction = nil
    end
end
```


