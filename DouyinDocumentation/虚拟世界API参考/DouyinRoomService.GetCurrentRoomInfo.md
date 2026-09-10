public static void GetCurrentRoomInfo(Action<DouyinRoomInfo> cb)
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| cb | 回调函数，承载着获取到的房间信息DouyinRoomInfo |
# 描述
获取当前房间信息。
# 代码示例
```Lua
local Input = UnityEngine.Input

function Update()
    if Input.GetKeyDown("0") then
        GetCurrentRoomInfoSample()
    end
end

function GetCurrentRoomInfoSample()
    DouyinRoomService.GetCurrentRoomInfo(function (roomInfo)
        print(string.format("---GetCurrentRoomInfo:roomID=%s__worldID=%s", roomInfo.roomID, roomInfo.worldID))
    end)
end
```


