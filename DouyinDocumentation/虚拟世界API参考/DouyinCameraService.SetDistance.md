public static void SetDistance(float distance)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| distance | 所要设置的主相机距主角的距离 |
# 描述
设置主相机与主角之间的距离，游戏模式有效。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("8") then
        SetDistanceSample()
    end
end

function SetDistanceSample()
    DouyinCameraService.SetDistance(10)
    print("DouyinCameraServiceSample:SetDistance=10")
end
```


