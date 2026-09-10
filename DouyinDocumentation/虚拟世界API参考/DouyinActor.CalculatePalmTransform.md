public void CalculatePalmTransform(bool isLeft, out Vector3 position, out Quaternion rotation)
# 参数
| 参数 | 描述 |
| --- | --- |
| isLeft | true: 左手挂点 / false：右手挂点 |
| position | 返回挂点的位置 |
| rotation | 返回挂点的旋转信息 |
# 描述
计算当前 Actor 手部挂点
# 代码示例
```Lua
function ActorCalculatePalmTransform(actor, isLeft)
    local position, rotation = actor:CalculatePalmTransform(isLeft)
    local str = string.format("--DouyinActorSample:position=(%f,%f,%f):rotation=(%f,%f,%f)", position.x, position.y,
        position.z, rotation.eulerAngles.x, rotation.eulerAngles.y,
        rotation.eulerAngles.z)
    print(str)
    return position, rotation
end
```


