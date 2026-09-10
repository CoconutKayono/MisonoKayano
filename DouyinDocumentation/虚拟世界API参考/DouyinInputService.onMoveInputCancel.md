public static DouyinInputEvent onMoceInputCancel
# 事件参数
通过 DouyinInputEvent 可获取：

* 输入方向向量（标准化向量）
* 输入强度值

# 触发时机
当移动输入中断时触发。
# 描述
移动输入取消。
# 代码示例
```Lua
-- Start is called before the first frame update
function Start()
    DouyinInputService.onMoveInputCancel:AddListener(function()
        print("DouyinInputServiceSample:onMoveInputCancel")
    end)
end
```


