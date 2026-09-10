public static Camera GetCamera()
# 返回
Camera
若代理服务有效，返回相机。
否则返回 null。
# 描述
获取与主角绑定的相机。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("4") then
        GetCameraSample()
    end
end

function GetCameraSample()
    local camera = DouyinCameraService.GetCamera()
    print("DouyinCameraServiceSample:GetCamera=" .. camera.gameObject.name)
    return camera
end
```


