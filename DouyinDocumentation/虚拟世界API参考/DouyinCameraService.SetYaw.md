public static void SetYaw(float yaw)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| yaw | 要设置的偏航角 |
# 描述
设置主相机与主角之间的偏航角，游戏模式有效。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("0") then
        SetYawSample()
    end
end

function SetYawSample()
    DouyinCameraService.SetYaw(10)
    local yaw = DouyinCameraService.GetYaw()
    print("DouyinCameraServiceSample:SetYaw=" .. yaw)
end
```


