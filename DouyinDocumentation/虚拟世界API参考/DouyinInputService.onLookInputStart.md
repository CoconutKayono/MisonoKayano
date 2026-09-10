public static DouyinInputEvent onLookInputStart
# 事件参数
通过 DouyinInputEvent 可获取：

* 输入方向向量（标准化向量）
* 输入强度值

# 触发时机
当开始旋转视角时触发（手指开始滑动屏幕空白区域）
# 描述
旋转视角（屏幕空白区域）
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onLookInputStart:AddListener(function()
        print("DouyinInputServiceSample:onLookInputStart")
    end)
end
```


