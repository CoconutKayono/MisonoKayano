public void OwnerCall(string method, LuaFunction onFinish, params object[] args)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| method | DouyinScript 的 Lua 文件中定义的函数名称 |
| onFinish | 远程调用完成时的回调通知 |
| args | 变量参数 |
# 描述
非主权方调用主权方的函数。
* 使用该方法通知主权方执行某个方法时，是不能保证主权方能接收到该消息，且主权方接收到，回调函数onFinish也不一定能执行。当执行回调函数onFinish时，该消息确实发送成功了，但是没有执行回调，主权方可能也收到消息了。所以使用该方法通知主权方执行逻辑时，拥有一定的不确定性。建议使用同步变量的方式代替该方法。
* 在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("--DouyinNetSample:网络未准备好")
        return
    end
    if Input.GetKeyDown("1") then
        OwnerCallSample()
    end
end

function OwnerCallSample()
    print("--DouyinNetSample:调用主权方的某个函数")
    self:OwnerCall("Method5", function(result)
        if result then
            print("--DouyinNetSample:调用主权方的Method5成功" .. result)
        else
            print("--DouyinNetSample:调用主权方的Method5失败")
        end
    end, 5)
end

function Method5(index)
    print("--DouyinNetSample:收到OwnerCall消息" .. index)
    return "Method5Success"
end
```


