 public void RequestControllership(Action<bool> onFinished)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| onFinished | 远程调用完成时的回调通知，如果回调函数中的布尔参数为 true，则请求成功 |
# 描述
申请控制权。
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
        RequestControllershipSample()
    end
end

function RequestControllershipSample()
    self:RequestControllership(function(success)
        local player = DouyinPlayerService.GetLocalPlayer()
        if success and self.gameObject and player then
            print(string.format("--DouyinNetSample:RequestControllership:请求%s的控制权成功", player.playerOpenID))
        else
            print("--DouyinNetSample:RequestControllership:请求控制权失败")
        end
    end)
end
```


