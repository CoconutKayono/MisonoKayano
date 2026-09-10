public void StartPhotograph()
# 描述
进入相机功能模式
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("2") then
        StartPhotographSample()
    end
end

function StartPhotographSample()
    print("DouyinCameraServiceSample:StartPhotograph")
    DouyinCameraService.StartPhotograph()
end
```


