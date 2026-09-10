public static DouyinInputEvent onMoveInputStart
# 事件参数
通过 DouyinInputEvent 可获取：

* 输入方向向量（标准化向量）
* 输入强度值

# 触发时机
当检测到移动输入开始时触发（例如虚拟摇杆开始操作）
# 描述
开始有移动输入。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onMoveInputStart:AddListener(function()
        print("DouyinInputServiceSample:onMoveInputStart")
    end)
end
```


