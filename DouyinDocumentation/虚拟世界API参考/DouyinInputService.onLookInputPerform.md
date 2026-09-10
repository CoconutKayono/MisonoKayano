public static DouyinInputPerformEvent onLookInputPerform
# 事件参数
包含视角旋转的：

* X/Y轴向旋转量
* 旋转速度参数
* 当前视角角度限制

# 触发时机
在视角旋转过程中每帧持续触发。
# 描述
旋转视角（屏幕空白区域）
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onLookInputPerform:AddListener(function(ver2)
        print(string.format("DouyinInputServiceSample:onLookInputPerform=((%f,%f))", ver2.x, ver2.y))
    end)
end
```


