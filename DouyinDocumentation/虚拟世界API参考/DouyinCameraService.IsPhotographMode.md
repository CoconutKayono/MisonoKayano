public bool IsPhotographMode()
# 返回
bool
true: 当前处于相机模式
false：当前未处于相机模式
# 描述
判断当前相机功能模式的状态
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("1") then
        IsPhotographModeSample()
    end
end

function IsPhotographModeSample()
    local isPhotoMode = DouyinCameraService.IsPhotographMode()
    print("DouyinCameraServiceSample:IsPhotographMode=" .. tostring(isPhotoMode))
    return isPhotoMode
end
```


