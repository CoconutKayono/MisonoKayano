function OnPlayerLeft(DouyinPlayer player, PlayerLeftEvent evt)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| player | 离开房间的玩家 |
| evt | PlyaerLeftEvent 的枚举值 |
# 描述
当有玩家离开房间时触发。
evt  类型为 PlayerLeftEvent。
包括： Disconnect,ExitRoom。

1. 正常退出房间，evt 参数将返回 PlayerNetEvent.ExitRoom；
2. 杀进程、断线时，evt 参数将返回 PlayerNetEvent.Disconnect；
3. 玩家离开房间时，本客户端和远程客户端触发 OnPlayerLeft 时返回的 evt 参数确保一致；
4. OnPlayerLeft为协程函数，支持coroutine.yield方式异步等待 `c#协程` 和 `DATASTORE协程`
5. 客户端退房时，等待OnPlayerLeft协程完成再执行退出
   1. DS模式下：DS Server端等待与Player有关的所有OnPlayerLeft协程执行完成再退出（超时时间5s）；
   2. Shared模式下：将等待此客户端Player有关的所有OnPlayerLeft协程执行完成再退出（超时时间5s）；

# 注意事项
该事件用于监听玩家加入房间的世界，不建议使用该事件监听合养精灵加入游戏。使用该事件前，建议先阅读 [玩家与合养精灵](unknown)章节，理解世界SDK中Actor和Player的差异。
# 代码示例
```Lua
function OnPlayerLeft(player, reason)
    -- 可以使用Unity协程等待
    -- coroutine.yield(CS.UnityEngine.WaitForSeconds(2))
    
    -- 等待数据存储完成
    local datastoreCoro = DATASTORE(function()
        local ok, store = DouyinDataService.GetDataStore('PlayerInventory', 'player001')
        if ok ~= 0 then
            print("OnPlayerLeft() datastore GetDataStore Failed")
            return
        end

        --利用SetData函数，传入数值
        local ok, val, info = store:SetData('t1_1', 2)
        if ok ~= 0 then
            print("OnPlayerLeft() datastore SetData failed")
            return
        end
        
        --利用GetData函数，获取数值
        local ok, val, info = store:GetData('t1_1');
        if ok ~= 0 then
            print("OnPlayerLeft() datastore GetData")
        end
    end)

    -- 等待数据存储完成
    coroutine.yield(datastoreCoro)
end
```


