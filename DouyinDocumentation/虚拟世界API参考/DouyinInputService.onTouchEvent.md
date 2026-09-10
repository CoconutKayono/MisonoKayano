public static DouyinTouchEvent onTouchEvent
# 事件参数
通过 DouyinTouchEvent 可获取：

* 触摸点坐标
* 触摸时间戳
* 点击类型

# 触发时机
当用户点击屏幕时触发。
# 描述
屏幕点击事件。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onTouchEvent:AddListener(function(ver2)
        print(string.format("DouyinInputServiceSample:onTouchEvent=((%f,%f))", ver2.x, ver2.y))
    end)
end
```


