public static DouyinInputZoomEvent onZoomInput
# 事件参数
通过 DouyinInputZoomEvent 可获取：

* 当前两指间距
* 相对于上次的缩放增量
* 缩放中心点坐标

# 触发时机
当检测到双指缩放操作时触发。
# 描述
屏幕缩放（双指）
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onZoomInput:AddListener(function(f)
        print("DouyinInputServiceSample:onZoomInput=" .. f)
    end)
end
```


