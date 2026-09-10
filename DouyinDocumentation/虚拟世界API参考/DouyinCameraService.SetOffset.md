public static void SetOffset(Vector3 offset)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| offset | 所要设置的位置偏移 |
# 描述
设置主相机与主角位置偏移，游戏模式有效。
# 代码示例
```Lua
function Update()
    if Input.GetKeyDown("9") then
        SetOffsetSample()
    end
end

function SetOffsetSample()
    local offset = Vector3(1, 1, 1)
    DouyinCameraService.SetOffset(offset)
    print(string.format("DouyinCameraServiceSample:SetOffset=((%f,%f,%f))", offset.x, offset.y, offset.z))
end
```


