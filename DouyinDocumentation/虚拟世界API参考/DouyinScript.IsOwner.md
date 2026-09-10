public bool IsOwner(DouyinPlayer player)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 判断 DouyinPlayer 是否为所有者 |
# 返回
bool
true：有主权，
false：无主权。
# 描述
判断指定的 DouyinPlayer 是否拥有该物体的主权。
在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--DouyinNetSample:网络未准备好")
        return
    end
    if Input.GetKeyDown("1") then
        IsOwnerSample()
    end
end

function IsOwnerSample()
    local player = DouyinPlayerService.GetLocalPlayer()
    if not player then return end
    local isowner = self:IsOwner(player)
    if isowner then
        print(string.format("--DouyinNetSample:%s是主权方", player.playerOpenID))
    else
        print(string.format("--DouyinNetSample:%s不是主权方", player.playerOpenID))
    end
end
```


