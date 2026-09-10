public static float GetPitch()
# 返回
float
若代理服务正常，返回相机与主角之间的俯仰角
否则，返回null
# 描述
获取主相机与主角之间的俯仰角，游戏模式有效
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("5") then
        GetPitchSample()
    end
end

function GetPitchSample()
    local picth = DouyinCameraService.GetPitch()
    print("DouyinCameraServiceSample:GetPitch=" .. picth)
end
```

# 
