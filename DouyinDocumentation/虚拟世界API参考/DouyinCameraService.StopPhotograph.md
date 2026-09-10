public void StopPhotograph()
# 描述
停止相机功能模式
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("3") then
        StopPhotographSample()
    end
end

function StopPhotographSample()
    print("DouyinCameraServiceSample:StopPhotograph")
    DouyinCameraService.StopPhotograph()
end
```


