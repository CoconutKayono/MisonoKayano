public static DouyinInputEvent onJumpInputStart
# 事件参数
通过 DouyinInputEvent 可获取：

* 手机跳跃按钮点击

# 触发时机
当发起跳跃操作时触发。
# 描述
跳跃。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onJumpInputStart:AddListener(function()
        print("DouyinInputServiceSample:onJumpInputStart")
    end)
end
```


