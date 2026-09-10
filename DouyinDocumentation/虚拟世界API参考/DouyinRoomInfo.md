# 描述
用户信息结构体，用来存储房间信息。
# 公开属性
| roomID | string | 房间ID |
| --- | --- | --- |
| worldID | string | 房间所属的世界ID |
| inviterOpenID | string | 邀请者ID |
| enterFrom | int | 用户入口来源： <br>  <br> * `-1`：其他渠道 <br> * `0`：逛一逛 <br> * `1`：侧边栏 |
# 代码示例
```Lua
function OnPlayerJoined(player)
    DouyinRoomService.GetCurrentRoomInfo(function (roomInfo)
        if roomInfo then
            if roomInfo.enterFrom == -1 then
                print("[TEST] 其他渠道进入房间")
            elseif roomInfo.enterFrom == 0 then
                print("[TEST] 从逛一逛进入房间")
            elseif roomInfo.enterFrom == 1 then
                print("[TEST] 从侧边栏进入房间")
            end
        else
            print("[TEST] GetCurrentRoomInfo failed")
        end
    end)
end

function OnPlayerRejoined(player)
    print("---OnPlayerRejoined")
end
```


