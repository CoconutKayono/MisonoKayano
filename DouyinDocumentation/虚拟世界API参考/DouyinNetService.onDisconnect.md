public static UnityEvent<int> onDisconnect
# 描述
当前网络中断时触发该事件
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinNetService.onDisconnect:AddListener(OnDisconnectCallBack)
end

function OnDisconnectCallBack(reason)
    print("--DouyinNetService.onDisconnect, reason:", reason)
end

function OnDestroy()
    DouyinNetService.onDisconnect:RemoveListener(OnDisconnectCallBack)
end
```

