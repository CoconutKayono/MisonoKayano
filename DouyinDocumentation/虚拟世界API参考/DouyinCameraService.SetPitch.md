public static void SetPitch(float pitch)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| pitch | 所要设置的俯仰角 |
# 描述
设置主相机与主角之间的俯仰角，游戏模式有效。
```Lua
function Update()
    if Input.GetKeyDown("6") then
        SetPitchSample()
    end
end

function SetPitchSample()
    DouyinCameraService.SetPitch(10)
    local picth = DouyinCameraService.GetPitch()
    print("DouyinCameraServiceSample:SetPitch=" .. picth)
end
```


