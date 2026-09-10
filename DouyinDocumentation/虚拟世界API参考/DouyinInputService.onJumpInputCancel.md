public static DouyinInputEvent onJumpInputCancel
# 事件参数
通过 DouyinInputEvent 可获取：

* 手机跳跃按钮点击

# 触发时机
当跳跃操作被中断时触发（例如蓄力未完成突然松开按键）
# 描述
取消跳跃事件。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onJumpInputCancel:AddListener(function()
        print("DouyinInputServiceSample:onJumpInputCancel")
    end)
end
```


