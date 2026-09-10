public static float GetYaw()
# 返回
float
若代理服务正常，返回主相机与主角之间的偏航角。
否则返回 null。
# 描述
获取主相机与主角之间的偏航角，游戏模式有效。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("7") then
        GetYawSample()
    end
end

function GetYawSample()
    local yaw = DouyinCameraService.GetYaw()
    print("DouyinCameraServiceSample:GetYaw=" .. yaw)
end
```


