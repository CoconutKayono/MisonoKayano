public static DouyinInputEvent onLookInputCancel
# 事件参数
通过 DouyinInputEvent 可获取：

* 输入强度值

# 触发时机
当视角旋转操作被终止时触发。
# 描述
旋转视角操作取消。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onLookInputCancel:AddListener(function()
        print("DouyinInputServiceSample:onLookInputCancel")
    end)
end
```


