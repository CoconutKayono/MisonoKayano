public static DateTime GetServerTime()
# 返回
DateTime (日期时间格式)
例如：2025-09-03 14:30:45.123
服务器当前时间
# 描述
返回服务器时间DateTime，默认返回的是UTC 0时区的时间，可以通过DateTime.ToLocalTime()方法转为本地时区时间，可参考下方的代码示例。
在使用网络相关的API时，需要判断网络环境是否已经准备好了。特别是在Awake、Start、Update等生命周期中调用网络API时，很有可能当前网络环境没有准备好，导致出现异常情况。开发者在调用这些API时，需要先使用[DouyinNetService.isNetworkSettled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fr0wz6p5)判断网络环境是否准备好了。

# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if not DouyinNetService.isNetworkSettled then
        print("---网络未准备好")
        return
    end
    if Input.GetKeyDown("3") then
        GetServerTimeSample()
    end
end

function GetServerTimeSample()
    local dt = DouyinUtility.GetServerTime()
    local format = "yyyy-MM-dd HH:mm:ss"
    print("---ServerTime=" .. dt:ToString(format))--ServerTime=2025-11-19 07:11:29
    local localDt = dt:ToLocalTime()
    print("---ServerTime=" .. localDt:ToString(format))--ServerTime=2025-11-19 15:11:29
end
```


