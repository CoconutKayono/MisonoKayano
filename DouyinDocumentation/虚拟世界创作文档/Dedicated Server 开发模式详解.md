# 如何开启DS服务器

1. 在Hierarchy面板创建一个空节点，命名为DouyinServerRoot（DouyinServerRoot下必须挂至少一个服务脚本）
2. 点击AddComponent添加组件DouyinServerRoot和DouyinServerScriptLoader
   1. DouyinServerScriptLoader自定义脚本文件夹中的脚本只能由DS服务器使用，客户端不能使用这里的脚本。
   2. DouyinScriptLoader自定义脚本文件夹中的脚本，客户端和DS服务器都可以使用。
   3. 已经放入DouyinScriptLoader自定义脚本文件夹中的脚本，不能再放入DouyinServerScriptLoader中，二者是互斥的。
   4. DouyinServerRoot下不允许挂Canvas节点

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9de301dc200f4884bc46f8dd53ac41db~tplv-goo7wpa0wc-image.image" width="500px" /></div>


3. 打开抖音虚拟资产调试器，如果配置正确，调试器面板会有Ds模式表示，在下方会出现启动服务器端的选项。

> 注意：服务器端只能启动一个，若多次启动服务器端，新启动的服务器端将会“顶掉”之前的服务器端

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8463d6229fc7488cb8c9cda886ce81d2~tplv-goo7wpa0wc-image.image" width="500px" /></div>


4. 勾选启动服务器端，点击开始调试。下方为服务器端，可以点击日志按钮，查看服务端的日志。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/79064dc08d2042a08ae43a43341f6219~tplv-goo7wpa0wc-image.image" width="500px" /></div>

# DS相关API
## DouyinApplication.isServer
用于标识当前是否是Dedicated Server
```Lua
function Start() 
    JudgeIsServer() 
end 
function JudgeIsServer() 
    local isServer = DouyinApplication.isServer 
    print("---isServer: " .. tostring(isServer)) 
    return isServer 
end 
```

## DouyinPlayer.isServer
是否是Dedicated Server的DouyinPlayer
当启动DS时，会进入一个专属于DS的“Player”，这个“Player”并非真实玩家，开发者可以`isServer`字段过滤。

```Lua
function OnPlayerJoined(player, evt) 
    if player.isServer then 
        print("---DSApiTest: 玩家加入房间, player: " .. player.playerOpenID) 
    end 
end 
```

## DouyinObjectService.ServerSpawn
服务器动态生成网络对象，该函数只能在服务器端执行。
**注意**：生成的网络对象仅存在于服务器，不会同步到客户端，生成的对象会放在DouyinServerRoot节点下。
由于DouyinObjectService.ServerSpawn生成的网络对象仅存在于服务器端（客户端无对应实例），因此这些对象不应带有Rigidbody组件或其他物理交互特性。若此类对象包含Rigidbody并与精灵发生碰撞（如阻挡精灵移动），会导致服务器端记录的精灵位置因物理交互改变，而客户端因无该碰撞对象，精灵位置仍保持原状态，最终造成客户端与服务器端位置同步异常。

```Lua
local Vector3 = UnityEngine.Vector3
local Quaternion = UnityEngine.Quaternion
local Input = UnityEngine.Input
local serverObjs = {}

function Start()
    if JudgeIsServer() then
        ServerCreateNetObj_1()
        ServerCreateNetObj_2()
        ServerCreateNetObj_3()
        ServerCreateNetObj_4()
    end
end

function Update()
    if Input.GetKeyDown("1") then
        ServerDestroyNetObjs()
    end
end

function JudgeIsServer()
    local isServer = DouyinApplication.isServer
    print("---isServer: " .. tostring(isServer))
    return isServer
end

function ServerCreateNetObj_1()
    local netObj, netObjId = DouyinObjectService.ServerSpawn("NetObj_1", function (netObj, netObjId)
        print("---DSApiTest: DS ServerCreateNetObj_1 Success, netObj: " .. netObj.name)
        table.insert(serverObjs, netObj)
    end)
end

function ServerCreateNetObj_2()
    local netObj, netObjId = DouyinObjectService.ServerSpawn("NetObj_1", Vector3(1, 0, 0), function (netObj, netObjId)
        print("---DSApiTest: DS ServerCreateNetObj_1 Success, netObj: " .. netObj.name)
        table.insert(serverObjs, netObj)
    end)
end

function ServerCreateNetObj_3()
    local netObj, netObjId = DouyinObjectService.ServerSpawn("NetObj_1", Vector3(2, 0, 0), Vector3(45, 45, 45), function (netObj, netObjId)
        print("---DSApiTest: DS ServerCreateNetObj_1 Success, netObj: " .. netObj.name)
        table.insert(serverObjs, netObj)
    end)
end

function ServerCreateNetObj_4()
    local netObj, netObjId = DouyinObjectService.ServerSpawn("NetObj_1", Vector3(3, 0, 0), Quaternion.identity, function (netObj, netObjId)
        print("---DSApiTest: DS ServerCreateNetObj_1 Success, netObj: " .. netObj.name)
        table.insert(serverObjs, netObj)
    end)
end

function ServerDestroyNetObjs()
    for i = #serverObjs, 1, -1 do
        local netObj = serverObjs[i]
        DouyinObjectService.ServerDestroy(netObj)
        table.remove(serverObjs, i)
    end
end
```

## DouyinObjectService.ServerDestroy
服务器销毁网络对象，该函数只能在服务器端执行。示例同上
## RPC通信相关API
| **类名** |  | API名 | 说明 |
| --- | --- | --- | --- |
| **DouyinRemoteEvent** <br>  | **Event** <br>  | ```C# <br> public UnityEvent<object[]> onClientEvent <br> ``` <br>  | 客户端的事件：服务器调用客户端，客户端需要侦听该事件，并处理业务逻辑 <br>  |
|  |  | ```C# <br> public UnityEvent<DouyinPlayer, object[]> onServerEvent <br> ``` <br>  | 服务端的事件：客户端调用服务器，服务器需要侦听该事件，并处理业务逻辑 |
|  | **Method** <br>  | ```C# <br> public void FireClient(DouyinPlayer player, object[] args) <br> ``` <br>  | 服务器调用指定的客户端 <br>  |
|  |  | ```C# <br> public void FireAllClients(object[] args) <br> ``` <br>  | 服务器广播给所有的客户端 |
|  |  | ```C# <br> public void FireServer(object[] args) <br> ``` <br>  | 客户端调用服务器 <br>  |
| **DouyinRemoteFunction** <br>  | **Event** | ```C# <br> public DouyinClientFunction onClientInvoke <br> ``` <br>  | 客户端的事件：服务器调用客户端，客户端需要侦听该事件，处理业务逻辑并返回结果 <br>  |
|  |  | ```C# <br> public DouyinServerFunction onServerInvoke <br> ``` <br>  | 服务端的事件：客户端调用服务器，服务器需要侦听该事件，处理业务逻辑并返回结果 <br>  |
|  | **Method** | ```C# <br> public void InvokeServer(Action<object[]> response, object[] args) <br> ``` <br>  | 客户端调用服务器，并处理服务器的响应 <br>  |
|  |  | ```C# <br> public void InvokeClient(DouyinPlayer player, Action<DouyinPlayer, object[]> response, object[] args) <br> ``` <br>  | 服务器调用指定的客户端， 并处理客户端响应 <br>  |
注意：最好不要在方法中定义**DouyinRemoteEvent**/**DouyinRemoteFunction**的变量，因为当方法结束时，会将变量进行垃圾回收，这会导致当异步双向通信调用回调时变量报nil

## **DouyinRemoteEvent使用教程**
DouyinRemoteEvent 对象用于在客户端与服务器之间进行异步单向通信，调用方无需等待响应。 
它支持以下几种通信方式： 

* **FireServer：​**从客户端发送至服务器
* **FireClient：​**从服务器发送至单个客户端
* **FireAllClients：​**从服务器广播至所有客户端

### 客户端->服务器（客户端逻辑）
#### 定义客户端调用服务器的DouyinRemoteEvent对象
```Lua
--DSApiRemoteEvent_Client.lua
local ClientToServerEvent = DouyinRemoteEvent("ClientToServer")
```

#### 客户端调用服务器逻辑
```Lua
--DSApiRemoteEvent_Client.lua
local Input = UnityEngine.Input
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
```

#### 客户端清理逻辑
```Lua
--DSApiRemoteEvent_Client.lua
function OnDestroy()
    if ClientToServerEvent ~= nil then
        ClientToServerEvent:Dispose()
        ClientToServerEvent = nil
    end
end
```

### 客户端->服务器（服务器逻辑）
#### 定义客户端调用服务器的DouyinRemoteEvent对象
```Lua
--DSApiRemoteEvent_Server.lua
local ClientToServerEvent = DouyinRemoteEvent("ClientToServer")
```

#### 服务器添加ClientToServerEvent.onServerEvent监听
```Lua
--DSApiRemoteEvent_Server.lua
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
```

#### 服务器清理逻辑
```Lua
--DSApiRemoteEvent_Server.lua
function OnDestroy()
    if DouyinApplication.isServer then
        ClientToServerEvent.onServerEvent:RemoveListener(OnServerEventHandle)
    end
    
    if ClientToServerEvent ~= nil then
        ClientToServerEvent:Dispose()
        ClientToServerEvent = nil
    end
end
```

### 服务器->客户端（服务器逻辑）
#### 定义服务器调用客户端的DouyinRemoteEvent对象
```Lua
--DSApiRemoteEvent_Server.lua
local ServerToClientEvent = DouyinRemoteEvent("ServerToClient")
```

#### 服务器调用客户端逻辑
```Lua
--DSApiRemoteEvent_Server.lua
local Input = UnityEngine.Input

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
```

#### 服务器清理逻辑
```Lua
--DSApiRemoteEvent_Server.lua
function OnDestroy()
    if ServerToClientEvent ~= nil then
        ServerToClientEvent:Dispose()
        ServerToClientEvent = nil
    end
end
```

### 服务器->客户端（客户端逻辑）
#### 定义服务器调用客户端的DouyinRemoteEvent对象
```Lua
--DSApiRemoteEvent_Client.lua
local ServerToClientEvent = DouyinRemoteEvent("ServerToClient")
```

#### 客户端添加ServerToClientEvent.onClientEvent监听
```Lua
--DSApiRemoteEvent_Client.lua
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
```

#### 客户端清理逻辑
```Lua
--DSApiRemoteEvent_Client.lua
function OnDestroy()
    if not DouyinApplication.isServer then
        ServerToClientEvent.onClientEvent:RemoveListener(OnClientEventHandle)
    end

    if ServerToClientEvent ~= nil then
        ServerToClientEvent:Dispose()
        ServerToClientEvent = nil
    end
end
```

### 完整示例
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/092cbdbe41ce40b6bcd16f946a8f2c1b~tplv-goo7wpa0wc-image.image" filename="DSApiRemoteEvent_Client.lua" download>DSApiRemoteEvent_Client.lua</a>
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/982baf48455b4bfdb06c8bca01c0e2dc~tplv-goo7wpa0wc-image.image" filename="DSApiRemoteEvent_Server.lua" download>DSApiRemoteEvent_Server.lua</a>
## DouyinRemoteFunction使用教程
DouyinRemoteFunction 对象用于在客户端与服务器之间进行双向通信。您可以为 DouyinRemoteFunction.onClientInvoke 或 DouyinRemoteFunction.onServerInvoke 事件设置回调函数，来处理来自另一方的调用请求。
### 客户端->服务器->客户端（客户端逻辑）
#### 定义客户端调用服务器的DouyinRemoteFunction对象
```Lua
--DSApiRemoteFunction_Client.lua
local CSToCFunction = DouyinRemoteFunction("ClientToServerToClient")
```

#### 客户端向服务器发起请求
```Lua
--DSApiRemoteFunction_Client.lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("1") then
        ClientRequestServer("Client-Request-参数1", "Client-Request-参数2")
    end
end

function ClientRequestServer(...)
    CSToCFunction:InvokeServer(function (...)
        local responseArgs = {...}
        for _, arg in ipairs(responseArgs) do
            print("---DSApiTest_3: 服务器返回结果, arg: " .. arg)
        end
    end, ...)
end
```

#### 客户端清理逻辑
```Lua
--DSApiRemoteFunction_Client.lua
function OnDestroy()
    if CSToCFunction ~= nil then
        CSToCFunction:Dispose()
        CSToCFunction = nil
    end
end
```

### 客户端->服务器->客户端（服务器逻辑）
#### 定义客户端调用服务器的DouyinRemoteFunction对象
```Lua
--DSApiRemoteFunction_Server.lua
local CSToCFunction = DouyinRemoteFunction("ClientToServerToClient")
```

#### 服务器添加CSToCFunction.onClientInvoke监听
```Lua
--DSApiRemoteFunction_Server.lua
function Start()
    if DouyinApplication.isServer then
        --客户端通知服务器执行逻辑，服务器添加事件监听，执行对应逻辑
        CSToCFunction.onServerInvoke:AddListener(OnServerResponseHandle)
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
```

#### 服务器清理逻辑
```Lua
--DSApiRemoteFunction_Server.lua
function OnDestroy()
    if DouyinApplication.isServer then
        CSToCFunction.onServerInvoke:RemoveListener(OnServerResponseHandle)
    end

    if CSToCFunction ~= nil then
        CSToCFunction:Dispose()
        CSToCFunction = nil
    end
end
```

### 服务器->客户端->服务器（服务器逻辑）
#### 定义服务器调用客户端的DouyinRemoteFunction对象
```Lua
local SCToSFunction = DouyinRemoteFunction("ServerToClientToServer")
```

#### 服务器向客户端发起请求
```Lua
local Input = UnityEngine.Input

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

function ServerRequestClient(targetPlayer, ...)
    SCToSFunction:InvokeClient(targetPlayer, function (player, ...)
        local responseArgs = {...}
        print("---DSApiTest_4: 客户端响应，返回结果, player: " .. player.playerOpenID)
        for _, arg in ipairs(responseArgs) do
            print("---DSApiTest_4: 客户端响应，返回结果, arg: " .. arg)
        end
    end, ...)
end
```

#### 服务器清理逻辑
```Lua
function OnDestroy()
    if SCToSFunction ~= nil then
        SCToSFunction:Dispose()
        SCToSFunction = nil
    end
end
```

### 服务器->客户端->服务器（客户端逻辑）
#### 定义服务器调用客户端的DouyinRemoteFunction对象
```Lua
--DSApiRemoteFunction_Client.lua
local SCToSFunction = DouyinRemoteFunction("ServerToClientToServer")
```

#### 客户端添加SCToSFunction.onClientInvoke监听
```Lua
--DSApiRemoteFunction_Client.lua
function Start()
    if not DouyinApplication.isServer then
        --服务器通知客户端执行逻辑，客户端添加事件监听，执行对应逻辑
        SCToSFunction.onClientInvoke:AddListener(OnClientResponseHandle)
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
```

#### 客户端清理逻辑
```Lua
--DSApiRemoteFunction_Client.lua
function OnDestroy()
    if not DouyinApplication.isServer then
        SCToSFunction.onClientInvoke:RemoveListener(OnClientResponseHandle)
    end

    if SCToSFunction ~= nil then
        SCToSFunction:Dispose()
        SCToSFunction = nil
    end
end
```

### 完整示例
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/cebb25cddfb04458b8df64cb348dd8df~tplv-goo7wpa0wc-image.image" filename="DSApiRemoteFunction_Client.lua" download>DSApiRemoteFunction_Client.lua</a>
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/2f095b54901243dda04d84209bef68c9~tplv-goo7wpa0wc-image.image" filename="DSApiRemoteFunction_Server.lua" download>DSApiRemoteFunction_Server.lua</a>
# 常见问题解答
#### 1、是否有只在服务器端执行、客户端不执行的代码？

* **方式1**：将挂载DouyinScript脚本的节点放在DouyinServerRoot节点下。DouyinServerRoot节点及其子节点仅在服务器端存在，逻辑仅在服务器执行。
* **方式2**：使用`DouyinObjectService.ServerSpawn`创建挂载DouyinScript脚本的网络对象。该方式创建的网络对象会自动置于DouyinServerRoot节点下，仅在服务器端存在，客户端不会同步。
* **方式3**：通过`DouyinApplication.isServer`或`DouyinPlayer.isServer`判断当前环境是否为服务器，仅在条件成立时执行代码。

#### 2、是否有只在客户端执行、服务器端不执行的代码？
**回答：​**无。
#### 3、使用DouyinRemoteEvent进行服务器与客户端通信时，参数类型有哪些限制？
**回答：​**仅支持基础数据类型（bool, byte, short, int, long, float, double, string等），可通过Lua可变参数传递多个数据，但不支持table等复杂类型。
#### 4、服务器脚本的生命周期和房间生命周期是一致的吗？
**回答：​**是的。
#### 5、是否可以在服务器处理玩家退出（包括最后一个玩家）的逻辑呢？
**回答：​**是的。
#### 6、在服务器节点下面定义的同步变量，不会同步到客户端吗？
**回答：​**是的。
#### 7、所有的DouyinRemoteEvent / DouyinRemoteFunction 都不保证一定到达吗
**回答：​**是的，DouyinRemoteEvent和DouyinRemoteFunction均不保证消息100%到达接收方。
**原因分析：**

* 网络通信的天然不确定性会导致消息丢失或无法送达，常见场景包括：
   * **网络异常**：客户端与服务器之间的连接波动（如延迟过高、断连重连），导致消息在传输链路中丢失。
   * **接收方状态异常**：例如客户端崩溃、玩家主动退出游戏，或服务器负载过高无法及时处理消息。
   * **异步通信特性**：
      * DouyinRemoteEvent为异步单向通信，发送方不会等待接收方的确认。
      * DouyinRemoteFunction虽支持双向响应，但仍依赖网络传输的可靠性，无法完全避免丢失。

#### 8、在DS开发模式下，数据存储上报-11002错误码是什么意思？
**回答**：对于使用DS开发的新世界，数据存储必须要写到DS服务器脚本上，若在客户端脚本上调用数据存储相关的API将会上报-11002错误码。
#### 9、如果使用DS模式进行开发，客户端可以调用数据存储API吗？
**回答**：所有数据存储业务逻辑必须要写到DS脚本上，不允许在客户端脚本上调用任何数据存储相关API接口
#### 10、不能在方法内定义DouyinRemoteEvent、DouyinRemoteFunction吗？
**回答**：是的。若在方法内部将`DouyinRemoteEvent`、`DouyinRemoteFunction`声明为局部变量，则当该变量被垃圾回收时，会自动触发`RemoveListener`操作以清理事件监听。
#### 11、NetworkNetPacket_PlayerEnterSyncForOther Playerlnfos miss. 报错如何解决？
回答：在DouyinServerRoot下挂一个服务脚本即可

