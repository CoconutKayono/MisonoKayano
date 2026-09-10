public static DouyinInputPerformEvent onMoveInputPerform
# 事件参数
通过 DouyinInputPerformEvent 可获取：

* 当前移动方向
* 实时输入强度
* 持续时间参数

# 触发时机
在移动输入持续过程中每帧触发。
# 描述
持续有移动输入。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onMoveInputPerform:AddListener(function()
        print("DouyinInputServiceSample:onMoveInputPerform")
    end)
end
```


