public static DouyinInputEvent onJumpInputPerform
# 事件参数
通过 DouyinInputEvent 可获取：

* 手机跳跃按钮点击

# 触发时机
在跳跃动作持续阶段触发。
# 描述
跳跃时事件。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onJumpInputPerform:AddListener(function()
        print("DouyinInputServiceSample:onJumpInputPerform")
    end)
end
```


