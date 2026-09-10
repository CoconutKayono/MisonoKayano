public bool HasControllership()
# 返回
bool
true：有控制权，
false：没有控制权。
# 描述
判断是否有控制权。
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
        HasControllershipSample()
    end
end

function HasControllershipSample()
    local player = DouyinPlayerService.GetLocalPlayer()
    if not player then return end
    local hasController = self:HasControllership()
    if hasController then
        print(string.format("--DouyinNetSample:HasControllership:%s拥有%s的控制权", player.playerOpenID, self.gameObject.name))
    else
        print(string.format("--DouyinNetSample:HasControllership:%s未拥有%s的控制权", player.playerOpenID, self.gameObject.name))
    end
end
```


