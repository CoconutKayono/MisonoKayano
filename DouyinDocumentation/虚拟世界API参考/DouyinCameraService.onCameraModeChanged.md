public static DouyinCameraModeEvent onCameraModeChanged
# 事件参数
public enum DouyinCameraMode
{

   GamePlay = 0 //游戏模式
   Photograph= 1 //拍照模式

}
DouyinCameraModeEvent 会传递当前切换到的相机模式作为参数。


# 描述
相机模式发生切换时触发该事件。
# 代码示例
```Lua
function Start()
    DouyinCameraService.onCameraModeChanged:AddListener(function(mode)
        if mode == CS.DouyinCameraMode.GamePlay then
            print("处于游戏模式")
        else
            print("处于拍照模式")
        end
    end)
end
```


