public void RequestOwnership(Action<bool>  onFinished)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| onFinished | 请求完成时的回调通知。如果回调函数中的 bool 参数为 true，则请求成功，否则请求失败。 |
# 描述
请求该对象的主权。
在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
当调用RequestOwnership()方法时，会向当前**主权方**发送主权转移请求通知。主权方收到请求后，会自动执行回调方法[DouyinScript.OnOwnershipRequest(int senderID)](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=isb7h6vh)，用于答复是否同意转移。
主权方返回 true 代表同意主权转移，返回 false 代表不同意主权转移（默认行为：若未实现此方法，或未显式设置返回值（如方法无返回语句），则默认**同意转移**（等效于返回 `true`））。当主权方同意后，会发送[OnOwnershipTransferred](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hmuqupj3)事件给房间内所有人。
如果一个物体上有多个脚本都有此事件函数，则所有脚本都返回 true 才是同意请求，只要有一个脚本返回 false，则拒绝请求，且后续其他脚本中的对应[OnOwnershipTransferred](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hmuqupj3)事件将不再执行。因此请避免在答复主权转移的事件函数中，实现赋值相关逻辑，因为有可能他不会被执行。 
```Lua
local Input = UnityEngine.Input

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--DouyinNetSample:网络未准备好")
        return
    end
    if Input.GetKeyDown("1") then
        RequestOwnershipSample()
    end
end

function RequestOwnershipSample()
    self:RequestOwnership(function(success)
        local player = DouyinPlayerService.GetLocalPlayer()
        if success and self.gameObject and player then
            print(string.format("--DouyinNetSample:RequestOwnershipSample:请求成为%s主权方成功", player.playerOpenID))
        else
            print("--DouyinNetSample:请求成为主权方失败")
        end
    end)
end
```


